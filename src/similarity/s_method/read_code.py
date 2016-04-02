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
