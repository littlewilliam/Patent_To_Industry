# coding=utf-8

__author__ = 'tianchuang'

import jieba
import jieba.analyse
import pandas as pd
import re
import time

time_initial = time.time()

f = open('./../res/A01B.csv', 'r')
# 读取所有行
lines = f.readlines()[1:]
f.close()

sa01b=''
for l in lines:
    l=l.strip()
    l=re.sub(r'([\d])','',l)
    l=re.sub(r'([a-z])','',l)

    sa01b=sa01b+l

print (len(sa01b))
tagsA01B=jieba.analyse.extract_tags(sa01b, topK=100, withWeight=False, allowPOS=('n'))
print('A01B:')
print(",".join(tagsA01B))

print ('完成! 耗时：%fs!' % (time.time() - time_initial))
