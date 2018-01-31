#!/usr/bin/python
# coding=utf-8

'''
 决策树算法实现代码
'''

import operator
from math import log
from collections import Counter  # 按需导入


def createDataSet():
    """
        初始化基础数据集
        dataSet: 基础数据集
        Args: 无需输入参数
        Returns: 返回数据集和对应的label标签
    """

    dataSet = [
        [1, 1, 'yes'],
        [1, 1, 'yes'],
        [1, 0, 'no'],
        [0, 1, 'no'],
        [0, 1, 'no']
    ]

    labels = ['no surfacing', 'flippers']

    return dataSet, labels


def calcShannonEntropy(dataSet):
    """
        计算给定数据集的香农熵(也就是label的信息熵)
        Args:
            dataSet: 数据集
        Returns:
            返回每一组feature下的某个分类下，香农熵的信息期望
    """
    numEntries = len(dataSet) #计算参与训练的数据量

    #计算分类标签label出现的次数
    labelCounts = {}

    for featVec in dataSet:

        # 将当前实例的标签存储，即每一行数据的最后一个数据代表的是标签
        currentLabel = featVec[-1]

        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel] = 0

        labelCounts[currentLabel] += 1

    # 对于label标签的占比，求出label标签的香农熵
    shannonEntropy = 0.0
    for key in labelCounts:
        prob = float(labelCounts[key]) / numEntries

        # 计算香农熵，以2为底求对数
        shannonEntropy -= prob * log(prob, 2)

    return shannonEntropy


def splitDataSet(dataSet, index, value):
    """
        splitDataSet(通过遍历dataSet数据集，求出第index列且值为value的行)
        如果第index列的值等于value，则把当前行切分出来(去除这一列)
        Args:
            dataSet 数据集                   待切分的数据集
            index 第几列                     划分数据集的特征
            value 表示这一列的某个取值         需要返回的特征的值
        Returns:
            第index列中，值为value的数据集(满足条件的那些行)
    """

    retDataSet = []
    for featVec in dataSet:

        if featVec[index] == value:
            # [:index]表示前index行，即若 index 为2，就是取 featVec 的前 index 行
            reducedFeatVec = featVec[:index]

            # [index+1:]表示从跳过 index 的 index+1行，取接下来的数据
            reducedFeatVec.extend(featVec[index+1:])

            retDataSet.append(reducedFeatVec) # reducedFeatVec为切分后的数据

    return retDataSet


def chooseBestFeatureToSplit(dataSet):
    """
        选择最好的特征进行切分
        Args:
            dataSet 数据集
        Returns:
          bestFeature 最优的特征列
    """
    # 求数据集的总特征数(每列就是一个特征)
    numFeatures = len(dataSet[0]) - 1

    # label的信息熵(即数据集的香农熵)
    baseEntropy = calcShannonEntropy(dataSet)

    # 最优的信息增益值, 和最优的feature编号
    bestInfoGain, bestFeature = 0.0, -1

    for i in range(numFeatures):

        featvalueList = [] #存储某个特征的所有取值
        for example in dataSet:

            featvalueList.append(example[i])
            uniqueVals = set(featvalueList) #获取某一列特征的所有特征取值

            # 创建一个临时信息熵
            newEntropy = 0.0

            # 遍历某一列的value集合，计算该列的信息熵
            for value in uniqueVals:
                subDataSet = splitDataSet(dataSet, i, value)
                prob = len(subDataSet) / float(len(dataSet))
                newEntropy += prob * calcShannonEntropy(subDataSet) #条件熵

            infoGain = baseEntropy - newEntropy
            if(infoGain > bestInfoGain):
                bestInfoGain = infoGain
                bestFeature = i

    return bestFeature


def majorityCnt(classList):
    """
    在指定list中,选择出现次数最多的一个结果
    Args:
        classList label列的集合
    Returns:
        bestFeature 最优的特征列
    """

    classCount = {}
    for vote in classList:
        if vote not in classCount.keys():
            classCount[vote] = 0
        classCount[vote] += 1

    sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)

    return sortedClassCount[0][0]

dataSet, labels = createDataSet()
#shannonEntropy = calcShannonEntropy(dataSet)
#retDataSet = splitDataSet(dataSet,0,1)
#print(retDataSet)

#bestFeature = chooseBestFeatureToSplit(dataSet)
#print(bestFeature)

bestFeature = majorityCnt(['yes', 'no', 'yes'])
print(bestFeature)



