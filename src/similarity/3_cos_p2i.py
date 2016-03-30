# coding=utf-8
__author__ = 'tianchuang'

# 相似度计算,专利数据已按照小类各提取出所有名词,产业类目也已提取出所有名词

from gensim import corpora, models, similarities
import re
import pandas as pd
import time


# python2.7 则需要以下转码
# import sys
# reload(sys)
# sys.setdefaultencoding("utf-8")

time_initial = time.time()

ind = pd.read_csv('../../res/Industry/GMJJHY_OK_all_n_list.csv', dtype=str)
ipc = pd.read_csv('../../res/A01/IPC_list_n.csv')

print(ind.head())
print(ipc.head())

words = []
l_ind=[]
l_ind_d=['IPC']

for index, row in ind.iterrows():
    print(row['code'])
    des = row['describe']
    des = re.sub(r'([\[\]\' ])', '', des)
    des = des.split(',')
    words.append(des)
    l_ind.append(row['code'])
    l_ind_d.append(row['code'])

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
new_data = pd.DataFrame(columns=l_ind_d)
new_data_index = 1
print(new_data)

# l_ipc = ['A01B', 'A01C', 'A01D', 'A01F', 'A01G', 'A01H', 'A01J', 'A01K', 'A01L', 'A01M', 'A01N', 'A01P']

for index_ind, row in ipc.iterrows():
    # if index_ind == 1:
    #     break
    print(row['code'])
    new_data.loc[new_data_index] = None
    new_data['IPC'].loc[new_data_index] = row['code']

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
    len_ind=len(l_ind)
    for i in range(0, len_ind):
        new_data[l_ind[i]].loc[new_data_index] = words[i - 1]

    new_data_index += 1
    # print(sort_sims[0:1])
new_data.to_csv('../../out/cos_p2i.csv', index=False, index_label='index')

print('数据转换完成! 耗时：%fs!' % (time.time() - time_initial))
