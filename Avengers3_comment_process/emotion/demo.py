from collections import defaultdict
import matplotlib.pyplot as plt
import pandas as pd
import numpy as nm
import os
import re
import jieba
import codecs
"""
1.对文本进行切割
"""
def sent2word(sentence):
    """
    将语句进行分词
    """
    segList = jieba.cut(sentence)
    segResult = []
    for w in segList:
        segResult.append(w)
    fh = open('stop_words.txt')
    stopwords = fh.readlines()
    newSent = []
    for word in segResult:
        if word in stopwords:
            # print "stopword: %s" % word
            continue
        else:
            newSent.append(word)
    return newSent


"""
2. 情感定位
"""


def classifyWords(wordDict):
    # (1) 情感词
    rm = open('BosonNLP_sentiment_score.txt','rb')
    senList = rm.readlines()
    senDict = defaultdict()
    for s in senList:
        s = s.decode()
        if s.strip() != '':
            senDict[s.split(' ')[0]] = s.split(' ')[1]
    # (2) 否定词
    rn = open('not_words.txt')
    notList = rn.readlines()
    # (3) 程度副词
    rd = open('degree_words.txt')
    degreeList = rd.readlines()
    degreeDict = defaultdict()
    for d in degreeList:
        if d.strip() != '':
            degreeDict[d.split(',')[0]] = d.split(',')[1]
    senWord = defaultdict()
    notWord = defaultdict()
    degreeWord = defaultdict()

    for word in wordDict.keys():
        if word in senDict.keys() and word not in notList and word not in degreeDict.keys():
            senWord[wordDict[word]] = senDict[word]
            #print(wordDict[word])
        elif word in notList and word not in degreeDict.keys():
            notWord[wordDict[word]] = -1
            #print(word)
        elif word in degreeDict.keys():
            degreeWord[wordDict[word]] = degreeDict[word]
    #print(senWord.keys())
    return senWord, notWord, degreeWord


"""
3. 情感聚合
"""


def scoreSent(senWord, notWord, degreeWord, segResult):
    W = 1
    score = 0
    # 存所有情感词的位置的列表
    senLoc = senWord.keys()
    notLoc = notWord.keys()
    degreeLoc = degreeWord.keys()
    senloc = -1
    # notloc = -1
    # degreeloc = -1
    #print(senLoc)
    # 遍历句中所有单词segResult，i为单词绝对位置
    for i in range(0, len(segResult)):
        # 如果该词为情感词
        if i in senLoc:
            # loc为情感词位置列表的序号
            senloc += 1
            # 直接添加该情感词分数
            score += W * float(senWord[i])
            # print "score = %f" % score
            if senloc < len(senLoc) - 1:
                # 判断该情感词与下一情感词之间是否有否定词或程度副词
                # j为绝对位置
                for j in range(list(senLoc)[senloc], list(senLoc)[senloc + 1]):
                    # 如果有否定词
                    if j in notLoc:
                        W *= -1
                    # 如果有程度副词
                    elif j in degreeLoc:
                        W *= float(degreeWord[j])
        # i定位至下一个情感词
        if senloc < len(senLoc) - 1:
            i = list(senLoc)[senloc + 1]
    return score
"""
保存数值
"""
def savedata(texts):
    wirte_flag = True
    path = 'fulian_content_score.txt'
    with open(path, 'a', encoding='utf-8') as f:
        f.writelines(texts+'\n')
        f.close()

"""
4.对结果进行分析处理
"""
def analysitdata(score_disc):
    average = nm.average(score_disc)
"""
读取妇联3影评进行情感分析
"""
fulian = pd.read_csv("fulian_content.csv",encoding = 'gb18030')
score_disc = []
for each in fulian.iterrows():
   sentence = str(each)
   SegResult = sent2word(sentence)
   SegResult_dist = {}
   i =0
   for word in SegResult:
       SegResult_dist[word] = i
       i=i+1
   senWord, notWord, degreeWord = classifyWords(SegResult_dist)
   score = scoreSent(senWord, notWord, degreeWord, SegResult)
   score_disc.append(score)
   score_str = str(score)
   texts = str(each)+","+score_str
   #savedata(texts)
list.sort(score_disc)
plt.scatter(list(range(0,len(score_disc))),score_disc)
plt.show()
