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

cos_data = pd.read_csv('../../../out/4_digit/p2i/cos_A01_all.csv', encoding='gbk', dtype={'industry': str})

# print(cos_data.head())

cos_data_T = cos_data.T
print('横竖转置完成')

# print (cos_data_T.head())
cos_data_T.to_csv('../../../out/4_digit/p2i/cos_all_A01.csv', encoding='gbk')


# 去除因索引而多出的第一行
def drop_1_row():
    print('去除因转置,而新增的无效第一行')
    f = open('../../../out/4_digit/p2i/cos_all_A01.csv', 'r', encoding='gbk')
    # 读取第1行(不包括)之后所有行
    lines = f.readlines()[1:]
    f.close()

    f = open('../../../out/4_digit/p2i/cos_all_A01.csv', 'w', encoding='gbk')
    for l in lines:
        f.write(l)
    f.close()
drop_1_row()

print('数据转换完成! 耗时：%fs!' % (time.time() - time_initial))
