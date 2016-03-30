# coding=utf-8
__author__ = 'tianchuang'

# 将原始的国民经济行业分类表,提取出代码为三位数的类别名称
# 011	  谷物种植
# 012	  豆类、油料和薯类种植
# 013	  棉、麻、糖、烟草种植

import pandas as pd
import time
import re

# 读取数据
startTime = time.time()
f = open('../../res/Industry/GMJJHY.csv', 'r')
# 读取所有行
lines = f.readlines()[1:]
f.close()
print('数据读取完成! 耗时：%fs!' % (time.time() - startTime))

print('创造新的表:')
new_data = pd.DataFrame(columns=('code', 'describe'))
print(new_data)

i = 0

for l in lines:
    l = l.strip()
    l_list = l.split(',')
    if len(l_list[0]) == 3:
        ind_code = l_list[0]
        s = ''
        if len(l_list[1]) == 4:
            l_list[1] = ''
        for item in l_list[1:]:
            s = s + item
        print(ind_code, s)
        new_data.loc[i] = None
        new_data['code'].loc[i] = ind_code
        new_data['describe'].loc[i] = s
        i += 1

print(new_data.head())

new_data.to_csv('../../res/Industry/GMJJHY_Comment.csv', index=False, index_label='index')
print('数据转换完成! 耗时：%fs!' % (time.time() - startTime))
