# coding=utf-8

__author__ = 'tianchuang'

# 将原始的A01小组下全专利信息进行规整,仅提取有用的专利标题与摘要信息

# python 2.7.11
# python2.7 则需要以下转码
# import sys
# reload(sys)
# sys.setdefaultencoding( "utf-8" )

import pandas as pd
import time

startTime = time.time()

# 5000条以内的专利数据直接以GBK解码
l = ['A01B', 'A01C', 'A01D', 'A01F',  'A01H', 'A01J', 'A01K', 'A01L', 'A01M',  'A01P']
# 读取数据 1到n 的数字
for i in range(0, 10):
    x=str(l[i])
    ipc_data = pd.read_csv('../../res/A01/original/'+x+'.csv', encoding="GBK")
    # print(ipc_data.head())

    ipc_data_final = ipc_data[['名称', '摘要']]
    # print(ipc_data_final.head())


    ipc_data_final.to_csv('../../res/A01/clean/'+x+'.csv',index=False,encoding='utf-8')
    print(x, '提取完成')

print('5000以内专利数据提取完成! 耗时：%fs!' % (time.time() - startTime))


# 超过5000条的专利数据因由excel重新拼接,解码需更改为utf-8
l2 = ['A01G', 'A01N']
# 读取数据 1到n 的数字
for i in range(0, 2):
    x = str(l2[i])
    ipc_data = pd.read_csv('../../res/A01/original/' + x + '.csv', encoding="utf-8")
    # print(ipc_data.head())

    ipc_data_final = ipc_data[['名称', '摘要']]
    # print(ipc_data_final.head())
    ipc_data_final.to_csv('../../res/A01/clean/' + x + '.csv', index=False, encoding='utf-8')
    print(x, '提取完成')

print('5000以上专利数据提取完成! 耗时：%fs!' % (time.time() - startTime))
