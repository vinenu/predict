#/usr/bin/env python
# _*_ coding:utf-8 _*_

## 首次运行需要解除下面5行注释
# import nltk
# nltk.download('averaged_perceptron_tagger')
# nltk.download('wordnet')
# nltk.download('omw-1.4')
# nltk.download('punkt')

import pandas as pd
import numpy as np
import re
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk import word_tokenize, pos_tag
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from nltk.stem import SnowballStemmer
# from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

## 要找出多少个关键词
top_num = 10

## 用户自己设置的停用词
# user_stop_words = ["word1", "word2", "word3"]

## 数据保存路径
datadir = './xlsx'


## 列出所有非隐藏文件
def filelist(dirname):
    path_list = []
    for name in os.listdir(dirname):
        path = os.path.join(dirname, name)
        if not name.startswith("."):
            if os.path.isfile(path):
                path_list.append(path)
            else:
                filelist(path)
    return path_list

## TFIDF计算
def dfidf_compute(data):
    tfidf_vector = TfidfVectorizer(stop_words='english', analyzer='word', token_pattern=r"(?u)\b[a-zA-Z]\w+\b", use_idf=True, max_df=0.5, min_df=1, ngram_range=(1,3))

    ## 如果需要使用用户设置的停用词
    # tfidf_vector = TfidfVectorizer(stop_words=stop_words, analyzer='word', token_pattern=r"(?u)\b[a-zA-Z]\w+\b", min_df=0.005)
    tfidf_matrix = tfidf_vector.fit_transform(data).toarray()
    word_list = tfidf_vector.get_feature_names_out()

    df = []
    for j in range(len(tfidf_matrix)):
        dic = {}
        for k in range(len(word_list)):
            if tfidf_matrix[j][k] > 0:
                word = word_list[k]
                tfidf = tfidf_matrix[j][k]
                dic[word] = tfidf
        df.append(dic)
    return(df)

## 排序并取top N
def dfidf_sort(df):
    df_sorted = []
    for i in range(len(df)):
        data = sorted(df[i].items(), key=lambda x:x[1], reverse=True)
        data = data[:top_num]
        df_sorted.append(data)
    return df_sorted

# 获取单词的词性
def get_wordnet_pos(tag):
    if tag.startswith('J'):
        return wordnet.ADJ
    elif tag.startswith('V'):
        return wordnet.VERB
    elif tag.startswith('N'):
        return wordnet.NOUN
    elif tag.startswith('R'):
        return wordnet.ADV
    else:
        return None

# ## 结合用户设置的停用词生成新的停用词
# stop_words= []
# for w in ENGLISH_STOP_WORDS:
#     stop_words.append(w)
# for w in user_stop_words:
#     stop_words.append(w)

## 读取文件并处理
snowball_stemmer = SnowballStemmer("english")
wordnet_lemmatizer = WordNetLemmatizer()
for file in filelist(datadir):
    data = pd.read_excel(file, 'Sheet1')
    contents = data['Content']
    new_contents = []

    ## 预处理去除一些文字
    for i in range(len(contents)):
        try:
            content = re.sub(r""" \(C\) \d{4} Elsevier .* All rights reserved\.""", "", contents[i], count=0, flags=re.I)
            content = re.sub(r"NOVELTY|USE|ADVANTAGE|DETAILED DESCRIPTION|DESCRIPTION OF DRAWING", "", content, count=0)
        except:
            content = ""
        
        ## 词形还原
        tokens = word_tokenize(content)   # 分词
        tagged_sent = pos_tag(tokens)     # 获取单词词性
        lemmas_sent = []
        for tag in tagged_sent:
            wordnet_pos = get_wordnet_pos(tag[1]) or wordnet.NOUN
            lemmas_sent.append(wordnet_lemmatizer.lemmatize(tag[0], pos=wordnet_pos)) # 词形还原
        
        ## 词干提取
        new_content = ""
        for word in lemmas_sent:
            try:
                new_word = snowball_stemmer.stem(word) # 词干提取
                # new_word = word    # 词干不提取
                new_content = new_content + " " + new_word
            except:
                new_content = ""

        ## 新的 Content 列表
        new_contents.append(new_content.strip())

    ## 计算TFIDF
    dfidf_dataframe = dfidf_compute(new_contents)
    dfidf_dataframe_sorted = dfidf_sort(dfidf_dataframe)
    data['TopTFIDF'] = dfidf_dataframe_sorted

    ## 切片TFIDF最高的单词
    top_word_df = []
    for j in range(len(dfidf_dataframe_sorted)):
        top_word = ""
        for k in range(len(dfidf_dataframe_sorted[j])):
            try:
                top_word = top_word + ';' + dfidf_dataframe_sorted[j][k][0]
            except:
                top_word = ""
        top_word = re.sub(r";", "", top_word.strip(), count=1)
        top_word_df.append(top_word)
    data['TopWord'] = top_word_df

    ## 写入新文件
    new_file = re.sub(r"./xlsx", "./result", file)
    pd.DataFrame(data).to_excel(new_file, sheet_name='Sheet1', index=False, header=True)

