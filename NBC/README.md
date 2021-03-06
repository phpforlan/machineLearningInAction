生活中很多场合需要用到分类，比如新闻分类、病人分类等。本次分享介绍朴素贝叶斯分类器(Naive Bayes Classifier)，
它是一种简单有效的常用分类算法。

阮一峰老师: http://www.ruanyifeng.com/blog/2013/12/naive_bayes_classifier.html

朴素贝叶斯分类器的基本方法: 在统计资料的基础上，依据某些特征(假设特征之间是相互独立的)，计算各个类别的概率，从而实现分类。

# 一、什么是贝叶斯理论
1. 频率派观念
事情发生的频率是一定的（虽然可能算不出来，但是是确定的一个值），然而，样本空间却是是不确定的，因此只需要关键样本分布即可。

2. 贝叶斯派观念
参数是随机的(会产生变化)，而样本却是固定的，因此需要重点关注参数估计。

为了估计参数，就需要先知道参数的无条件分布，也就是说在有样本之前，参数是什么样的。

先验分布π(0) + 样本信息X  => 后验分布π(0|x)

# 二、贝叶斯公式
贝叶斯定理是根据条件概率得到的

P(A|B) = ( P(B|A)P(A) ) / P(B)

解释: P(A|B)表示在事件B已经发生的条件下，事件A发生的概率。

1. 贝叶斯定理推断过程: http://www.ruanyifeng.com/blog/2011/08/bayesian_inference_part_one.html
2. 条件概念百度百科: https://baike.baidu.com/item/%E6%9D%A1%E4%BB%B6%E6%A6%82%E7%8E%87/4475278?fr=aladdin
3. 朴素贝叶斯分类器的应用: http://www.ruanyifeng.com/blog/2013/12/naive_bayes_classifier.html

案例一、贝叶斯定理病人分类的例子:
```
    症状　　职业　　　疾病

　　打喷嚏　护士　　　感冒
　　打喷嚏　农夫　　　过敏
　　头痛　　建筑工人　脑震荡
　　头痛　　建筑工人　感冒
　　打喷嚏　教师　　　感冒
　　头痛　　教师　　　脑震荡
```

```
问题: 现在又来了第七个病人，是一个打喷嚏的建筑工人。请问他患上感冒的概率有多大？
B => 打喷嚏x建筑工人(条件)
A => 感冒(要发生的事件)

根据贝叶斯定理可得:
    P(感冒|打喷嚏x建筑工人)
    　　　　= P(打喷嚏x建筑工人|感冒) x P(感冒)
    　　　　/ P(打喷嚏x建筑工人)

假定"打喷嚏"和"建筑工人"这两个特征是独立的，因此，上面的等式就变成了

P(感冒|打喷嚏x建筑工人)
　　　　= P(打喷嚏|感冒) x P(建筑工人|感冒) x P(感冒)
　　　　/ P(打喷嚏) x P(建筑工人)

最后计算: P(感冒|打喷嚏x建筑工人) = 0.66x0.33x0.5/(0.5x0.33) = 0.66 因此这个打喷嚏的建筑工人，有66%的概率是得了感冒
```

```
核心: 下一步我们来推算朴素贝叶斯分类器的公式
假设某个体有n项特征，分别为F1、F2、F3、...、Fn。现在有m个类别，分别为C1、C2、...、Cm。贝叶斯分类器就是计算出概率最大的那个分类，也就是
求下面这个算式的最大值:
    P(C|F1F2...Fn)
    　　= P(F1F2...Fn|C)P(C) / P(F1F2...Fn)
解释: 在F1、F2,...,Fn这些特征的条件下，属于类别C的概率。

由于 P(F1F2...Fn) 对于所有的类别都是相同的(特征之间是相互独立的，每个特征发生的概率是一样的)，可以省略，问题就变成了求:
  P(F1F2...Fn|C)P(C) 的最大值。

so,朴素贝叶斯分类器则是更进一步，假设所有特征都彼此独立，因此:
P(F1F2...Fn|C)P(C) = P(F1|C)P(F2|C) ... P(Fn|C)P(C)
上式等号右边的每一项，都可以从统计资料中得到，由此就可以计算出每个类别对应的概率，从而找出最大概率的那个类。

备注: 虽然"所有特征彼此独立"这个假设，在现实中不太可能成立，但是它可以大大简化计算，而且有研究表明对分类结果的准确性影响不大。
```

```
上面讲了朴素贝叶斯分类器的推导计算过程，可能还是比较模糊，那么我们用一个"帐号分类"的例子来讲明白。

案例二、账号分类
根据某社区网站的抽样统计，该站10000个账号中有89%为真实账号（设为C0），11%为虚假账号（设为C1）。其中C0 = 0.89，C1 = 0.11

接下来，就要用统计资料判断一个账号的真实性。假定某一个账号有以下三个特征：
       F1: 日志数量/注册天数
　　　　F2: 好友数量/注册天数
　　　　F3: 是否使用真实头像（真实头像为1，非真实头像为0）

问题：现在一个新用户的实际特征值如下: F1 = 0.1，F2 = 0.2，F3 = 0，请问该帐号是真实帐号还是虚假帐号？
解答：
  根据上面推导的公式，当然我们要计算P(F1|C)P(F2|C)P(F3|C)P(C)的值，得到对应C0、C1的概率，以概率大的为准。

虽然上面这些值可以从统计资料得到，但是这里有一个问题：F1和F2是连续变量，不适宜按照某个特定值计算概率。
一个技巧是将连续值变为离散值，计算区间的概率。比如将F1分解成[0, 0.05]、(0.05, 0.2)、[0.2, +∞]三个区间，然后计算每个区间的概率。
在我们这个例子中，F1等于0.1，落在第二个区间，所以计算的时候，就使用第二个区间的发生概率。

根据统计资料，可得:
    P(F1|C0) = 0.5,     P(F1|C1) = 0.1
　　P(F2|C0) = 0.7,     P(F2|C1) = 0.2
　　P(F3|C0) = 0.2,     P(F3|C1) = 0.9

因此:

P(F1|C0) P(F2|C0) P(F3|C0) P(C0)
　　　　= 0.5 x 0.7 x 0.2 x 0.89
　　　　= 0.0623

P(F1|C1) P(F2|C1) P(F3|C1) P(C1)
　　　　= 0.1 x 0.2 x 0.9 x 0.11
　　　　= 0.00198

=> 可以看到，虽然这个用户没有使用真实头像，但是他是真实账号的概率，比虚假账号高出30多倍，因此判断这个账号为真。

```

1. 在事件B发生前，我们需要对事件A发生的概率有一个粗略的判断，也就是事件A的先验概率P(A)。（不依赖于B事件，A事件发生的概率）

2. 在事件B发生后，我们可以对P(A)进行一个修正，变成后验概率P(B|A)

# 三、贝叶斯决策论(BDT: Bayesian Decision Theory)
基于事物发生的概率进行决策的基本方法。在分类任务中，BDT通过最小化误判损失来选择最优的类别。(使误判损失最小)

针对类别i的误判风险为: (公式)

# 四、朴素贝叶斯分类器的原理
1. 属性独立假设
从贝叶斯公式中可以看出，如果样本属性独立地对分类结果有影响，可推算出对应的公式。

2. 样本同分布假设
样本的分布与属性无关

3. 类的先验概率估计

4. 样本属性的条件概率的估计

# 五、朴素贝叶斯实现步骤
1. 数据预处理，计算各个属性出现的次数
2. 统计概率，计算各属性的条件概率和类别的边缘概率
3. 缺失值处理，一般使用拉普拉斯平滑
4. 构建朴素贝叶斯模型，对测试集进行预测

# 参考资料:
* 带你搞懂朴素贝叶斯分类算法: http://blog.csdn.net/amds123/article/details/70173402
* 1小时入门朴素贝叶斯: http://www.chinahadoop.cn/course/985/learn#lesson/18484
* 机器学习从入门到放弃之朴素贝叶斯: https://segmentfault.com/a/1190000006244439
* 朴素贝叶斯分类器的应用: http://www.ruanyifeng.com/blog/2013/12/naive_bayes_classifier.html