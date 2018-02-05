#!/usr/bin/python
# coding=utf-8

"""
    家庭作业代码实现
"""


def homeWorkClassTest():
    trainingFile = '../data/training.data'
    testFile = '../data/test.data'

    f = open(trainingFile)
    t = open(testFile)

    trainingData = [inst.strip().split(',') for inst in f.readlines()]

    testingData = [inst.strip().split(',') for inst in t.readlines()]

    print(trainingData)




if __name__ == '__main__':
    homeWorkClassTest()
