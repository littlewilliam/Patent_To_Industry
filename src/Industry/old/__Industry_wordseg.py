# coding=utf-8
__author__ = 'tianchuang'

# 无用,废弃
# 将原始的国民经济行业分类表,进行第二次规整,调整格式为
# code,describe
# A,农|、|林|、|牧|、|渔业|本|门类|包括|～|大|类|。
# 01,农业|指对|各种|农作物|的|种植|。

import pandas as pd
import time
import re
import jieba

# python2.7 则需要以下转码
# import sys
# reload(sys)
# sys.setdefaultencoding( "utf-8" )


time_initial = time.time()

# 读取数据
startTime = time.time()
ind_data = pd.read_csv('../../res/GMJJHY_OK.csv')
print('数据读取完成! 耗时：%fs!' % (time.time() - startTime))

print('创造新的表:')
new_data = pd.DataFrame(columns=('code', 'describe'))
print(new_data)

i = 0
for index, row in ind_data.iterrows():
    if index == 10:
        break

    c = str(row['describe'])

    c = jieba.cut(c, cut_all=False)
    c = str("|".join(c))

    new_data.loc[i] = None
    new_data['code'].loc[i] = row['code']
    new_data['describe'].loc[i] = c
    i += 1

print(new_data.head())
print('全部数据分词完成! 耗时：%fs!' % (time.time() - startTime))

# new_data.to_csv('../../res/GMJJHY_OK_SEG.csv', index=False, index_label='index')
