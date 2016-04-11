# coding=utf-8
from random import randint
import pandas as pd
import re

__author__ = 'tianchuang'

# 观测无效高频率词

from collections import Counter

list1 = ['a', 'b', 'a', 'c', 'a', 'c', 'b']

print(Counter(list1))

ipc = pd.read_csv('../../res/A/IPC_Comment_complete_A_list_n.csv')
stopwords = {}.fromkeys([line.rstrip() for line in open('../../res/stopwords/baidu.txt')])

words = []
for index, row in ipc.iterrows():
    print(row['code'])
    des = row['describe']
    des = re.sub(r'([\[\]\' ])', '', des)
    des = des.split(',')
    s_ok = []
    for item in des:
        if item not in stopwords:
            s_ok.append(item)

    words.append(s_ok)

# print(Counter(words[0]))

words_all = []

for item in words:
    words_all=words_all+item

print(Counter(words_all))
