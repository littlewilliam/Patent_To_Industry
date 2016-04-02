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
f = open('../../res/A01/IPC_Comment_raw.csv', 'r')
# 读取所有行
lines = f.readlines()[0:]
f.close()
print('数据读取完成! 耗时：%fs!' % (time.time() - startTime))


print('创造新的表:')
new_data = pd.DataFrame(columns=('code', 'describe'))
print(new_data)

i = 0

for l in lines:
    l = l.strip()
    #有可能某一行不到4位的长度,提前加4个空格
    l = l + '    '
    if l[3].isupper():
        ipc_code = l[0:4]
        ipc_comment = l[4:]
        ipc_comment = ipc_comment[0:-7]
        ipc_comment = ipc_comment.strip()
        # print(ipc_code,ipc_comment)
        new_data.loc[i] = None
        new_data['code'].loc[i] = ipc_code
        new_data['describe'].loc[i] = ipc_comment
        i += 1

print(new_data.head())

new_data.to_csv('../../res/A01/IPC_Comment.csv', index=False, index_label='index')
print('数据转换完成! 耗时：%fs!' % (time.time() - startTime))
