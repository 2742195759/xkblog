---
layout : post
title  : Referit 添加 Attribute
date   : 2021-02-22 09:00:00 +0000
category : DL
typora-root-url: ../../../code
---

#### 1. ReferitDataset 添加 Attribute 信息

##### 		使用Dataset Transformer 的方式来添加 Attribute

<font color='red'>TODO:</font>

目前提出的方法是，使用Transformer的方式添加Attribute，这样可以让代码各个部分更加简洁。不杂糅到一起。

1. 构造一个 DatasetTransformer，为原来数据集合中添加 raw_attrs 属性。并且格式和tokens的格式一样。便于重用原来的Tokenized代码
2. 构造几个新的DatasetTransformer包含Tokenized和Id化。
3. 按照顺序组建成为一个合理的TransformSequences。然后插入进去。就实现了。

⚠️： 注意，需要将Context所需的信息也加入到init里面去。比如Tokenize 需要 Dict 那么需要给出Dict在Context中的key name

#### 2. Referit Api 记录



