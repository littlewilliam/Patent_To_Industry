# coding=utf-8
__author__ = 'tianchuang'

import logging
# logging.basicConfig(format='%(asctime)s: %(levelname)s : %(message)s', level=logging.INFO)

from gensim import corpora, models, similarities
import numpy as np
import re
import pandas as pd
import time


# python2.7 则需要以下转码
# import sys
# reload(sys)
# sys.setdefaultencoding("utf-8")

time_initial = time.time()

cos_data = pd.read_csv('../../out/cos_all_A01B.csv',dtype={'industry': str})

print(cos_data.head())

cos_data_T=cos_data.T

print(cos_data_T.head())


cos_data_T.to_csv('../../out/cos_A01B_all.csv')

print('数据转换完成! 耗时：%fs!' % (time.time() - time_initial))
