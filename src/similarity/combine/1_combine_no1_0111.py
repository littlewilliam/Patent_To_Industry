# coding=utf-8
__author__ = 'tianchuang'

# 相似度计算,专利数据已按照小类各提取出所有名词,产业类目也已提取出所有名词

from gensim import corpora, models, similarities
import re
import pandas as pd
import time
from combine_method import *
from scipy.stats import zscore

# python2.7 则需要以下转码
# import sys
# reload(sys)
# sys.setdefaultencoding("utf-8")

time_initial = time.time()

# 读取IPC代码与描述
l_ipc_code, l_ipc = read_IPC_code()

# 读取产业类目代码与描述
l_ind_code, l_ind = read_ind_code()

column_show = ['p_code'] + l_ind[0:2]
column_show = ['p_code'] + l_ind[0:1]

d = {l_ind[0]: ['A01C', 'A01D', 'A01G', 'A01H'], l_ind[1]: ['A01C', 'A01D', 'A01G', 'A01H']}
data_v = pd.DataFrame(data=d)
print('用以验证的Dataframe:\n', data_v)
compare_column=l_ind[0]
print('仅读取以下列\n', column_show)
# -------------------------------------------------------------------------------
# 第一大类,产业描述为语料库,可随意扩展至任意专利
# <查询词>:专利数据[IPC官方注释](A01大组共12个小类)
# <语料库>:产业描述文字(全1094),可以仅提取前60个类目
# Comment_to_Comment/5_p2i_1_cos.py
p2i_c2c = pd.read_csv('../../../out/C_to_C/p2i/cos_A01_all.csv', encoding='gbk')
p2i_c2c['p_code'] = l_ipc_code
print('<查询词>:专利数据[IPC官方注释](A01大组共12个小类),所得出的余弦相似度:\n', p2i_c2c[column_show].sort_values([compare_column], ascending=False))

# <查询词>:专利数据[26000条专利](A01大组共12个小类)
# <语料库>:产业描述文字(全1094),可以仅提取前60个类目
# 4_digit/5_p2i_1_cos.py
p2i_d2c = pd.read_csv('../../../out/4_digit/p2i/cos_A01_all.csv', encoding='gbk')
p2i_d2c['p_code'] = l_ipc_code
print('<查询词>:专利数据[26000条专利](A01大组共12个小类),所得出的余弦相似度:\n', p2i_d2c[column_show].sort_values([compare_column], ascending=False))
# -------------------------------------------------------------------------------

# -------------------------------------------------------------------------------
# 处理1 展示原始数据准确程度
print('原始1数据:')
data_ok = p2i_c2c[p2i_c2c[compare_column] > 0].copy()
data_ok = data_ok[column_show].sort_values([compare_column], ascending=False)
# print('合并原始数据与检验数据后:\n',data_ok)
v_0111(data_ok, data_v)

print('原始2数据:')
data_ok = p2i_d2c[p2i_d2c[compare_column] > 0].copy()
data_ok = data_ok[column_show].sort_values([compare_column], ascending=False)
# print('合并原始数据与检验数据后:\n',data_ok)
v_0111(data_ok, data_v)
# -------------------------------------------------------------------------------

# -------------------------------------------------------------------------------
# 处理2 Z-score标准化方法处理后:
print('Z-score标准化方法处理后:')
if (p2i_c2c[compare_column].max()-p2i_c2c[compare_column].min())==0:
    p2i_c2c['zscore']=0
else:
    p2i_c2c['zscore'] = zscore(p2i_c2c[compare_column])

if (p2i_d2c[compare_column].max()-p2i_d2c[compare_column].min())==0:
    p2i_d2c['min-max']=0
else:
    p2i_d2c['zscore'] = zscore(p2i_d2c[compare_column])

p2i_c2c['zscore+'] = p2i_c2c['zscore'] + p2i_d2c['zscore']
print('两者数据Z-score处理后相加:\n', p2i_c2c[['p_code','zscore+']].sort_values(['zscore+'], ascending=False))

data_ok['zscore+']=p2i_c2c['zscore+']
data_ok = p2i_c2c[p2i_c2c['zscore+'] > 0].copy()
print('大于0的数据:\n',data_ok[['p_code','zscore+']].sort_values(['zscore+'], ascending=False))

data_ok = data_ok[column_show].sort_values([compare_column], ascending=False)
v_0111(data_ok, data_v)

data_ok=data_ok.iloc[0:1]
print('取排位前1的数据与检验数据后:\n', data_ok)
v_0111(data_ok, data_v)
# -------------------------------------------------------------------------------

# -------------------------------------------------------------------------------
# 处理3 min-max标准化方法处理后:
print('min-max标准化方法处理后:')
if (p2i_c2c[compare_column].max()-p2i_c2c[compare_column].min())==0:
    p2i_c2c['min-max']=0
else:
    p2i_c2c['min-max']=(p2i_c2c[compare_column]-p2i_c2c[compare_column].min())/(p2i_c2c[compare_column].max()-p2i_c2c[compare_column].min())

if (p2i_d2c[compare_column].max()-p2i_d2c[compare_column].min())==0:
    p2i_d2c['min-max']=0
else:
    p2i_d2c['min-max']=(p2i_d2c[compare_column]-p2i_d2c[compare_column].min())/(p2i_d2c[compare_column].max()-p2i_d2c[compare_column].min())

p2i_c2c['min-max+'] = p2i_c2c['min-max'] + p2i_d2c['min-max']
print('两者数据min-max+处理后相加:\n', p2i_c2c[['p_code','min-max+']].sort_values(['min-max+'], ascending=False))

data_ok['min-max+']=p2i_c2c['min-max+']
data_ok = p2i_c2c[p2i_c2c['min-max+'] > 0].copy()
print('大于0的数据:\n',data_ok[['p_code','min-max+']].sort_values(['min-max+'], ascending=False))

#这个效果好!  F1分数（综合分数）:57.14 %-->57.14 %
data_ok = data_ok[column_show].sort_values([compare_column], ascending=False)
v_0111(data_ok, data_v)

data_ok=data_ok.iloc[0:1]
print('取排位前1的数据与检验数据后:\n', data_ok)
v_0111(data_ok, data_v)


# -------------------------------------------------------------------------------


# new_data.to_csv('../../../out/C_to_C/cos_A_A01.csv', index=False, encoding='gbk')

print('数据转换完成! 耗时：%fs!' % (time.time() - time_initial))
