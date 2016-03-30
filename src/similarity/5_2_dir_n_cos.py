# coding=utf-8
__author__ = 'tianchuang'

# 相似度计算,直接将所有专利数据分词,并只保留名词,产业类目用已提取的100关键词,一个专利小组数据约耗时30秒  字典的大小:34508

from gensim import corpora, models, similarities
import jieba
import jieba.posseg as pseg

import numpy as np
import re
import pandas as pd
import time

jieba.initialize()

# python2.7 则需要以下转码
# import sys
# reload(sys)
# sys.setdefaultencoding("utf-8")

time_initial = time.time()

# ind = pd.read_csv('../../res/Industry/GMJJHY_OK_all_list.csv', dtype=str)
ind = pd.read_csv('../../res/Industry/GMJJHY_OK_A_list.csv', dtype=str)

# ipc = pd.read_csv('../../res/IPC_OK.csv', dtype={'code': str, 'describe': list})


print(ind.head())

words = []
sentences = []
l_ipc = ['A01B', 'A01C', 'A01D', 'A01F', 'A01G', 'A01H', 'A01J', 'A01K', 'A01L', 'A01M', 'A01N', 'A01P']

# 读取数据 1到n 的数字(12)
for i in range(0, 12):

    x = str(l_ipc[i])

    print(x, '开始分词')

    startTime = time.time()

    f = open('../../res/A01/clean/' + x + '.csv', 'r')
    # 读取所有行
    lines = f.readlines()[1:]
    f.close()

    s = ''
    for l in lines:
        l = l.strip()
        l = re.sub(r'([\d])', '', l)
        l = re.sub(r'([a-z])', '', l)

        s = s + l
    sentences.append(s)
    print('转换完成')
    print('耗时：%fs!' % (time.time() - startTime))

for doc in sentences:
    words_p = pseg.cut(doc)
    word_list = []
    for w, flag in words_p:

        if flag == 'n':
            # print('%s %s' % (word, flag))
            word_list.append(w)
            # print(word)

    words.append(word_list)
# print('分词结果:\n', (words))

# print(words)

dic = corpora.Dictionary(words)

print('字典:\n', (dic))
# print('词或词组在字典中的编号:\n', (dic.token2id))
print('字典的大小:\n', (len(dic)))
len_dict = len(dic)

corpus = [dic.doc2bow(text) for text in words]
# print('向量空间模型格式的语料库:\n', (corpus))


tfidf = models.TfidfModel(corpus)

corpus_tfidf = tfidf[corpus]

index = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features=len_dict)

print('创造新的表:')
new_data = pd.DataFrame(columns=(
'industry', 'A01B', 'A01C', 'A01D', 'A01F', 'A01G', 'A01H', 'A01J', 'A01K', 'A01L', 'A01M', 'A01N', 'A01P'))
new_data_index = 1
print(new_data)

for index_ind, row in ind.iterrows():
    # if index_ind == 1:
    #     break
    print(row['code'])
    new_data.loc[new_data_index] = None
    new_data['industry'].loc[new_data_index] = row['code']

    query = row['describe']
    query = re.sub(r'([\[\]\' ])', '', query)
    query = query.split(',')

    query_bow = dic.doc2bow(query)
    # print('查询词为:\n', query)
    # print('改为向量空间格式:\n', (query_bow))

    sims = index[tfidf[query_bow]]
    # print('比较查询词和训练中的专利类目的相似度:\n', list(enumerate(sims)))
    # sort_sims = sorted(enumerate(sims), key=lambda item: -item[1])
    # print('排序:比较查询词和训练中的专利类目的相似度:\n',(sort_sims))
    norm_sims = list(enumerate(sims))
    print('非排序:比较查询词和训练中的专利类目的相似度:\n', (norm_sims))
    words = []
    for code, sim in norm_sims:
        # print(code)
        # print(sim)
        words.append(sim)
    # print(words)

    # 读取数据 1到n 的数字
    for i in range(0, 12):
        new_data[l_ipc[i]].loc[new_data_index] = words[i - 1]

    new_data_index += 1
    # print(sort_sims[0:1])
new_data.to_csv('../../out/cos_dir_n.csv', index=False, index_label='index')

print('数据转换完成! 耗时：%fs!' % (time.time() - time_initial))
