# coding=utf-8

__author__ = 'tianchuang'

# 将原始的A全专利标题与摘要信息进行整合,去除标点符号及英文字母,提取出名词和动词
# A部下的全部84个小类,平均25秒转换一小组数据
# 耗时：1993.134529s

import jieba
import jieba.analyse
import pandas as pd
import re
import time
import jieba.posseg as pseg

time_initial = time.time()


# 读取IPC代码与描述
def read_IPC_code():
    print('开始读取IPC代码与描述')
    ipc_code = pd.read_csv('../../../res/A01/IPC_Comment.csv')
    l_ipc_code = []
    l_ipc = []

    for index, item in ipc_code.iterrows():
        code = item['code']
        # 此处为判断A部下的全部84个小类,可调整
        if code[0:1] == 'A':
            l_ipc_code.append(code)
            code = code + ' ' + item['describe']
            l_ipc.append(code)
            # print(code)
    print(l_ipc_code, '\n读取完毕')
    return l_ipc_code, l_ipc


l_ipc_code, l_ipc = read_IPC_code()

print('创造新的表:')
new_data = pd.DataFrame(columns=('code', 'describe'))
print(new_data)
n_all = ['n', 'nr', 'nr1', 'nr2', 'nrj', 'nrf', 'ns', 'nsf', 'nt', 'nz', 'nl', 'ng']
v_all = ['v']
n_all = n_all + v_all

i = 0
# 读取所有ipc_code
for item in l_ipc_code:
    x = str(item)
    print(x, '开始分词')

    startTime = time.time()

    f = open('../../../res/A/clean/' + x + '.csv', 'r')
    # 读取所有行
    lines = f.readlines()[1:]
    f.close()

    s = ''
    for l in lines:
        l = l.strip()
        l = re.sub(r'([\d])', '', l)
        l = re.sub(r'([a-z])', '', l)

        s = s + l

    words_p = pseg.cut(s)
    word_list = []

    for w, flag in words_p:
        if flag in n_all:
            word_list.append(w)

    new_data.loc[i] = None
    new_data['code'].loc[i] = x
    new_data['describe'].loc[i] = word_list

    print(x, '完成提取关键词')
    print('耗时：%fs!' % (time.time() - startTime))
    i = i + 1

new_data.to_csv('../../../res/A/IPC_A_list_n.csv', index=False, index_label='index')

print('A部专利数据提取完成! 耗时：%fs!' % (time.time() - time_initial))
