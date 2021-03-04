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

***现在有一个想法，就是 自适应 Modular Network。给出足够的信息，然后设计好Attention网络。让模型自己学习合适的Modular，并且利用相应的信息。最后的分数还是使用各种模块汇总。但是可以吧Sub和Loc单独拎出来。***

这个方法很有潜力。利用关键在于如何设计模型可以利用的输入。然后如何给他们进行链接！

#### 想法2

对MattNet Attention有效性的一个感性思考：