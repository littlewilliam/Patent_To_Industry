# coding=utf-8
__author__ = 'tianchuang'

# 相似度计算,专利数据已按照小类各提取出所有名词,产业类目也已提取出所有名词
# <查询词>:专利数据[26000条专利](A01大组共12个小类)
# <语料库>:产业描述文字(全1094),可以仅提取前60个类目
# 不需要转置

from gensim import corpora, models, similarities
import re
import pandas as pd
import time
# python2.7 则需要以下转码
# import sys
# reload(sys)
# sys.setdefaultencoding("utf-8")

time_initial = time.time()

ind = pd.read_csv('../../../res/Industry/4_digit/GMJJHY_OK_all_n_list_4.csv', dtype=str)
ipc = pd.read_csv('../../../res/A01/IPC_list_n.csv')

print(ind.head())
print(ipc.head())

words = []
for index, row in ind.iterrows():
    # print(row['code'])
    des = row['describe']
    des = re.sub(r'([\[\]\' ])', '', des)
    des = des.split(',')
    words.append(des)

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


# 读取IPC代码与描述
def read_IPC_code():
    print('开始读取IPC代码与描述')
    ipc_code = pd.read_csv('../../../res/A01/IPC_Comment.csv')
    l_ipc_code = []
    l_ipc = []

    for index, item in ipc_code.iterrows():
        code = item['code']
        # 此处为判断A0大类下的全部12个小类,可调整
        if code[0:2] == 'A0':
            l_ipc_code.append(code)
            code = code + ' ' + item['describe']
            l_ipc.append(code)
            # print(code)
    print(l_ipc_code,'\n读取完毕')
    return l_ipc_code, l_ipc
    # l_ipc_code = ['A01B', 'A01C', 'A01D', 'A01F', 'A01G', 'A01H', 'A01J', 'A01K', 'A01L', 'A01M', 'A01N', 'A01P']

l_ipc_code, l_ipc = read_IPC_code()


# 读取产业类目代码与描述
def read_ind_code():
    print('开始读取产业代码与描述')

    ind_code = pd.read_csv('../../../res/Industry/4_digit/GMJJHY_Comment_4.csv', dtype=str)
    l_ind_code = []
    l_ind = []

    for index, item in ind_code.iterrows():
        code_str = str(item['code'])
        code = int(item['code'])
        # 此处为判断A	农、林、牧、渔业类目下的所有4位精度的国民经济行业类目,可调整
        # if code <= 540:
        if code <= 9600:

            l_ind_code.append(code_str)
            code_str = code_str + ' ' + item['describe']
            l_ind.append(code_str)
            # print(code_str)
    print(l_ind_code, '\n读取完毕')

    return l_ind_code, l_ind

l_ind_code, l_ind = read_ind_code()

column_name = ['patent']
column_name=column_name+l_ind_code
column_name_new=['patent']
column_name_new=column_name_new+l_ind

print('创造新的表:')
new_data = pd.DataFrame(columns=column_name_new)
new_data_index = 1
print(new_data)

for index_ind, row in ipc.iterrows():
    # if index_ind == 1:
    #     break
    # print(row['code'])
    new_data.loc[new_data_index] = None
    new_data['patent'].loc[new_data_index] = l_ipc[new_data_index-1]

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
    # print('非排序:比较查询词和训练中的专利类目的相似度:\n', (norm_sims))
    words = []
    for code, sim in norm_sims:
        # print(code)
        # print(sim)
        words.append(sim)
    # print(words)

    # 读取数据 1到n 的数字
    for i in range(0, len(l_ind)):
        new_data[l_ind[i]].loc[new_data_index] = words[i - 1]

    new_data_index += 1
    # print(sort_sims[0:1])


# new_data = new_data.rename(columns={column_name: column_name_new})

new_data.to_csv('../../../out/4_digit/p2i/cos_A01_all.csv', index=False, encoding='gbk')

print('数据转换完成! 耗时：%fs!' % (time.time() - time_initial))
