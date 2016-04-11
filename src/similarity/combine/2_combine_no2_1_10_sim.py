# coding=utf-8
__author__ = 'tianchuang'

# 第二大类,专利数据为语料库,语料库全,用全数据扩展后会有变化
# <查询词>:产业描述文字(A 农、林、牧、渔业,60类目)
# <语料库>:专利数据[IPC官方注释](A01大组共12个小类)
# <查询词>:产业描述文字(A 农、林、牧、渔业,60类目)
# <语料库>:专利数据[26000条专利](A01大组共12个小类)
# 导出相似度矩阵 和 TOP1相似度

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

# 前60个产业分类,即到"0540 渔业服务业"为止
l = l_ind[0:60]
# 前12个专利类目分类,即到"A01P"为止
p = l_ipc[0:12]

export_d = ['patent']
export_d = export_d + l
data_export = pd.DataFrame(columns=export_d)

# -------------------------------------------------------------------------------
# 第二大类,专利数据为语料库,语料库全,用全数据扩展后会有变化
# <查询词>:产业描述文字(A 农、林、牧、渔业,60类目)
# <语料库>:专利数据[IPC官方注释](A01大组共12个小类)
# Comment_to_Comment/0_i2p_1_cos.py,然后转置
i2p_c2c = pd.read_csv('../../../out/C_to_C/cos_A_A01_T.csv', encoding='gbk')

# <查询词>:产业描述文字(A 农、林、牧、渔业,60类目)
# <语料库>:专利数据[26000条专利](A01大组共12个小类)
# 4_digit/0_i2p_1_cos.py,然后转置
i2p_c2d = pd.read_csv('../../../out/4_digit/cos_A_A01_T.csv', encoding='gbk')
# -------------------------------------------------------------------------------

i = 0

for col in l:
    # Z-score标准化方法处理:

    # 如果该列结果全为0,则跳过处理(赋值为零)
    if (i2p_c2c[col].max() - i2p_c2c[col].min()) == 0:
        i2p_c2c['zscore'] = 0
    else:
        i2p_c2c['zscore'] = zscore(i2p_c2c[col])

    if (i2p_c2d[col].max() - i2p_c2d[col].min()) == 0:
        i2p_c2d['min-max'] = 0
    else:
        i2p_c2d['zscore'] = zscore(i2p_c2d[col])

    data_export[col] = round((i2p_c2c['zscore'] + i2p_c2d['zscore']),4)

    # print('两者数据Z-score处理后相加:\n', i2p_c2c[['p_code', 'zscore+']].sort_values(['zscore+'], ascending=False))
    i += 1

# 添加专利分类号说明
n = 0
for p_col in p:
    data_export['patent'].loc[n] = p_col
    # print(data_export['patent'])
    n += 1


# print('data_export\n',data_export.head())

# 导出相似度矩阵
data_export.to_csv('../../../out/combine/method_2_sim.csv', index=False, encoding='gbk')




# 导出TOP1相似度映射关系

export_d = ['industry','patent']
top_1 = pd.DataFrame(columns=export_d)

i = 0

for col in l:

    d_top_1 = data_export[['patent',col]].sort_values([col], ascending=False)
    d_top_1 = d_top_1.iloc[0:1]
    # print('取排位前1的数据与检验数据后:\n',d_top_1[['patent',col]])
    # print(d_top_1['patent'].iloc[0])

    top_1.loc[i] = None

    top_1['industry'].loc[i] = col
    top_1['patent'].loc[i] = d_top_1['patent'].iloc[0]

    i += 1

print(top_1.head())

top_1.to_csv('../../../out/combine/method_2_top1.csv', index=False, encoding='gbk')

print('数据处理完成! 耗时：%fs!' % (time.time() - time_initial))
