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
# 011,"['种用', '高粱', '小麦', '籼稻', '大麦', '稻谷', '糯玉米', '谷子', '甜玉米', '谷物', '硬质小麦', '糯稻', '白粒',
# 012,"['种用', '豌豆', '油菜籽', '绿豆', '小豆', '芝麻', '白芝麻', '木薯', '饭豆', '花生', '蚕豆', '杂豆', '鹰嘴豆', '
# 013,"['糖料', '烟草', '棉花', '烟叶', '麻类', '甜菜', '甘蔗', '未加工', '籽棉', '线麻', '肋烟', '烟秆', '生麻', '麻秆'

import jieba
import jieba.analyse
import pandas as pd
import time
import jieba.posseg as pseg

time_initial = time.time()

# 读取数据
startTime = time.time()
ind_data = pd.read_csv('../../res/Industry/GMJJHY_OK_A.csv', dtype=str)
print('数据读取完成! 耗时：%fs!' % (time.time() - startTime))
print(ind_data.head())

print('创造新的表:')
new_data = pd.DataFrame(columns=('code', 'describe'))
print(new_data)

i = 0
n_all = ['n', 'nr', 'nr1', 'nr2', 'nrj', 'nrf', 'ns', 'nsf', 'nt', 'nz', 'nl', 'ng']
for index, row in ind_data.iterrows():
    # if i == 2:
    #     break
    new_data.loc[i] = None
    new_data['code'].loc[i] = row['code']
    # cut = list(jieba.cut(row['describe']))
    words_p = pseg.cut(row['describe'])
    word_list = []
    for w, flag in words_p:
        print('未判断:')
        print('%s %s' % (w, flag))

        if flag in n_all:
            print('判断是否为n后:')
            print('%s %s' % (w, flag))
            word_list.append(w)
            # print(word)

    new_data['describe'].loc[i] = word_list

    i += 1

print(new_data.head())

new_data.to_csv('../../res/Industry/GMJJHY_OK_A_n_list.csv', index=False, index_label='index')
print('数据转换完成! 耗时：%fs!' % (time.time() - startTime))
