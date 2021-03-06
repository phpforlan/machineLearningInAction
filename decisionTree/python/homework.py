#!/usr/bin/python
# coding=utf-8

"""
    家庭作业代码实现
"""

import operator
from math import log
import random

def createTree(dataSet, labels):

    #取出所有的label
    classList = [example[-1] for example in dataSet]

    if classList.count(classList[0]) == len(classList):
        return classList[0]
    # 如果数据集只有1列，那么最初出现label次数最多的一类，作为结果
    # 第二个停止条件：使用完了所有特征，仍然不能将数据集划分成仅包含唯一类别的分组。
    if len(dataSet[0]) == 1:
        return majorityCnt(classList)

    # 选择最优的列，得到最优列对应的label含义
    bestFeat = chooseBestFeatureToSplit(dataSet)

    # 获取label的名称
    bestFeatLabel = labels[bestFeat]

    # 初始化myTree
    myTree = {bestFeatLabel: {}}
    # 注：labels列表是可变对象，在PYTHON函数中作为参数时传址引用，能够被全局修改
    # 所以这行代码导致函数外的同名变量被删除了元素，造成例句无法执行，提示'no surfacing' is not in list
    del (labels[bestFeat])
    # 取出最优列，然后它的branch做分类
    featValues = [example[bestFeat] for example in dataSet]
    uniqueVals = set(featValues)
    for value in uniqueVals:
        # 求出剩余的标签label
        subLabels = labels[:]
        # 遍历当前选择特征包含的所有属性值，在每个数据集划分上递归调用函数createTree()
        myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet, bestFeat, value), subLabels)
        # print 'myTree', value, myTree
    return myTree


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

        for example in dataSet:

            featList = [example[i] for example in dataSet] #获取某一列特征的所有特征取值
            uniqueVals = set(featList)

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



def storeTree(inputTree, filename):
    import pickle
    # -------------- 第一种方法 start --------------
    fw = open(filename, 'w')
    pickle.dump(inputTree, fw)
    fw.close()
    # -------------- 第一种方法 end --------------

    # -------------- 第二种方法 start --------------
    with open(filename, 'w') as fw:
        pickle.dump(inputTree, fw)
    # -------------- 第二种方法 start --------------


def grabTree(filename):
    import pickle
    fr = open(filename)
    return pickle.load(fr)


def classify(inputTree, featLabels, testVec):
    # 获取tree的根节点对于的key值
    firstStr = inputTree.keys()[0]
    # 通过key得到根节点对应的value
    secondDict = inputTree[firstStr]
    # 判断根节点名称获取根节点在label中的先后顺序，这样就知道输入的testVec怎么开始对照树来做分类
    featIndex = featLabels.index(firstStr)
    # 测试数据，找到根节点对应的label位置，也就知道从输入的数据的第几位来开始分类
    key = testVec[featIndex]
    valueOfFeat = secondDict[key]
    #print '+++', firstStr, 'xxx', secondDict, '---', key, '>>>', valueOfFeat
    # 判断分枝是否结束: 判断valueOfFeat是否是dict类型
    if isinstance(valueOfFeat, dict):
        classLabel = classify(valueOfFeat, featLabels, testVec)
    else:
        classLabel = valueOfFeat
    return classLabel


def list2file(lists):
    txtName = "./result"
    f = file(txtName, "a+")
    writeFile = ''
    for item in lists:
        for i in item:
            writeFile = writeFile + str((i)) + ','
        writeFile = writeFile.strip(',') + '\n'
    f.write(writeFile)
    f.close()

def homeWorkClassTest():
    trainingFile = '../data/training.data'
    testFile = '../data/test.data'

    f = open(trainingFile)
    t = open(testFile)

    trainingData = [inst.strip().split(',') for inst in f.readlines()]
    testData = [inst.strip().split(',') for inst in t.readlines()]

    labels = ['buying', 'maint', 'doors', 'persons', 'lug_boot', 'safety']

    #生成树
    vehicleTree = createTree(trainingData, labels)
    storeTree(vehicleTree, 'vehicleTree.tree')

    testDataLen = len(testData)

    resArr = ['unacc', 'acc', 'good', 'vgood']
    for i in range(testDataLen):
        try:
            res = classify(grabTree('vehicleTree.tree'), ['buying', 'maint', 'doors', 'persons', 'lug_boot', 'safety'],
                       testData[i])
        except:
            randIndex = random.randint(0, len(resArr)-1)
            res = resArr[randIndex]

        testData[i].append(res)

    list2file(testData)


if __name__ == '__main__':
    homeWorkClassTest()
