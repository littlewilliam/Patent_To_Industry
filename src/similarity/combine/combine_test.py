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

print('仅读取以下列\n', column_show)
# -------------------------------------------------------------------------------
# 第一大类,产业描述为语料库,可随意扩展至任意专利
# <查询词>:专利数据[IPC官方注释](A01大组共12个小类)
# <语料库>:产业描述文字(全1094),可以仅提取前60个类目
# Comment_to_Comment/5_p2i_1_cos.py
p2i_c2c = pd.read_csv('../../../out/C_to_C/p2i/cos_A01_all.csv', encoding='gbk')
p2i_c2c['p_code'] = l_ipc_code
print(p2i_c2c[column_show])

# <查询词>:专利数据[26000条专利](A01大组共12个小类)
# <语料库>:产业描述文字(全1094),可以仅提取前60个类目
# 4_digit/5_p2i_1_cos.py
p2i_d2c = pd.read_csv('../../../out/4_digit/p2i/cos_A01_all.csv', encoding='gbk')
p2i_d2c['p_code'] = l_ipc_code

print(p2i_d2c[column_show])

# -------------------------------------------------------------------------------


# -------------------------------------------------------------------------------
# 第二大类,专利数据为语料库,语料库全,用全数据扩展后会有变化
# <查询词>:产业描述文字(A 农、林、牧、渔业,60类目)
# <语料库>:专利数据[IPC官方注释](A01大组共12个小类)
# Comment_to_Comment/0_i2p_1_cos.py,然后转置
i2p_c2c = pd.read_csv('../../../out/C_to_C/cos_A_A01_T.csv', encoding='gbk')
i2p_c2c['p_code'] = l_ipc_code
print(i2p_c2c[column_show])

# <查询词>:产业描述文字(A 农、林、牧、渔业,60类目)
# <语料库>:专利数据[26000条专利](A01大组共12个小类)
# 4_digit/0_i2p_1_cos.py,然后转置
i2p_c2d = pd.read_csv('../../../out/4_digit/cos_A_A01_T.csv', encoding='gbk')
i2p_c2d['p_code'] = l_ipc_code
print('需要展示的数据:\n',i2p_c2d[column_show])

i2p_c2d['zscore']=zscore(i2p_c2d[l_ind[0]])
print('Z-score标准化方法处理后:\n',i2p_c2d['zscore'])

data_ok = i2p_c2d[i2p_c2d[l_ind[0]] > 0].copy()
data_ok = data_ok[column_show].sort_values([l_ind[0]], ascending=False)
print('合并原始数据与检验数据后:\n',data_ok)

v_0111(data_ok,data_v)

# -------------------------------------------------------------------------------

# new_data.to_csv('../../../out/C_to_C/cos_A_A01.csv', index=False, encoding='gbk')

print('数据转换完成! 耗时：%fs!' % (time.time() - time_initial))
