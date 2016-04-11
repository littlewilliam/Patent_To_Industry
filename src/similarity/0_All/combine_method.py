# coding=utf-8
__author__ = 'tianchuang'

# 相似度计算,专利数据已按照小类各提取出所有名词,产业类目也已提取出所有名词

import pandas as pd
import time
import numpy as np


# 读取IPC代码与描述
def read_IPC_code():
    print('开始读取IPC代码与描述')
    ipc_code = pd.read_csv('../../../res/A01/IPC_Comment.csv')
    l_ipc_code = []
    l_ipc = []

    for index, item in ipc_code.iterrows():
        code = item['code']
        # # 此处为判断A0大类下的全部12个小类,可调整
        # if code[0:2] == 'A0':
        # 此处为判断A部下的全部84个小类,可调整
        if code[0:1] == 'A':
            l_ipc_code.append(code)
            code = code + ' ' + item['describe']
            l_ipc.append(code)
            # print(code)
    print(l_ipc_code, '\n读取完毕')
    return l_ipc_code, l_ipc
    # l_ipc_code = ['A01B', 'A01C', 'A01D', 'A01F', 'A01G', 'A01H', 'A01J', 'A01K', 'A01L', 'A01M', 'A01N', 'A01P']


# 读取产业类目代码与描述
def read_ind_code():
    print('开始读取产业代码与描述')

    ind_code = pd.read_csv('../../../res/Industry/4_digit/GMJJHY_Comment_4.csv', dtype=str)
    l_ind_code = []
    l_ind = []

    for index, item in ind_code.iterrows():
        code_str = str(item['code'])
        code = int(item['code'])
        # 此处为判断A	农、林、牧、渔业类目下的所有4位精度的国民经济行业类目,可调整
        if code <= 540:
            # if code <= 9600:

            l_ind_code.append(code_str)
            code_str = code_str + ' ' + item['describe']
            l_ind.append(code_str)
            # print(code_str)
    print(l_ind_code, '\n读取完毕')

    return l_ind_code, l_ind



# 检验'XXX',例如'0111 稻谷种植',结果的精确率、召回率和F2(F1)值,返回三个数值
def f_compare_column(data_ok, data_v, compare_column):
    data_c = data_ok.merge(data_v, how='inner', left_on=['p_code'], right_on=compare_column)
    c_1 = len(data_ok)
    # 因为dataframe性质,有些列会有空行,即NaN,需要减去NaN的数
    true_len = len(data_v[compare_column]) - data_v[compare_column].isnull().sum()
    c_2 = true_len
    c_3 = len(data_c)
    if c_1 != 0:
        P_Score = c_3 / c_1
    else:
        P_Score = 0
    if c_2 != 0:
        R_Score = c_3 / c_2
    else:
        R_Score = 0
    if (P_Score + R_Score) != 0:
        F2_Score = (5 * P_Score * R_Score) / (4*P_Score + R_Score)
    else:
        F2_Score = 0
    print('| 精确率(正确率):%.2f' % (P_Score * 100), '%', ' | 召回率(查全率):%.2f' % (R_Score * 100), '%',
          ' | F2分数（综合分数）:%.2f' % (F2_Score * 100), '%|')
    return round(P_Score, 3), round(R_Score, 3), round(F2_Score, 3)


# 国知局公布的映射成果,用于验证结果的准确性,检查A 农、林、牧、渔业,60类目
def read_data_v_60():
    l_ind_code, l_ind = read_ind_code()
    x = np.nan
    d = {l_ind[0]: ['A01C', 'A01D', 'A01G', 'A01H'], l_ind[1]: ['A01C', 'A01D', 'A01G', 'A01H'],
         l_ind[2]: ['A01C', 'A01D', 'A01G', 'A01H'], l_ind[3]: ['A01C', 'A01D', 'A01G', 'A01H']
        , l_ind[4]: ['A01C', 'A01D', 'A01G', 'A01H'], l_ind[5]: ['A01C', 'A01D', 'A01G', 'A01H'],
         l_ind[6]: ['A01C', 'A01D', 'A01G', 'A01H'], l_ind[7]: ['A01C', 'A01D', 'A01G', 'A01H']
        , l_ind[8]: ['A01C', 'A01D', 'A01G', 'A01H'], l_ind[9]: ['A01C', 'A01D', 'A01G', 'A01H'],
         l_ind[10]: ['A01C', 'A01D', 'A01G', 'A01H'], l_ind[11]: ['A01C', 'A01D', 'A01G', 'A01H']
        , l_ind[12]: ['A01C', 'A01D', 'A01G', 'A01H'], l_ind[13]: ['A01C', 'A01D', 'A01G', 'A01H'],
         l_ind[14]: ['A01C', 'A01D', 'A01G', 'A01H'], l_ind[15]: ['A01C', 'A01D', 'A01G', 'A01H']
        , l_ind[16]: ['A01C', 'A01D', 'A01G', 'A01H'], l_ind[17]: ['A01C', 'A01D', 'A01G', 'A01H'],
         l_ind[18]: ['A01C', 'A01D', 'A01G', 'A01H'], l_ind[19]: ['A01C', 'A01D', 'A01G', 'A01H']
        , l_ind[20]: ['A01C', 'A01D', 'A01G', 'A01H'], l_ind[21]: ['A01C', 'A01D', 'A01G', 'A01H'],
         l_ind[22]: ['A01C', 'A01D', 'A01G', 'A01H'], l_ind[23]: ['A01C', 'A01D', 'A01G', 'A01H']
        , l_ind[24]: ['A01C', 'A01D', 'A01G', 'A01H'], l_ind[25]: ['A01C', 'A01D', 'A01G', 'A01H']

        , l_ind[26]: ['A01C', 'A01H', x, x], l_ind[27]: ['A01G', 'A01H', x, x], l_ind[28]: ['A01G', x, x, x],
         l_ind[29]: ['A01B', 'A01C', 'A01G', x]
        , l_ind[30]: ['A01G', x, x, x], l_ind[31]: ['A01G', x, x, x], l_ind[32]: ['A01D', x, x, x],
         l_ind[33]: ['A01D', 'A01G', x, x]

        , l_ind[34]: ['A01K', x, x, x], l_ind[35]: ['A01K', x, x, x], l_ind[36]: ['A01K', x, x, x],
         l_ind[37]: ['A01K', x, x, x]
        , l_ind[38]: ['A01K', x, x, x], l_ind[39]: ['A01K', x, x, x], l_ind[40]: ['A01K', x, x, x],
         l_ind[41]: ['A01K', x, x, x]
        , l_ind[42]: ['A01K', x, x, x], l_ind[43]: ['A01K', x, x, x],

         l_ind[44]: ['A01M', x, x, x], l_ind[45]: ['A01K', x, x, x]
        , l_ind[46]: ['A01G', 'A01H', 'A01K', x], l_ind[47]: ['A01G', 'A01H', 'A01K', x], l_ind[48]: ['A01K', x, x, x],
         l_ind[49]: ['A01K', x, x, x]

        , l_ind[50]: [x, x, x, x], l_ind[51]: [x, x, x, x], l_ind[52]: ['A24B', x, x, x],

         l_ind[53]: ['A01B', 'A01G', 'A01M', 'A01N']
        , l_ind[54]: ['A01G', 'A01M', x, x],

         l_ind[55]: [x, x, x, x], l_ind[56]: [x, x, x, x],

         l_ind[57]: ['A01N', x, x, x], l_ind[58]: ['A01N', 'A61D', x, x]
        , l_ind[59]: ['A01N', 'A61D', x, x]
         }
    data_v = pd.DataFrame(data=d)
    return data_v


# data_v=read_data_v_60()
# print(data_v)
# print(data_v['0529 其他林业服务'])
# true_len=len(data_v['0529 其他林业服务'])-data_v['0529 其他林业服务'].isnull().sum()
# print(true_len)


# 国知局公布的映射成果,用于验证结果的准确性,检查A 农、林、牧、渔业,前26个类目
def read_data_v_26():
    l_ind_code, l_ind = read_ind_code()

    d = {l_ind[0]: ['A01C', 'A01D', 'A01G', 'A01H'], l_ind[1]: ['A01C', 'A01D', 'A01G', 'A01H'],
         l_ind[2]: ['A01C', 'A01D', 'A01G', 'A01H'], l_ind[3]: ['A01C', 'A01D', 'A01G', 'A01H']
        , l_ind[4]: ['A01C', 'A01D', 'A01G', 'A01H'], l_ind[5]: ['A01C', 'A01D', 'A01G', 'A01H'],
         l_ind[6]: ['A01C', 'A01D', 'A01G', 'A01H'], l_ind[7]: ['A01C', 'A01D', 'A01G', 'A01H']
        , l_ind[8]: ['A01C', 'A01D', 'A01G', 'A01H'], l_ind[9]: ['A01C', 'A01D', 'A01G', 'A01H'],
         l_ind[10]: ['A01C', 'A01D', 'A01G', 'A01H'], l_ind[11]: ['A01C', 'A01D', 'A01G', 'A01H']
        , l_ind[12]: ['A01C', 'A01D', 'A01G', 'A01H'], l_ind[13]: ['A01C', 'A01D', 'A01G', 'A01H'],
         l_ind[14]: ['A01C', 'A01D', 'A01G', 'A01H'], l_ind[15]: ['A01C', 'A01D', 'A01G', 'A01H']
        , l_ind[16]: ['A01C', 'A01D', 'A01G', 'A01H'], l_ind[17]: ['A01C', 'A01D', 'A01G', 'A01H'],
         l_ind[18]: ['A01C', 'A01D', 'A01G', 'A01H'], l_ind[19]: ['A01C', 'A01D', 'A01G', 'A01H']
        , l_ind[20]: ['A01C', 'A01D', 'A01G', 'A01H'], l_ind[21]: ['A01C', 'A01D', 'A01G', 'A01H'],
         l_ind[22]: ['A01C', 'A01D', 'A01G', 'A01H'], l_ind[23]: ['A01C', 'A01D', 'A01G', 'A01H']
        , l_ind[24]: ['A01C', 'A01D', 'A01G', 'A01H'], l_ind[25]: ['A01C', 'A01D', 'A01G', 'A01H']

         }
    data_v = pd.DataFrame(data=d)
    return data_v
# 检验'0111 稻谷种植'结果的精确率、召回率和F1值
def v_0111(data_ok, data_v):
    data_c = data_ok.merge(data_v, how='inner', left_on=['p_code'], right_on='0111 稻谷种植')
    c_1 = len(data_ok)
    c_2 = len(data_v)
    c_3 = len(data_c)
    if c_1 != 0:
        P_Score = c_3 / c_1
    else:
        P_Score = 0
    if c_2 != 0:
        R_Score = c_3 / c_2
    else:
        R_Score = 0
    if (P_Score + R_Score) != 0:
        F1_Score = (2 * P_Score * R_Score) / (P_Score + R_Score)
    print('| 精确率(正确率):%.2f' % (P_Score * 100), '%', ' | 召回率(查全率):%.2f' % (R_Score * 100), '%',
          ' | F1分数（综合分数）:%.2f' % (F1_Score * 100), '%|')


# 检验'0112 小麦种植'结果的精确率、召回率和F1值
def v_0112(data_ok, data_v):
    data_c = data_ok.merge(data_v, how='inner', left_on=['p_code'], right_on='0112 小麦种植')
    c_1 = len(data_ok)
    c_2 = len(data_v)
    c_3 = len(data_c)
    if c_1 != 0:
        P_Score = c_3 / c_1
    else:
        P_Score = 0
    if c_2 != 0:
        R_Score = c_3 / c_2
    else:
        R_Score = 0
    if (P_Score + R_Score) != 0:
        F1_Score = (2 * P_Score * R_Score) / (P_Score + R_Score)
    else:
        F1_Score = 0
    print('| 精确率(正确率):%.2f' % (P_Score * 100), '%', ' | 召回率(查全率):%.2f' % (R_Score * 100), '%',
          ' | F1分数（综合分数）:%.2f' % (F1_Score * 100), '%|')


# 检验'XXX',例如'0111 稻谷种植',结果的精确率、召回率和F1值,只打印,不返回数值
def f_compare_column_old(data_ok, data_v, compare_column):
    data_c = data_ok.merge(data_v, how='inner', left_on=['p_code'], right_on=compare_column)
    c_1 = len(data_ok)
    c_2 = len(data_v)
    c_3 = len(data_c)
    if c_1 != 0:
        P_Score = c_3 / c_1
    else:
        P_Score = 0
    if c_2 != 0:
        R_Score = c_3 / c_2
    else:
        R_Score = 0
    if (P_Score + R_Score) != 0:
        F1_Score = (2 * P_Score * R_Score) / (P_Score + R_Score)
    else:
        F1_Score = 0
    print('| 精确率(正确率):%.2f' % (P_Score * 100), '%', ' | 召回率(查全率):%.2f' % (R_Score * 100), '%',
          ' | F1分数（综合分数）:%.2f' % (F1_Score * 100), '%|')

