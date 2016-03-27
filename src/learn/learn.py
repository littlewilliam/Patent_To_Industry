# coding=utf-8
from random import randint
import pandas as pd
import re

__author__ = 'tianchuang'

#字符串中替换指定字符

line='!!!abc'
print(line)
line = re.sub('[!@#$]', '', line)
print(line)





#DataFrame增加行并改某一数值
'''
df = pd.DataFrame(columns=('lib', 'qty1', 'qty2'))
print df

df.loc[0] = None

df['lib'].loc[0]='100eg'

print df
'''
