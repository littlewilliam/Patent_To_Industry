# coding=utf-8
__author__ = 'tianchuang'

# 第二大类,专利数据为语料库,语料库全,用全数据扩展后会有变化
# <查询词>:产业描述文字(A 农、林、牧、渔业,60类目)
# <语料库>:专利数据[IPC官方注释](A01大组共12个小类)
# <查询词>:产业描述文字(A 农、林、牧、渔业,60类目)
# <语料库>:专利数据[162813条专利](A部下的全部84个小类)
# 寻找最适宜的标准化方式

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

# 国知局公布的映射成果,用于验证结果的准确性,检查A 农、林、牧、渔业,前26个类目
# data_v=read_data_v_26()

# 国知局公布的映射成果,用于验证结果的准确性,检查A 农、林、牧、渔业,60类目
data_v=read_data_v_60()

cols_data_v = list(data_v.columns)
# print(cols_data_v)
print('用以验证的Dataframe:\n', data_v)

export_d = ['i_code', 'P1', 'R1', 'F1', 'P11', 'P2', 'R2', 'F2', 'P21', 'ZP', 'ZR', 'ZF', 'Z1P', 'MP', 'MR', 'MF',
            'M1P']
data_export = pd.DataFrame(columns=export_d)

# -------------------------------------------------------------------------------
# 第二大类,专利数据为语料库,语料库全,用全数据扩展后会有变化
# <查询词>:产业描述文字(A 农、林、牧、渔业,60类目)
# <语料库>:专利数据[IPC官方注释](A01大组共12个小类)
# Comment_to_Comment/0_i2p_1_cos.py,然后转置
i2p_c2c = pd.read_csv('../../../out/C_to_C/cos_A_A01_T.csv', encoding='gbk')
i2p_c2c['p_code'] = l_ipc_code

# <查询词>:产业描述文字(A 农、林、牧、渔业,60类目)
# <语料库>:专利数据[26000条专利](A01大组共12个小类)
# 4_digit/0_i2p_1_cos.py,然后转置
i2p_c2d = pd.read_csv('../../../out/4_digit/cos_A_A01_T.csv', encoding='gbk')
i2p_c2d['p_code'] = l_ipc_code
# -------------------------------------------------------------------------------

i = 0
for cols in cols_data_v:

    data_export.loc[i] = None
    data_export['i_code'].loc[i] = cols

    compare_column = cols
    column_show = ['p_code'] + l_ind[i:i + 1]
    # print('------------------------------检验以下列------------------------------\n', compare_column, '\n')

    # -------------------------------------------------------------------------------
    # 处理1 展示原始数据准确程度
    # print('原始1数据:(<查询词>:专利数据[IPC官方注释](A01大组共12个小类))')
    data_ok = i2p_c2c[i2p_c2c[compare_column] > 0].copy()
    data_ok = data_ok[column_show].sort_values([compare_column], ascending=False)
    # print('合并原始数据与检验数据后:\n',data_ok)
    data_export[export_d[1]].loc[i], data_export[export_d[2]].loc[i], data_export[export_d[3]].loc[
        i] = f_compare_column(data_ok, data_v, compare_column)

    data_ok = data_ok.iloc[0:1]
    data_export[export_d[4]].loc[i], x_null1, x_null2 = f_compare_column(data_ok, data_v, compare_column)

    # print('原始2数据:(<查询词>:专利数据[26000条专利](A01大组共12个小类))')
    data_ok = i2p_c2d[i2p_c2d[compare_column] > 0].copy()
    data_ok = data_ok[column_show].sort_values([compare_column], ascending=False)
    # print('合并原始数据与检验数据后:\n',data_ok)
    data_export[export_d[5]].loc[i], data_export[export_d[6]].loc[i], data_export[export_d[7]].loc[
        i] = f_compare_column(data_ok, data_v, compare_column)

    data_ok = data_ok.iloc[0:1]
    data_export[export_d[8]].loc[i], x_null1, x_null2 = f_compare_column(data_ok, data_v, compare_column)
    # -------------------------------------------------------------------------------

    # -------------------------------------------------------------------------------
    # 处理2 Z-score标准化方法处理后:
    # print('--------Z-score标准化方法处理后:--------')

    # 如果该列结果全为0,则跳过处理(赋值为零)
    if (i2p_c2c[compare_column].max() - i2p_c2c[compare_column].min()) == 0:
        i2p_c2c['zscore'] = 0
    else:
        i2p_c2c['zscore'] = zscore(i2p_c2c[compare_column])

    if (i2p_c2d[compare_column].max() - i2p_c2d[compare_column].min()) == 0:
        i2p_c2d['min-max'] = 0
    else:
        i2p_c2d['zscore'] = zscore(i2p_c2d[compare_column])

    i2p_c2c['zscore+'] = i2p_c2c['zscore'] + i2p_c2d['zscore']
    # print('两者数据Z-score处理后相加:\n', i2p_c2c[['p_code', 'zscore+']].sort_values(['zscore+'], ascending=False))

    data_ok['zscore+'] = i2p_c2c['zscore+']
    #阈值最小为0.13
    data_ok = i2p_c2c[i2p_c2c['zscore+'] > 0].copy()
    # print('大于0的数据:\n', data_ok[['p_code', 'zscore+']].sort_values(['zscore+'], ascending=False))

    data_ok = data_ok[column_show].sort_values([compare_column], ascending=False)
    data_export[export_d[9]].loc[i], data_export[export_d[10]].loc[i], data_export[export_d[11]].loc[
        i] = f_compare_column(data_ok, data_v, compare_column)

    data_ok = data_ok.iloc[0:1]
    # print('取排位前1的数据与检验数据后:\n', data_ok['p_code'])
    data_export[export_d[12]].loc[i], x_null1, x_null2 = f_compare_column(data_ok, data_v, compare_column)
    # -------------------------------------------------------------------------------

    # -------------------------------------------------------------------------------
    # 处理3 min-max标准化方法处理后:
    # print('--------min-max标准化方法处理后:--------')
    if (i2p_c2c[compare_column].max() - i2p_c2c[compare_column].min()) == 0:
        i2p_c2c['min-max'] = 0
    else:
        i2p_c2c['min-max'] = (i2p_c2c[compare_column] - i2p_c2c[compare_column].min()) / (
            i2p_c2c[compare_column].max() - i2p_c2c[compare_column].min())

    if (i2p_c2d[compare_column].max() - i2p_c2d[compare_column].min()) == 0:
        i2p_c2d['min-max'] = 0
    else:
        i2p_c2d['min-max'] = (i2p_c2d[compare_column] - i2p_c2d[compare_column].min()) / (
            i2p_c2d[compare_column].max() - i2p_c2d[compare_column].min())

    i2p_c2c['min-max+'] = i2p_c2c['min-max'] + i2p_c2d['min-max']
    # print('两者数据min-max+处理后相加:\n', i2p_c2c[['p_code', 'min-max+']].sort_values(['min-max+'], ascending=False))

    data_ok['min-max+'] = i2p_c2c['min-max+']
    data_ok = i2p_c2c[i2p_c2c['min-max+'] > 0].copy()
    # print('大于0的数据:\n', data_ok[['p_code', 'min-max+']].sort_values(['min-max+'], ascending=False))

    # 这个效果好!  F1分数（综合分数）:57.14 %-->57.14 %
    data_ok = data_ok[column_show].sort_values([compare_column], ascending=False)
    data_export[export_d[13]].loc[i], data_export[export_d[14]].loc[i], data_export[export_d[15]].loc[
        i] = f_compare_column(data_ok, data_v, compare_column)

    data_ok = data_ok.iloc[0:1]
    # print('取排位前1的数据与检验数据后:\n', data_ok['p_code'])
    data_export[export_d[16]].loc[i], x_null1, x_null2 = f_compare_column(data_ok, data_v, compare_column)

    # -------------------------------------------------------------------------------



    i += 1

x=(data_export['ZR'].sum())/(data_export['ZR'].count()-4)
print('平均召回率',x)
data_export.to_csv('../../../out/combine/method_2.csv', index=False, encoding='gbk')

print('数据处理完成! 耗时：%fs!' % (time.time() - time_initial))
