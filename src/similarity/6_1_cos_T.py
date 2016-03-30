# coding=utf-8
__author__ = 'tianchuang'

# 将相似度矩阵 行与列转置


import pandas as pd
import time

# python2.7 则需要以下转码
# import sys
# reload(sys)
# sys.setdefaultencoding("utf-8")

time_initial = time.time()

cos_data = pd.read_csv('../../out/cos_dir.csv', dtype={'industry': str})

print(cos_data.head())

cos_data_T = cos_data.T

print(cos_data_T.head())

cos_data_T.to_csv('../../out/cos_dir_T.csv')

print('数据转换完成! 耗时：%fs!' % (time.time() - time_initial))
