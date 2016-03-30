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

startTime = time.time()

# 读取数据
startTime = time.time()
ipc_data = pd.read_csv('../../res/A01/IPC_Comment.csv')
print('数据读取完成! 耗时：%fs!' % (time.time() - startTime))

print('创造新的表:')
i = 0
l = []
for index, item in ipc_data.iterrows():
    code = item['code']

    if code[0:2] == 'A0':
    # if code[0] == 'A':
        print(code)
        l.append(code)
print(l)
print('共有',len(l),'个小类')

# new_data.to_csv('../../res/A01/IPC_Comment.csv', index=False, index_label='index')
print('数据转换完成! 耗时：%fs!' % (time.time() - startTime))
