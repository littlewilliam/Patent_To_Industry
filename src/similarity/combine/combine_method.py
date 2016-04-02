# coding=utf-8
__author__ = 'tianchuang'

# 相似度计算,专利数据已按照小类各提取出所有名词,产业类目也已提取出所有名词

import pandas as pd
import time

# 读取IPC代码与描述
def read_IPC_code():
    print('开始读取IPC代码与描述')
    ipc_code = pd.read_csv('../../../res/A01/IPC_Comment.csv')
    l_ipc_code = []
    l_ipc = []

    for index, item in ipc_code.iterrows():
        code = item['code']
        # 此处为判断A0大类下的全部12个小类,可调整
        if code[0:2] == 'A0':
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

# 检验'0111 稻谷种植'结果的精确率、召回率和F1值
def v_0111(data_ok,data_v):
    data_c = data_ok.merge(data_v, how='inner', left_on=['p_code'], right_on='0111 稻谷种植')
    c_1 = len(data_ok)
    c_2 = len(data_v)
    c_3 = len(data_c)
    if c_1!=0:
        P_Score = c_3 / c_1
    else:
        P_Score=0
    if c_2 != 0:
        R_Score = c_3 / c_2
    else:
        R_Score = 0
    if (P_Score+R_Score)!=0:
        F1_Score = (2 * P_Score * R_Score) / (P_Score + R_Score)
    print('| 精确率(正确率):%.2f' % (P_Score * 100), '%',' | 召回率(查全率):%.2f' % (R_Score * 100), '%',' | F1分数（综合分数）:%.2f' % (F1_Score * 100), '%|')

# 检验'0112 小麦种植'结果的精确率、召回率和F1值
def v_0112(data_ok,data_v):
    data_c = data_ok.merge(data_v, how='inner', left_on=['p_code'], right_on='0112 小麦种植')
    c_1 = len(data_ok)
    c_2 = len(data_v)
    c_3 = len(data_c)
    if c_1!=0:
        P_Score = c_3 / c_1
    else:
        P_Score=0
    if c_2 != 0:
        R_Score = c_3 / c_2
    else:
        R_Score = 0
    if (P_Score+R_Score)!=0:
        F1_Score = (2 * P_Score * R_Score) / (P_Score + R_Score)
    else:
        F1_Score=0
    print('| 精确率(正确率):%.2f' % (P_Score * 100), '%',' | 召回率(查全率):%.2f' % (R_Score * 100), '%',' | F1分数（综合分数）:%.2f' % (F1_Score * 100), '%|')
