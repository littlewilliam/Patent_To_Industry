# coding=utf-8

__author__ = 'tianchuang'

# 将原始的A01全专利标题与摘要信息进行整合,去除标点符号及英文字母,转换为字符串
# 平均30秒转换一小组数据

import jieba
import jieba.analyse
import pandas as pd
import re
import time

time_initial = time.time()

l_ipc = ['A01B', 'A01C', 'A01D', 'A01F', 'A01G', 'A01H', 'A01J', 'A01K', 'A01L', 'A01M', 'A01N', 'A01P']

print('创造新的表:')
new_data = pd.DataFrame(columns=('code', 'describe'))
print(new_data)

# 读取数据 1到n 的数字
for i in range(0, 12):
    print(x, '开始分词')

    startTime = time.time()

    x = str(l_ipc[i])
    f = open('../../res/A01/clean/' + x + '.csv', 'r')
    # 读取所有行
    lines = f.readlines()[1:]
    f.close()

    s = ''
    for l in lines:
        l = l.strip()
        l = re.sub(r'([\d])', '', l)
        l = re.sub(r'([a-z])', '', l)

        s = s + l

    tags = jieba.analyse.extract_tags(s, topK=1000, withWeight=False, allowPOS=('n'))
    words = []
    words.append(list(tags))
    print(x, '分词结果:\n', (words))

    new_data.loc[i] = None
    new_data['code'].loc[i] = x
    new_data['describe'].loc[i] = words

    print(x, '转换完成')
    print('耗时：%fs!' % (time.time() - startTime))

new_data.to_csv('../../res/A01/IPC_OK.csv', index=False, index_label='index')

print('完成! 耗时：%fs!' % (time.time() - time_initial))
