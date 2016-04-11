# coding=utf-8

__author__ = 'tianchuang'

# 处理IPC类目,提取出所有词(名词+动词 等,抽取关键词方法:jieba.extract_tags)

import jieba
import jieba.analyse
import pandas as pd
import re
import time
import jieba.posseg as pseg

time_initial = time.time()

l_ipc = ['A01B', 'A01C', 'A01D', 'A01F', 'A01G', 'A01H', 'A01J', 'A01K', 'A01L', 'A01M', 'A01N', 'A01P']

print('创造新的表:')
new_data = pd.DataFrame(columns=('code', 'describe'))
print(new_data)
n_all = ['n', 'nr', 'nr1', 'nr2', 'nrj', 'nrf', 'ns', 'nsf', 'nt', 'nz', 'nl', 'ng']
# v_all=['v']
# n_all=n_all+v_all
ipc_comment_data = pd.read_csv('../../res/A01/IPC_Comment_complete_A01.csv')

i = 0
for index, item in ipc_comment_data.iterrows():
    startTime = time.time()
    print(item['code'])
    word_list = list(jieba.analyse.extract_tags(item['describe'], withWeight=False))

    new_data.loc[i] = None
    new_data['code'].loc[i] = item['code']
    new_data['describe'].loc[i] = word_list
    i += 1

    print(item['code'], '转换完成')
    print('耗时：%fs!' % (time.time() - startTime))

    if item['code'] == 'A01P':
        break

new_data.to_csv('../../res/A01/IPC_Comment_complete_A01_list_n.csv', index=False, index_label='index')

print('完成! 耗时：%fs!' % (time.time() - time_initial))
