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
f = open('../../res/A01/IPC_Comment_complete_A01_raw.csv', 'r')
# 读取所有行
lines = f.readlines()[0:]
f.close()
print('数据读取完成! 耗时：%fs!' % (time.time() - startTime))
print('创造新的表:')
new_data = pd.DataFrame(columns=('code', 'describe'))
print(new_data)

l_ipc = ['A01B', 'A01C', 'A01D', 'A01F', 'A01G', 'A01H', 'A01J', 'A01K', 'A01L', 'A01M', 'A01N', 'A01P']

i = 0
ipc_comment = ''
for l in lines:
    l = l.strip()
    # 有可能某一行不到4位的长度,提前加4个空格
    l = l + '    '


    if i < len(l_ipc)-1:

        # 第一步:判断前4位等同第一个小类号,则添加后边的字符串描述信息
        if l[0:4] == l_ipc[i]:
            ipc_code = l_ipc[i]
            ipc_comment = ipc_comment + l[4:]
            ipc_comment = ipc_comment.strip()
            # print(ipc_code,ipc_comment)

        # 第二步:判断前4位等于第二个小类号时,则将数据写入Dataframe,继续下一轮
        if l[0:4] == l_ipc[i + 1]:
            new_data.loc[i] = None
            new_data['code'].loc[i] = l_ipc[i]
            new_data['describe'].loc[i] = ipc_comment
            i += 1
            ipc_comment = ''

    # 第三步:判断前4位等于最后一个小类号时,则特殊处理将数据写入Dataframe,并结束
    if i == len(l_ipc)-1:
        ipc_code = l_ipc[i]
        ipc_comment = ipc_comment + l[4:]
        ipc_comment = ipc_comment.strip()

new_data.loc[i] = None
new_data['code'].loc[i] = l_ipc[i]
new_data['describe'].loc[i] = ipc_comment

print(new_data.head())

new_data.to_csv('../../res/A01/IPC_Comment_complete_A01.csv', index=False, index_label='index')
print('数据转换完成! 耗时：%fs!' % (time.time() - startTime))
