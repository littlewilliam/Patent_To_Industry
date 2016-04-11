# coding=utf-8
__author__ = 'tianchuang'

# 相似度计算,自动化运行六个py程序,得出计算结果

import time
time_1 = time.time()

import a1,a2,a3,a4,a5,a6


print('总耗时：%fs!' % (time.time() - time_1))

