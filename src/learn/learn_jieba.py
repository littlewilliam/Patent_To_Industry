# coding=utf-8
__author__ = 'tianchuang'

import jieba
import jieba.posseg as pseg

seg_list = jieba.cut("我来到北京清华大学", cut_all=True)
print("Full Mode: " + "/ ".join(seg_list))  # 全模式

seg_list = jieba.cut("我来到北京清华大学", cut_all=False)
print("Default Mode: " + "/ ".join(seg_list))  # 精确模式

seg_list = jieba.cut("他来到了网易杭研大厦")  # 默认是精确模式
print(", ".join(seg_list))

seg_list = jieba.cut("他来到了网易杭研大厦", HMM=False)  # 默认是精确模式
print(", ".join(seg_list))

l = "小明硕士毕业于中国科学院计算所，后在日本京都大学深造"
seg_list = jieba.cut_for_search(l)  # 搜索引擎模式
print(", ".join(seg_list))

words = pseg.cut(l)
word_list = []
for word, flag in words:

    if flag == 'n':
        print('%s %s' % (word, flag))
        word_list.append(word)
        print(word)

print(word_list)