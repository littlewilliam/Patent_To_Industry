# coding=utf-8

__author__ = 'tianchuang'

# 学习PyNLPIR

import pynlpir
from pynlpir import nlpir


import sys
# print sys.getdefaultencoding()
# reload(sys)
#
# sys.setdefaultencoding("utf-8")

pynlpir.open()

# pynlpir.open(encoding='utf-8')

s = 'NLPIR分词系统前身为2000年发布的ICTCLAS词法分析系统，从2009年开始，为了和以前工作进行大的区隔，并推广NLPIR自然语言处理与信息检索共' \
    '享平台，调整命名为NLPIR分词系统。'
print (s)
print (pynlpir.segment(s,pos_tagging=False))
print (pynlpir.get_key_words(s, weighted=True))

c=pynlpir.segment(s,pos_tagging=False)
c=str("|".join(c)).encode('utf-8')
print (c)



import jieba

tokens = jieba.cut(s, cut_all=False)
print ('精确模式:')
print("|".join(tokens))
