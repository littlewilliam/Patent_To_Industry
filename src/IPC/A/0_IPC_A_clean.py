# coding=utf-8

__author__ = 'tianchuang'

# 将原始的A部下全专利信息进行规整,仅提取有用的[小类编码],专利标题与摘要信息,然后按小类名导出csv文件
# 先用windows 写字板打开,用UTF-8编码另存为导出
# Main_class  title  Abstract

# python 2.7.11
# python2.7 则需要以下转码
# import sys
# reload(sys)
# sys.setdefaultencoding( "utf-8" )

import pandas as pd
import time

time_initial = time.time()


# 读取IPC代码与描述
def read_IPC_code():
    print('开始读取IPC代码与描述')
    ipc_code = pd.read_csv('../../../res/A01/IPC_Comment.csv')
    l_ipc_code = []
    l_ipc = []

    for index, item in ipc_code.iterrows():
        code = item['code']
        # 此处为判断A部下的全部84个小类,可调整
        if code[0:1] == 'A':
            l_ipc_code.append(code)
            code = code + ' ' + item['describe']
            l_ipc.append(code)
            # print(code)
    print(l_ipc_code, '\n读取完毕')
    return l_ipc_code, l_ipc


l_ipc_code, l_ipc = read_IPC_code()

data_A = pd.read_csv('../../../res/A/A_162813_utf8.csv', encoding="utf-8", error_bad_lines=False)
data_A_3 = data_A[['Main_class', 'title', 'Abstract']]
# print(data_A_3.loc[2]['Main_class'][0:4])

for item in l_ipc_code:
    startTime = time.time()
    x = str(item)
    # if x=='A01C':
    #     break

    # print('创造新的表:')
    # new_data = pd.DataFrame(columns=('Main_class', 'title','Abstract'))
    # print(new_data)

    new_data = data_A_3[(data_A_3['Main_class'].str[0:4] == x)]
    # 仅提取出标题和摘要
    new_data = new_data[['title', 'Abstract']]
    new_data.to_csv('../../../res/A/clean/' + x + '.csv', index=False, encoding='utf-8')

    print(x, '提取完成! 耗时：%fs!' % (time.time() - startTime))

print('A部专利数据提取完成! 耗时：%fs!' % (time.time() - time_initial))
