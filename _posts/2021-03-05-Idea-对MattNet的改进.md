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

***为什么RelationModular效果不好：*** 首先

