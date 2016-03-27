# coding=utf-8
__author__ = 'tianchuang'


# 将原始的国民经济行业分类表,进行第一次规整,调整格式为
# code,describe
# A,农、林、牧、渔业本门类包括～大类。
# 01,农业指对各种农作物的种植。
# 011,谷物种植指以收获籽实为主，供人类食用的农作物的种植，如稻谷、小麦、玉米等农作物的种植。稻谷种植包括对下列稻谷的种植活动：—早籼稻：种用早籼稻、其他早籼稻；—晚籼稻：种用晚籼稻、其他晚籼稻；—中籼稻：种用中籼稻、其他中籼稻；—粳稻：种用粳稻、其他粳稻；—糯稻：种用糯稻、其他糯稻；—其他稻谷：稻谷壳、稻谷秸及其他未列明稻谷。小麦种植包括对下列小麦的种植活动：—硬质小麦：种用硬质小麦、其他硬质小麦；—软质小麦：种用软质小麦、其他软质小麦；—混合小麦：种用混合小麦、其他混合小麦；—其他小麦：麦秸及其他未列明小麦。玉米种植包括对下列玉米的种植活动：—白玉米：种用白玉米、其他白玉米；—黄玉米：种用黄玉米、其他黄玉米；—糯玉米：种用糯玉米、其他糯玉米；—甜玉米：种用甜玉米、其他甜玉米；—其他玉米：玉米秸及其他未列明玉米。其他谷物种植包括对下列谷物的种植活动：—谷子：硬谷子、糯谷子、其他谷子；—高粱：红粒高粱（种用红粒高粱、其他红粒高粱）、白粒高粱（种用白粒高粱、其他白粒高粱）、糯高粱（种用糯高粱、其他糯高粱）、其他高粱（其他种用高粱、其他未列明高粱）；—大麦：裸大麦（种用裸大麦、其他裸大麦）、皮大麦（种用皮大麦、其他皮大麦）；—燕麦：裸燕麦、皮燕麦；—黑麦；—荞麦：甜荞麦、苦荞麦；—作物茎、秆、根（部分）：稻草、谷壳、谷子秸、高粱秸；—其他谷物：莜麦、元麦、青稞、糜子（硬糜子、糯糜子）、黍子、紫米、薏苡、其他未列明谷物。


import pandas as pd
import time
import re

time_initial = time.time()

# 读取数据
startTime = time.time()
ind_data = pd.read_csv('../../res/Industry/GMJJHY.csv')
print('数据读取完成! 耗时：%fs!' % (time.time() - startTime))

# 规整数据
print('原数据:')
print(ind_data.head())

print('仅提取有效数据后:')
ind_data = ind_data[['C1', 'C4', 'C5']]
print(ind_data.head())

# 创造新的表

print('创造新的表:')
new_data = pd.DataFrame(columns=('code', 'describe'))
print(new_data)

i = 0
n = 1
for index, row in ind_data.iterrows():
    # if index==1000:
    #     break
    if n == 1:

        if row['C1']> 0:
            # print('索引: {}'.format(index))
            # print('读取到的数据  C1: {}; Des1: {}; Des2: {}'.format(row['C1'], row['C4'], row['C5']))

            new_data.loc[i] = None
            new_data['code'].loc[i] = row['C1']

            des = str(row['C4']) + (str(row['C5']))
            des = re.sub('nan', '', des)
            # des = re.sub('[、，。：—；～]', '', des)
            des = re.sub('[0123456789]', '', des)
            new_data['describe'].loc[i] = des

            # print new_data.loc[i]

            i += 1
            n = 0

    else:
        if row['C1'] > 0:

            new_data.loc[i] = None
            new_data['code'].loc[i] = row['C1']

            des = str(row['C4']) + (str(row['C5']))
            des = re.sub('nan', '', des)
            # des = re.sub('[、，。：—；～]', '', des)
            des = re.sub('[0123456789]', '', des)
            new_data['describe'].loc[i] = des

            # print new_data.loc[i]

            i += 1
            n = 0


        else:
            des1 = str(row['C4']) + (str(row['C5']))
            des1 = re.sub('nan', '', des1)
            des1 = re.sub('[0123456789]', '', des1)

            i -= 1
            new_data['describe'].loc[i] = new_data['describe'].loc[i] + des1
            i += 1

print('最终的数据')
print(new_data)

print('全部数据转换完成! 耗时：%fs!' % (time.time() - startTime))

# new_data.to_csv('../../res/Industry/GMJJHY_OK.csv',index=False,index_label='index')
