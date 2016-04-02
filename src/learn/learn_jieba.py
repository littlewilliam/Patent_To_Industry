# coding=utf-8
__author__ = 'tianchuang'

import jieba
import jieba.posseg as pseg

n_all = ['n', 'nr', 'nr1', 'nr2', 'nrj', 'nrf', 'ns', 'nsf', 'nt', 'nz', 'nl', 'ng']


sen="玉米种植,包括对下列玉米的种植活动：,—,白玉米：种用白玉米、其他白玉米；—,黄玉米：种用黄玉米、其他黄玉米；—,糯玉米：种用糯玉米、其他糯玉米；—,甜玉米：种用甜玉米、其他甜玉米；—,其他玉米：玉米秸及其他未列明玉米。"


words_p = pseg.cut(sen)
word_list = []
for w, flag in words_p:
    # print('未判断:')
    # print('%s %s' % (w, flag))

    if flag in n_all:
        print('判断是否为n后:')
        print('%s %s' % (w, flag))
        word_list.append(w)
print(word_list)



# seg_list = jieba.cut(sen, cut_all=True)
# print("Full Mode: " + "/ ".join(seg_list))  # 全模式
#
# seg_list = jieba.cut(sen, cut_all=False)
# print("Default Mode: " + "/ ".join(seg_list))  # 精确模式

# seg_list = jieba.cut("他来到了网易杭研大厦")  # 默认是精确模式
# print(", ".join(seg_list))
#
# seg_list = jieba.cut("他来到了网易杭研大厦", HMM=False)  # 默认是精确模式
# print(", ".join(seg_list))
#
# l = "小明硕士毕业于中国科学院计算所，后在日本京都大学深造"
# seg_list = jieba.cut_for_search(l)  # 搜索引擎模式
# print(", ".join(seg_list))
#
# words = pseg.cut(l)
# word_list = []
# for word, flag in words:
#
#     if flag == 'n':
#         print('%s %s' % (word, flag))
#         word_list.append(word)
#         print(word)
#
# print(word_list)