# coding=utf-8

__author__ = 'tianchuang'

# 处理IPC类目,提取出名词和动词,IPC类目全文

import jieba
import jieba.analyse
import pandas as pd
import re
import time
import jieba.posseg as pseg

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

print('创造新的表:')
new_data = pd.DataFrame(columns=('code', 'describe'))
print(new_data)
n_all = ['n', 'nr', 'nr1', 'nr2', 'nrj', 'nrf', 'ns', 'nsf', 'nt', 'nz', 'nl', 'ng']
v_all=['v']
n_all=n_all+v_all
ipc_comment_data = pd.read_csv('../../../res/A/IPC_Comment_complete_A.csv')

i = 0
for index, item in ipc_comment_data.iterrows():
    startTime = time.time()
    print(item['code'])
    p_code=str(item['code'])
    s=item['describe']
    pattern = r'\（(.+?)\）'

    # ---------------------------------------------------------
    # 4-2删除专利括号内说明，同时保留含有原专利号说明
    content_brackets = re.findall(pattern, s)
    # print('所有括号内的内容\n', content_brackets)

    s = re.sub(pattern, '', s)
    # print('删除后\n', s)

    content_brackets_useful = ''

    for item_brackets in content_brackets:
        if p_code in item_brackets:
            content_brackets_useful += item_brackets + '.'

    # print('所有括号内的应该保留的内容\n', content_brackets_useful)

    s = s + '.' + content_brackets_useful
    # print('最终的注释说明\n', s)
    # ---------------------------------------------------------


    #若4-1删除专利括号内说明,将括号内的都删除
    # s = re.sub(pattern, '', s)

    words_p = pseg.cut(s)
    word_list = []

    for w, flag in words_p:
        if flag in n_all:
            word_list.append(w)

    new_data.loc[i] = None
    new_data['code'].loc[i] = item['code']
    new_data['describe'].loc[i] = word_list
    i += 1

    print(item['code'], '转换完成')
    print('耗时：%fs!' % (time.time() - startTime))

    if item['code'] == 'A99Z':
        break

new_data.to_csv('../../../res/A/IPC_Comment_complete_A_list_n.csv', index=False, index_label='index')

print('完成! 耗时：%fs!' % (time.time() - time_initial))
