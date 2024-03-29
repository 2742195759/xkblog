---
layout : post
title  : IDEA-对MattNet的几个改进想法
date   : 2021-03-05 01:00:00 +0000
category : phraseground
typora-copy-images-to: ../../../code/xkblog/public/img/
typora-root-url: ../../../code
---

#### 前言

有了[MattNet复现完整实验](https://2742195759.github.io/xkblog/phraseground/2021/03/04/pg%E5%AE%9E%E9%AA%8C3.html)，并且到达了和文章中差不多的精度，接下来的目的就是改进MattNet。本文将包含三种标题，只按照时间顺序给出。第一个是基于MattNet的现存改进方法（命名为：现状+id），以及对现在MattNet的一些观察（命名为：观察+id），观察一般都是一些问题和改进点。还有就是对MattNet的原始改进方法（命名为：想法+id）。

#### 观察1

<font color='red'>观察1: MattNet模型包含3个模块：Sub + Loc + Rel。但是根据作者给出的Demo来看，Rel对结果的贡献很小！说明Rel模型设计存在不合理的成分。</font>

见作者给出的demo网址，[MattNet Demo](http://vision2.cs.unc.edu/refer/comprehension)。可见，任意给出一个表达式，几乎Rel 的score都很小。同时实验也表明添加了Rel模块其实对实验结果的影响很小（都是84%左右波动）。所以Rel模块肯定是存在不合理的成分。

***那么如何设计更好的Rel？是一个可以改进的点。***下图是一个示例表明了Rel Weight很小：

<div align='center'><img src="/xkblog/public/img/截屏2021-03-05 上午1.05.43.png" alt="截屏2021-03-05 上午1.05.43" style="zoom:50%;" /> </div>

#### 观察2

<font color='red'>观察2: 现在的完全MattNet网络，其实对于Max-Margin Loss已经"快走到头了"。可以从下图的train-acc看出，box-loss以及很小，同时训练过程中的acc也是非常小。所以其实网络几乎对大部分的训练样本都可以很好的区分。 </font>

![截屏2021-03-05 上午1.07.43](/xkblog/public/img/截屏2021-03-05 上午1.07.43.png)

按照目前的想法来看，这个观察点带来的启发和行为是：

1. ***更换Loss***。主要目的就是使用非样本平衡Loss来对hard / easy样本进行不同程度的加权，使得Hard样本比重更高。
2. ***打印出训练集合中无法正确分类的样本，可视化一下，看看到底是什么原因引起的。***

#### 想法1

***现在有一个想法，就是自适应 Modular Network。给出足够的信息，然后设计好Attention网络。让模型自己学习合适的Modular，并且利用相应的信息。最后的分数还是使用各种模块汇总。但是可以吧Sub和Loc这两个有效模块单独拎出来。***

这个方法很有潜力。利用关键在于如何设计模型可以利用的输入。然后如何给他们进行链接！

#### 想法2

对MattNet Attention有效性的一个感性思考：

MattNet其实主要就是使用“限制连接”的思想来增强模型效果。所谓限制连接就是通过删除某些单元的连接来为模型添加 Inductive Bias，使得模型可以在更小的样本上得到比较好的结果。

但是与之相对的是增广连接的思想。通过增加信息，并且将信息于现有模块增加连接。然后达到利用更多信息的目的。

在具有同样信息的前提下，限制连接应该是更好的方法，但是前提必须要有效的限制。因为通过有效的限制连接，我们可以让模型具有更多的先验知识，然后这些连接会让模型有更大的概率收敛到我们预先设定的先验上。

举个例子：如果对于Loc和Sub两个模块，本来我们具有以下几个信息：

<div align='center' height=100px width=100px><img src="/xkblog/public/img/image-20210305165930143.png" alt="image-20210305165930143" style="zoom:50%;" /><img src="/xkblog/public/img//image-20210305170037984.png" alt="image-20210305170037984" style="zoom:50%;" /></div>

通过上述的比较，我们发现ModularNetwork的优点在于，我们使用先验知识将不同特征的作用域***显示*** 的划分了。例如在Sub模型中，我们的目的只找到phrase指向的主要物体，所以我们不考虑Loc的信息，这样对于Sub模型来说，减少了位置信息和Context信息的使用，这样会让Sub和Phrase具有更加明确的对应关系。同理，对于Loc信息来说，我们只是用了SpatialFeature，因此当位置信息和某一个词语出现同时出现的概率很高时（强相关 / 协方差很大），我们的模型将会给该词语对该SpatialFeature更高的权重。上述的过程，其实也就是各个Modular模型学习的主要过程了。

***1. 为什么RelationModular权重普遍偏低：*** 首先对数据集观察，发现存在异样Category物体的训练样本很少，大多数都是同类。这个是导致RelAttScore很低的原因，因为存在mask，多数样本mask=0，这样的话Rel模块不会被训练到，所以其实本质上还是一个数据不平衡的问题导致Softmax偏重于占比大的Modular。

<font color='red'>验证上述1的想法： </font>

实验基本表明原因是正确的。因为打印出了三种不同的Score随着时间的变化，发现score-rel一直都是0左右。说明很多的region没有不同category的surroundings。这样的话，mask的存在会导致score=0。然后 rel模块中的参数长期得不到训练，保持一个较小的数值（因为sub和loc就是从0.01开始上升的，所以初始化的数值都是很小的。）

所以不可以认为是因为RelationModualr设计不合理导致的，而是数据不平衡导致训练不充分导致的。【这个问题在Self-Adapted Modular Network中也需要解决】

#### 想法3

<font color='red'>一些初步的想法：</font>

***Self-Grouping Network***：自组合网络主要的思想就是，利用文本的组合性质，然后不直接对单词属性进行

***Gated FC-Network***：Gated FCN主要的思想是，自适应的连接限制网络。唯一不同的是将Weight变成了计算出来的一个scalar

#### 观察3

***important***

【DONE】打印出预测不准确的 Image-Sentence Pair，找出预测不准确的原因。

通过在visual tool中添加了filter，只筛选出所有预测误差IOU < 0.5 的物体，我们得到了如下的一下观察和猜想： 

1. MattNet对于不同物体关联没有很好的建模：（on the floor之类的。因为Relation模块没有被很好的学习！）
2. 非通用词汇 / Implict词汇怎么办？低频率Vocabulary是一个难以处理的点。（可以参考zero-shot learning？）：例如MattNet模型可以很好的理解woman，但是却无法理解 Bikini / 卡其裤之类的词语。
3. 远近关系，3D关系没有很好的被理解：例如Closest to the camera / on the floor 等之类的。
4. 多个物体之间的关系：例如 3rd 之类的。laptop right to the cat。相对关系没有找准，right会默认寻找global right，而不是cat的right。
5. 利用物体的部位 / 例如Hand /  Ass / Butt 或者是衣服上的某一个图标之类的。难以定位。

【TODO1】编写工具，可以查看training数据集中，某个词出现在句子中的句子个数。用来看是否是low frequency words

【TODO2】由于PhraseAttention模块只与Tokens相关。可以编写工具，对所有训练集合中的句子经过PhraseAttention后，将所有的单词按照Threshold分类，然后查看sub/rel/loc三类对应的词汇分别是什么。

【DONE】编写输出函数：包含图像和inner box的attention featmap。然后展示出图像的attention部分。

<img src="/xkblog/public/img/截屏2021-03-09 上午1.33.47.png" alt="截屏2021-03-09 上午1.33.47" style="zoom:50%;" />

【TODO3】对word embedding进行TSNE，观察 battle / player / man / dudy 之类的语言是否具有相似的Embedding，如果不具有相似embedding，那么这个就是一个改进点。（同义词转换模块）