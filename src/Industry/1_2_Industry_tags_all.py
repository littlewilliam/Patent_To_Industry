# coding=utf-8
__author__ = 'tianchuang'

# 将原始的国民经济行业分类表,进行第二次规整,通过TF-IDF方法抽取名词关键词,全类目
# code,describe
# 011,"['种用', '高粱', '小麦', '籼稻', '大麦', '稻谷', '糯玉米', '谷子', '甜玉米', '谷物', '硬质小麦', '糯稻', '白粒',
# 012,"['种用', '豌豆', '油菜籽', '绿豆', '小豆', '芝麻', '白芝麻', '木薯', '饭豆', '花生', '蚕豆', '杂豆', '鹰嘴豆', '
# 013,"['糖料', '烟草', '棉花', '烟叶', '麻类', '甜菜', '甘蔗', '未加工', '籽棉', '线麻', '肋烟', '烟秆', '生麻', '麻秆'

import jieba
import jieba.analyse
import pandas as pd
import time

time_initial = time.time()

# 读取数据
startTime = time.time()
ind_data = pd.read_csv('../../res/Industry/GMJJHY_OK_all.csv',dtype=str)
print('数据读取完成! 耗时：%fs!' % (time.time() - startTime))
print(ind_data.head())

print('创造新的表:')
new_data = pd.DataFrame(columns=('code', 'describe'))
print(new_data)

i = 0
for index, row in ind_data.iterrows():
    new_data.loc[i] = None
    new_data['code'].loc[i] = row['code']
    # cut = list(jieba.cut(row['describe']))
    cut = list(jieba.analyse.extract_tags(row['describe'], topK=100, withWeight=False, allowPOS=('n')))
    new_data['describe'].loc[i] = cut

    i += 1

print(new_data.head())


new_data.to_csv('../../res/Industry/GMJJHY_OK_all_list.csv',index=False,index_label='index')
print('数据转换完成! 耗时：%fs!' % (time.time() - startTime))
