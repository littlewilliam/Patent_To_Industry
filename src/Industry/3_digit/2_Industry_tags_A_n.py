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
# 011,"[谷物, 籽实, 人类, 食用, 农作物, 稻谷, 小麦, 玉米, 农作物, 稻谷, 稻谷, 早籼稻, 种用, 早籼稻, 早籼稻, 籼稻, 籼稻, 籼稻, 籼稻, 种用, 籼稻, 籼稻, 粳稻, 种用, 粳稻, 粳稻, 糯稻, 种用, 糯稻, 糯稻, 稻谷, 稻谷, 壳, 稻谷, 秸, 列明, 稻谷, 小麦, 小麦, 硬质小麦, 种用, 硬质小麦, 硬质小麦, 软质, 小麦, 种用, 软质, 小麦, 软质, 小麦, 小麦, 种用, 小麦, 小麦, 小麦, 麦秸, 列明, 小麦, 玉米, 玉米, 玉米, 种用, 白, 玉米, 玉米, 黄玉米, 种用, 黄玉米, 黄玉米, 糯玉米, 种用, 糯玉米, 糯玉米, 甜玉米, 种用, 甜玉米, 甜玉米, 玉米, 玉米秸, 列明, 玉米, 谷物, 谷物, 谷子, 谷子, 糯, 谷子, 谷子, 高粱, 红粒, 高粱, 种用, 红粒, 高粱, 红粒, 高粱, 白粒, 高粱, 种用, 白粒, ...]"
# 012,"[豆类, 油料, 薯类, 豆类, 豆类, 大豆, 黄大豆, 大豆, 青, 大豆, 红, 大豆, 双, 青豆, 青仁乌, 豆, 黑豆, 大豆, 绿豆, 绿豆, 绿豆, 绿豆, 毛, 绿豆, 种用, 毛, 绿豆, 毛, 绿豆, 小豆, 红小豆, 小豆, 狸, 小豆, 小豆, 豌豆, 豌豆, 种用, 白, 豌豆, 豌豆, 豌豆, 种用, 绿, 豌豆, 豌豆, 麻, 豌豆, 种用, 麻, 豌豆, 麻, 豌豆, 蚕豆, 种用, 干, 蚕豆, 蚕豆, 芸豆, 种用, 芸豆, 芸豆, 饭豆, 种用, 饭豆, 饭豆, 豇豆, 种用, 干, 豇豆, 豇豆, 鹰嘴豆, 种用, 鹰嘴豆, 鹰嘴豆, 豆类蔬菜, 部分, 豌豆, 蚕豆, 豆秸, 杂豆, 种用, 杂豆, 列明, 杂豆, 油料, 油料, 花生, 壳, 花生, 种用, 壳, 花生, 壳, 花生, 花生仁, 油菜籽, 油菜籽, 油菜籽, 油菜籽, ...]"
# 013,"[棉, 麻, 烟草, 棉花, 棉花, 籽棉, 棉花, 秆, 棉花, 麻类, 麻类, 亚麻, 苎麻, 黄红麻, 线麻, 苘麻, 大麻, 剑麻, 麻秆, 生麻, 糖料, 指, 制糖, 甘蔗, 甜菜, 糖料, 甘蔗, 甜菜, 糖料, 烟草, 烟草, 烟叶, 烟叶, 烟叶, 肋烟, 烟秆, 未加工, 烟草]"

import jieba
import jieba.analyse
import pandas as pd
import time
import jieba.posseg as pseg

time_initial = time.time()

# 读取数据
startTime = time.time()
ind_data = pd.read_csv('../../../res/Industry/GMJJHY_OK.csv', dtype=str)
print('数据读取完成! 耗时：%fs!' % (time.time() - startTime))
print(ind_data.head())

print('创造新的表:')
new_data = pd.DataFrame(columns=('code', 'describe'))
print(new_data)

i = 0
n_all = ['n', 'nr', 'nr1', 'nr2', 'nrj', 'nrf', 'ns', 'nsf', 'nt', 'nz', 'nl', 'ng']
for index, row in ind_data.iterrows():
    if int(row['code'] )>54:
        break
    new_data.loc[i] = None
    new_data['code'].loc[i] = row['code']
    # cut = list(jieba.cut(row['describe']))
    words_p = pseg.cut(row['describe'])
    word_list = []
    for w, flag in words_p:
        # print('未判断:')
        # print('%s %s' % (w, flag))

        if flag in n_all:
            # print('判断是否为n后:')
            # print('%s %s' % (w, flag))
            word_list.append(w)
            # print(word)

    new_data['describe'].loc[i] = word_list

    i += 1

print(new_data.head())

new_data.to_csv('../../res/Industry/GMJJHY_OK_A_n_list.csv', index=False,encoding='utf-8')
print('数据转换完成! 耗时：%fs!' % (time.time() - startTime))
