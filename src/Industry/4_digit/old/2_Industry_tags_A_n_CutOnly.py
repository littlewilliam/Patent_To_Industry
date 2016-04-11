# coding=utf-8
__author__ = 'tianchuang'

# 将原始的国民经济行业分类表,进行第二次规整,分词,取名词
# n 名词
# nr 人名
# nr1 汉语姓氏
# nr2 汉语名字
# nrj 日语人名
# nrf 音译人名
# ns 地名
# nsf 音译地名
# nt 机构团体名
# nz 其它专名
# nl 名词性惯用语
# ng 名词性语素
# code,describe
# 0111,"[稻谷, 稻谷, 早籼稻, 种用, 早籼稻, 早籼稻, 籼稻, 籼稻, 籼稻, 籼稻, 种用, 籼稻, 籼稻, 粳稻, 种用, 粳稻, 粳稻, 糯稻, 种用, 糯稻, 糯稻, 稻谷, 稻谷, 壳, 稻谷, 秸, 列明, 稻谷]"
# 0112,"[小麦, 小麦, 硬质小麦, 种用, 硬质小麦, 硬质小麦, 软质, 小麦, 种用, 软质, 小麦, 软质, 小麦, 小麦, 种用, 小麦, 小麦, 小麦, 麦秸, 列明, 小麦]"
# 0113,"[玉米, 玉米, 玉米, 种用, 白, 玉米, 玉米, 黄玉米, 种用, 黄玉米, 黄玉米, 糯玉米, 种用, 糯玉米, 糯玉米, 甜玉米, 种用, 甜玉米, 甜玉米, 玉米, 玉米秸, 列明, 玉米]"

import jieba
import jieba.analyse
import pandas as pd
import time
import jieba.posseg as pseg

time_initial = time.time()

# 读取数据
startTime = time.time()
ind_data = pd.read_csv('../../../res/Industry/4_digit/GMJJHY_OK_4.csv', dtype=str)
print('数据读取完成! 耗时：%fs!' % (time.time() - startTime))
print(ind_data.head())

print('创造新的表:')
new_data = pd.DataFrame(columns=('code', 'describe'))
print(new_data)

i = 0
n_all = ['n', 'nr', 'nr1', 'nr2', 'nrj', 'nrf', 'ns', 'nsf', 'nt', 'nz', 'nl', 'ng']
# v_all=['v']
# n_all=n_all+v_all

for index, row in ind_data.iterrows():
    if int(row['code'] )>540:
        break
    new_data.loc[i] = None
    new_data['code'].loc[i] = row['code']
    # cut = list(jieba.cut(row['describe']))
    word_list = list(jieba.analyse.extract_tags(row['describe'], withWeight=False))

    new_data['describe'].loc[i] = word_list

    i += 1

print(new_data.head())

new_data.to_csv('../../../res/Industry/4_digit/GMJJHY_OK_A_n_list_4.csv', index=False,encoding='utf-8')
print('数据转换完成! 耗时：%fs!' % (time.time() - startTime))
