# coding=utf-8

__author__ = 'tianchuang'

# 将原始的IPC注释进行规整,提取所有小类的描述信息,IPC代码为四位数,A部有84个小类

# python 2.7.11
# python2.7 则需要以下转码
# import sys
# reload(sys)
# sys.setdefaultencoding( "utf-8" )

import pandas as pd
import time
import re

#读取产业类目代码与描述
ind_code = pd.read_csv('../../res/Industry/GMJJHY_Comment.csv', dtype=str)
l_ind_code = []
l_ind = []

for index, item in ind_code.iterrows():
    code_str=str(item['code'])
    code = int(item['code'])
    if code <= 54:
        print(code_str)
        l_ind_code.append(code_str)
        code_str = code_str + ' ' + item['describe']
        l_ind.append(code_str)

print(l_ind)
print('共有', len(l_ind), '分类')
print(l_ind_code)
l_a=['industry']
l_a=l_a+l_ind_code
print(l_a)

# new_data.to_csv('../../res/A01/IPC_Comment.csv', index=False, index_label='index')
