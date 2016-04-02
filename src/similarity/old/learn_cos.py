# coding=utf-8
__author__ = 'tianchuang'

import logging
# logging.basicConfig(format='%(asctime)s: %(levelname)s : %(message)s', level=logging.INFO)

from gensim import corpora, models, similarities
import jieba

jieba.initialize()
# python2.7 则需要以下转码
# import sys
# reload(sys)
# sys.setdefaultencoding("utf-8")

sentences = ["我喜欢吃土豆", "土豆是个百搭的东西", "我不喜欢今天雾霾的北京"]

words = []
for doc in sentences:
    words.append(list(jieba.cut(doc)))
print('分词结果:\n', (words))

dic = corpora.Dictionary(words)
print('字典:\n', (dic))
print('词或词组在字典中的编号:\n', (dic.token2id))

# for word, index in dic.token2id.items():
#     print (word + " 编号为:" + str(index))

corpus = [dic.doc2bow(text) for text in words]
print('向量空间模型格式的语料库:\n', (corpus))

tfidf = models.TfidfModel(corpus)

corpus_tfidf = tfidf[corpus]
# for doc in corpus_tfidf:
#     print('将用词频向量表示一句话变换成为用词的重要性(TF-IDF变换)向量表示一句话:\n', (doc))

vec = [(0, 1), (4, 1)]
print('vec是查询文本向量,0为吃，4为东西，所以vec这句话可以是["吃东西"]或者["东西吃"],vec:\n', (vec))
print('tfidf[vec]:\n', (tfidf[vec]))
index = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features=15)
sims = index[tfidf[vec]]
print('比较vec和训练中的三句话相似度:\n',list(enumerate(sims)))
sort_sims = sorted(enumerate(sims), key=lambda item: -item[1])
print(sort_sims)
print(sort_sims[0:1])

query = "我刚吃了土豆"
query_bow = dic.doc2bow(list(jieba.cut(query)))
print('查询词为:\n',query)
print('改为向量空间格式:\n',(query_bow))
sims = index[tfidf[query_bow]]
print('比较查询词和训练中的三句话相似度:\n',list(enumerate(sims)))
sort_sims = sorted(enumerate(sims), key=lambda item: -item[1])
print(sort_sims)
print(sort_sims[0:1])
