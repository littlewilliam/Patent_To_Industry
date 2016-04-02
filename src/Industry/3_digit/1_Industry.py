# coding=utf-8
__author__ = 'tianchuang'

# 将原始的国民经济行业分类表,进行第一次规整,调整格式为
# 需要python2.7
# code,describe
#    code                                           describe
# 0   011  谷物种植,指以收获籽实为主，供人类食用的农作物的种植，如稻谷、小麦、玉米等农作物的种植。,稻...
# 1   012  豆类、油料和薯类种植,豆类种植,包括对下列豆类的种植活动：,—,大豆：黄大豆、黑大豆、青大豆...
# 2   013  棉、麻、糖、烟草种植,棉花种植,包括对下列棉花的种植活动：,—,籽棉；—,棉花秆；—,其他棉...


import pandas as pd
import time
import re

time_initial = time.time()

# 读取数据
startTime = time.time()
ind_data = pd.read_csv('../../../res/Industry/GMJJHY.csv')
print('数据读取完成! 耗时：%fs!' % (time.time() - startTime))

# 规整数据
print('原数据:')
print(ind_data.head())

print('仅提取有效数据后:')
ind_data = ind_data[['C1', 'C4', 'C5']]
print(ind_data.head())

# 创造新的表

print('创造新的表:')
new_data = pd.DataFrame(columns=('code', 'describe'))
print(new_data)

i = 0
n = 1
for index, row in ind_data.iterrows():
    # if index == 500:
    #     break
    if n == 1:

        if row['C1'] > 0:
            if len(row['C1']) == 3:
                # print(row['C1'])
                # print(len(row['C1']))

                # print('索引: {}'.format(index))
                # print('读取到的数据  C1: {}; Des1: {}; Des2: {}'.format(row['C1'], row['C4'], row['C5']))

                new_data.loc[i] = None
                new_data['code'].loc[i] = row['C1']

                des = str(row['C4']) + ',' + (str(row['C5']))
                des = re.sub('nan', '', des)
                # des = re.sub('[、，。：—；～]', '', des)
                des = re.sub('[0123456789]', '', des)
                new_data['describe'].loc[i] = des

                # print new_data.loc[i]

                i += 1
                n = 0

    else:
        if row['C1'] > 0:
            if len(row['C1']) == 3:
                # print(row['C1'])
                # print(len(row['C1']))

                new_data.loc[i] = None
                new_data['code'].loc[i] = row['C1']

                des = str(row['C4']) + ',' + (str(row['C5']))
                des = re.sub('nan', '', des)
                # des = re.sub('[、，。：—；～]', '', des)
                des = re.sub('[0123456789]', '', des)
                new_data['describe'].loc[i] = des

                # print new_data.loc[i]

                i += 1
                n = 0


        else:
            des1 = str(row['C4']) + ',' + (str(row['C5']))
            des1 = re.sub('nan', '', des1)
            des1 = re.sub('[0123456789]', '', des1)

            i -= 1
            new_data['describe'].loc[i] = new_data['describe'].loc[i] + des1
            i += 1

print('最终的数据')
print(new_data.describe())

print('全部数据转换完成! 耗时：%fs!' % (time.time() - startTime))

new_data.to_csv('../../res/Industry/GMJJHY_OK.csv',index=False,encoding='utf-8')
