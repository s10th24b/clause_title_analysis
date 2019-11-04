import time
import os
import pickle
import glob
import re
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import font_manager,rc
import pandas as pd
from konlpy.tag import Kkma, Okt, Komoran, Hannanum, Mecab #Twitter has changed to Okt
pos_taggers = [('kkma', Kkma()), ('Okt', Okt()), ('Komoran', Komoran()),('Hannanum', Hannanum())]

def make_clause_title_files(txt_files):
    process_time = time.time()
    print(len(txt_files),"files detected.")

    for idx,txt_file in enumerate(txt_files):
        file_name = str(txt_file.split('/')[len(txt_file.split('/'))-1])
        #print("txt_name:",file_name)
        with open(txt_file,'r',encoding='utf8') as rdata:
            with open(clause_title_file_dir+'/'+file_name.split('.')[0]+'_clause_title'+'.txt','w',encoding='utf8') as wdata:
                print(idx+1,"/",len(txt_files),"current_file:",txt_file)
                lines = rdata.readlines()
                for line in lines:
                    line = line.replace('"','')
                    line = line.replace('u"\u201C"','')  #left quotation mark
                    line = line.replace('u"\u201D"','')  #right quotation mark
                    line = line.strip()
                    regex = re.compile(r"^제\d+조\s{0,10}\((.{0,100})\)|^제\s{0,10}\d+조\s{0,10}\((.{0,100})\)|^제\d+\s{0,10}조\s{0,10}\((.{0,100})\)|^제\s{0,10}\d+\s{0,10}조\s{0,10}\((.{0,100})\)")
                    matchobj = regex.match(line)
                    if matchobj is not None:
                        wc = matchobj.group() #wc means whole_clause_title
                        #print("Whole Clause Title:",wc)
                        wdata.write(wc+'\n')
                        #mc means main_clause_title

                        #mc = regex.findall(line)
                        # above findall(line) code is same as below for loop codes.
 
                        for group_idx in range(1,5):
                            mc = matchobj.group(group_idx)
                            if mc is not None:
                                #print("Main Clause Title:",mc)
                                break
    clause_title_files = glob.glob(clause_title_file_dir+'/*_clause_title.txt')
    process_time = time.time() - process_time
    print('make_clause_files process done. %.3f' % (process_time))
    return clause_title_files

def sort_unique_values(clause_title_files):
    process_time = time.time()
    str_idx = 0
    clause_title_dic = dict()
    with open(clause_title_file_dir+'/'+'clause_title_unique_values'+'.txt','w',encoding='utf8') as wdata:
        for idx,cl_title_file in enumerate(clause_title_files):
            file_name = str(cl_title_file.split('/')[len(cl_title_file.split('/'))-1])
            #print("clause_title_name:",file_name)
            with open(cl_title_file,'r',encoding='utf8') as rdata:
                print(idx+1,"/",len(clause_title_files),"current_file:",cl_title_file)
                lines = rdata.readlines()
                for line in lines:
                    line = line.replace('"','')
                    line = line.replace('u"\u201C"','')  #left quotation mark
                    line = line.replace('u"\u201D"','')  #right quotation mark
                    line=str(line)
                    for idx in range(0,len(line)):
                        if line[idx] == '(':
                            str_idx = idx
                    #print(line[str_idx+1:-2])
                    cl_title = line[str_idx+1:-2]
                    if cl_title in clause_title_dic:
                        clause_title_dic[cl_title]+=1
                    else:
                        clause_title_dic[cl_title] = 1
        clause_title_dic =sorted(clause_title_dic.items(),key=lambda t : t[1])
        for k,v in clause_title_dic:
            #print("k:",k,"v:",v)
            wdata.write(str(k)+" "+str(v)+" "'\n')
    process_time = time.time() - process_time
    print('sort_unique_values process done. %.3f' % (process_time))
    return clause_title_dic

def morphem_analysis(clause_title_files):
    process_time2 = time.time()
    str_idx = 0
    clause_title_dic_list = list()
    clause_title_dic_name_list = list()
    clause_title_token_dic_ = dict()
    clause_title_token_dic_kkma = dict()
    clause_title_dic_list.append(clause_title_token_dic_kkma)
    clause_title_dic_name_list.append("kkma")
    clause_title_token_dic_Okt = dict()
    clause_title_dic_list.append(clause_title_token_dic_Okt)
    clause_title_dic_name_list.append("Okt")
    clause_title_token_dic_Komoran = dict()
    clause_title_dic_list.append(clause_title_token_dic_Komoran)
    clause_title_dic_name_list.append("Komoran")
    clause_title_token_dic_Hannanum = dict()
    clause_title_dic_list.append(clause_title_token_dic_Hannanum)
    clause_title_dic_name_list.append("Hannanum")

    for idx,cl_title_file in enumerate(clause_title_files):
        file_name = str(cl_title_file.split('/')[len(cl_title_file.split('/'))-1])
        #print("clause_title_name:",file_name)
        with open(cl_title_file,'r',encoding='utf8') as rdata:
            print("\n",idx+1,"/",len(clause_title_files),"current_file:",cl_title_file,"\n")
            lines = rdata.readlines()
            for line in lines:
                if '"' in line:
                    print("lin")
                line = line.replace('"','')
                line=str(line)
                for idx in range(0,len(line)):
                    if line[idx] == '(':
                        str_idx = idx
                #print(line[str_idx+1:-2])
                cl_title = line[str_idx+1:-2]
                print("\nclause_title:",cl_title)

                results = []
                for name, tagger in pos_taggers:
                    print("\n")
                    current_dic = dict()
                    #print(len(pos_taggers))
                    if name == 'kkma':
                        current_dic = clause_title_token_dic_kkma
                    if name == 'Okt':
                        current_dic = clause_title_token_dic_Okt
                    if name == 'Komoran':
                        current_dic = clause_title_token_dic_Komoran
                    if name == 'Hannanum':
                        current_dic = clause_title_token_dic_Hannanum
                    tokens = []
                    process_time = time.time()
                    text = cl_title
                    # print("text:",text)
                    # text='본 사채 조건에 관한 사항'
                    #tokens.append(tagger.pos(text))
                    tokens.append(tagger.nouns(text))
                    # print("tokens:",tokens)
                    # print("tokens[0]:",tokens[0])
                    tokens = tokens[0]
                    print("tokens:",tokens)
                    process_time = time.time() - process_time
                    print('tagger name = %10s, %.3f secs' % (name, process_time))
                    results.append(tokens)
                    for token in (tokens):
                        #print(token)
                        if token in current_dic:
                            current_dic[str(token)] += 1
                        else:
                            current_dic[token] = 1
    for dic_idx,dic in enumerate(clause_title_dic_list):
        with open(pickle_file_dir+'/'+'clause_title_token_dic_'+clause_title_dic_name_list[dic_idx]+'.pickle','wb') as handle:
            dic =sorted(dic.items(),key=lambda t : t[1])
            print("clause_title_token_dic_"+clause_title_dic_name_list[dic_idx]+":",len(dic), dic)
            pickle.dump(dic,handle,protocol=pickle.HIGHEST_PROTOCOL)
    process_time2 = time.time() - process_time2
    print('morphem_analysis process done. %.3f' % (process_time2))
    return clause_title_dic_list,clause_title_dic_name_list


def visualize(clause_title_dic_list,clause_title_dic_name_list):
    # process_time = time.time()
    font_name = font_manager.FontProperties(fname=font_dir+'/'+'NanumGothic.ttf').get_name()
    mpl.rcParams['axes.unicode_minus'] = False
    rc('font', family=font_name)
    for dic_idx,dic in enumerate(clause_title_dic_list):
        # key = dic.keys()
        # df = pd.DataFrame([dic],index=key)
        # df.drop(df.columns[1:],inplace=True)
        # df.plot(kind='bar')
        # plt.show()
        width = 10.0
        plt.bar(dic.keys(), dic.values(), width)
        plt.title(clause_title_dic_name_list[dic_idx])
        plt.savefig(plot_file_dir+'/'+'fig_'+clause_title_dic_name_list[dic_idx]+'.png',dpi=500)
        plt.show()
        
    # process_time = time.time() - process_time
    # print('visualize process done. %.3f' % (process_time))

if __name__ == "__main__":
    #directory setting
    currentdir = os.getcwd()
    parentdir = os.path.dirname(currentdir)
    font_dir = currentdir+'/Fonts'
    txt_file_dir = currentdir+'/'+"Contract_Dataset"
    txt_files = glob.glob(txt_file_dir+'/*.txt')
    clause_title_file_dir = currentdir+'/Clause_title_Files'
    pickle_file_dir = currentdir+'/Pickle_Files'
    plot_file_dir = currentdir+'/Plot_Files'

    if not(os.path.isdir(font_dir)):
        os.makedirs(os.path.join(font_dir))
    if not(os.path.isdir(clause_title_file_dir)):
        os.makedirs(os.path.join(clause_title_file_dir))
    if not(os.path.isdir(pickle_file_dir)):
        os.makedirs(os.path.join(pickle_file_dir))
    if not(os.path.isdir(plot_file_dir)):
        os.makedirs(os.path.join(plot_file_dir))

    clause_title_files = make_clause_title_files(txt_files)
    #clause_title_files = glob.glob(clause_title_file_dir+'/*_clause_title.txt')

    clause_title_dic = sort_unique_values(clause_title_files)

    clause_title_dic_list,clause_title_dic_name_list = morphem_analysis(clause_title_files)
    visualize(clause_title_dic_list,clause_title_dic_name_list)
