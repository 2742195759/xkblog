---
layout : post
title  : pg实验2-MattNet的Dataloader逻辑
date   : 2021-03-02 20:33:00 +0000
category : phraseground
typora-copy-images-to: ../../../code/xkblog/public/img/
typora-root-url: ../../../code
---

## 前置实验

本实验上接 [XKBlog/pg实验1](/xkblog/phraseground/2021/02/26/pg%E5%AE%9E%E9%AA%8C1.html)，目前还是对MAttNet复现。今天的实验已经复现成功。发现MAttNet其实主要就是对DataLoader这个点的理解。如果使用了MAttNet相同的DataLoader（GT-Dataloader），确实可以得到 80% 左右的acc1。但是这样的结果确实是有点失望，毕竟这个属于EasyEval，不切合实际。<font color='green'>但是得到了启发，训练过程确实可以从更好的GT中获益。因此区分Train和Test，使得他们不完全一样，在Train过程中多使用GT可以提高模型的训练效果。而且需要多关注DataLoader，因为这个东西对效果的提升比模型对效果的提升大的多。Model可以随便看看，但是如果复现论文出现了很大的不一致，重点排查DataLoader先。</font>

当前复现阶段是：SubJectModel + DataLoader + NegativeSample + MaxMarginLoss，达到了 80.4% 的精度。

下一步还需要添加：LocationModel + RelationModel 两个部分，就是完全体的MattNet，理论上应该到 85%的精度。

## MattNet中的GT-Dataloader

#### 背景：

使用了 Max-Margin Loss 之后，发现效果反而变的不行了。而且怎么调都调不上去。个人感觉有点问题，但是阅读了MattNet源码和自己的源码，没有发现任何问题，所以觉得有可能是数据集准备的问题。然后看了源码的 gt_mrcn_loader.py文件，发现确实和自己的实现有点不同。

#### MattNet源码中GT-Dataloader逻辑：

***训练阶段***

首先是一个ImageBatch，一个是InnerImageBatch。每个Batch是ImageBatch * InnerImageBatch。选择ImageBatch个图片（遍历所有的refcoco数据集中的图片），然后对每个图片找到所有的refids（每个Refid就是一个Referred物体），然后对每个Refids找到InnerImageBatch个sent_id。这样我们得到了一个(ref_id, sent_id) 的对。个数是 #AllReferid * InnerImageBatch。然后进行采样。获取到候选的Proposals

采样和负采样的时候，不进行FasterRCNN Proposal的提取，而是直接把 GT 中的Box作为Proposals。 <font color='green'>这样的话，当然会精度更高了，因为相当于我们可以找到所有的正确Proposals，我们可以理解所有可疑的Proposals，并且这样也有助于我们发现他们的关系。换个角度，我们相当于进行了ImageCrop-Sentence搜索任务！！</font>

所以他和现在Referit-fast最大的区别在于，只是用 Annotations中的Proposals，而后者使用FasterRCNN方法预测出Proposals作为候选框。在MattNet中，FasterRCNN只是作为GT-DataLoader的特征提取预处理过程。

***预测阶段***

预测阶段其实也有区别，源码中的easy_eval阶段也是使用一样的方法，只是所有的候选Proposals变成了本图片所有的ann_ids的图片。也就是和ImageCrop-Sentence搜索任务一样了。

<font color='red'>值得注意的是，作者不是特意使用这个方法来欺骗，应该是这个方法是和之前的论文保持一致的。使用这样的Loader会得到比较高的结果，因为Frcn中的bias被直接消除了。而且Eval的过程中也是使用到了Gt的信息。作者实现了非GT版本的，在eval_det.py中，这个Loader对应在det_loader.py中，这个Loader应该就是使用Frcn预测的结果作为Gt来实现的。但是训练的时候，使用gt_mrcn_dataloader确实没有啥毛病，这样可以让模型更加专注于模型中自己处理的部分，消除了bias可以让学习效果更加好。虽然会有数据漂移的风险。（Train Eval的分布不同）</font>

#### 实现细节：

通过3-4h的添加和实现，重构了代码的同时，将EasyEval的代码逻辑复刻到了cvpack2/referit_fast.py里面。其中的AddEasyProposal存放的就是逻辑代码。所谓的Easy就是表示所有的Proposal都来自于GT Boxes，而不是从DetectionModel中输出的。然后原来的逻辑放到了 DatasetTransformer_AddFrcnProposal下面。所以我们可以在两者中随意选择一个来作为Proposal的属性。

1. GT作为Proposals （DONE）
2. 负采样方案为同一个图片 + Global采样 （DONE）
3. 添加对同一个Region加入多个负采样样本。同时引入 same_image_ratio作为采样同一个图片的概率。 = 3。同时在MattNet的forward中兼容多负样本。（DONE）

#### 深入细节：

1. 发现一个奇怪的现象： batch的个数会影响结果。后来发现是BatchNorm1d导致的，这个模块会因为batch个数的不同而不同。所以下次发现这种问题不要慌张
2. dropout层灰导致每次传播的数值都不一样，这个也很正常。但是对于调参数来说，Dropout层不是很好，因为他会影响模型的结果，使得输出结果是一个总体的分布。

#### 实验结果：

***(2/4)***

***epoch=6:*** [1h]

1. <font color='green'>Done</font>  **复现最高点**：<font color='green'>sub + attr + no-batchnorm + no-dropout + 3 neg + 0.5 sample ratio</font>

| acc@1 | acc@5 | acc@10 | acc@1000 |
| :---: | :---: | :----: | :------: |
| 0.804 | 0.999 | 1.000  |  1.000   |

2. <font color='green'>Done</font> 继承1 + no normalized(matcher)  【cosine 似乎和 dot差不多。所以两个其实差不多！】：

   | acc@1 | acc@5 | acc@10 | acc@1000 |
   | :---: | :---: | :----: | :------: |
   | 0.797 | 0.998 | 1.000  |  1.000   |

3. <font color='red'>Done</font> 继承1 + with BN【MattNet-BN】 【确认问题是否是BN引起的？单因素变量！】：观察到 train-acc会很容易到1.0，确实有点问题。而且BoxLoss = 0.000 了，这表明模型应该是通过BN找打了某种捷径。

   | acc@1 | acc@5 | acc@10 | acc@1000 |
   | :---: | :---: | :----: | :------: |
   | 0.533 | 0.990 | 1.000  |  1.000   |

4. <font color='red'>Doing</font> RandomSelect模型，随机选择一个GT-Proposals作为输出，看EasyEval的结果 【看看我们的任务难度，是否50%是最基本的baseline？因为MattNet-BN就是50%左右？看看这个50%是不是最容易得到的结果。】[具体实验](#RandomSelect 模型在 EasyProposal 上的测试)

#### 实验结论：

BN层不是所有的情况下都会有作用。例如在这个任务中，添加了BN层和没有添加BN层是完全不同的效果（53% -> 80%）。几乎可以理解为，BN层导致网络出了很大的问题。

<font color='green'>总结一下我是如何寻找到BN层的问题的：</font>首先是我发现在训练过程中，train-acc 确实很大，几乎所有的都是1.0。（train acc就是正样本分数 > 负样本分数的样本比例）。因此首先想到的是过拟合。但是发现将训练好的模型在训练集合上Eval，效果也就是50%左右。这个现象很反常，因此我单步调试，发现batchsize的大小，会影响输出的大小。比如在bs=64下训练的模型，在bs != 64 的情况下，会出现很多负样本 > 正样本的情况。而这个 bs 不同影响输出的层就只有BN层了。然后将BN去掉，发现首先train-acc上升的没有那么异常，其次是效果提升巨大。因此BN层有问题无疑了。

<font color='red'>思考问题：为什么BN层在这个任务中对实验结果有如此大的阻碍呢？是不是因为BN层泄漏了某些信息导致的（回忆Contrastive Learning？）</font> 

## SCRC使用EasyProposals来测试

为了验证MAttNet对SCRC的改进大小，首先得让他们具有可比性。因此下一步将在EasyProposals数据集上面重新适配SCRC模型，看SCRC模型在EasyProposals DataLoader的情况下，会得到什么样的效果？

固定Epoch=6，其余采样和sample策略和MattNet保持一致。

#### 实验结果：

## RandomSelect 模型在 EasyProposal 上的测试

为了验证MattNet的具体效果，需要知道EasyProposals具体有多么Easy，所以我们创造了一个RandomSelect模型作为Baseline，然后评估这个RandomSelect模型在EasyProposals数据集上的测试结果。

#### 实验设计：

简单的设计就是，我们的RandomSelect是无参数模型，只包含Eval过程。在eval过程中，我们将随机选择Props的一个region作为最高scores，这样就得到了随机选择的效果。然后看准确率。

准确率需要和MattNet-BN模型进行对比，对比之后可以知道加入了BN的模型，是完全不行还是部分可行。预计结果应该低于 50%。

固定Epoch=6，其余采样和sample策略和MattNet保持一致。

#### 实验结果：

| acc@1 | acc@5 | acc@10 | acc@1000 |
| :---: | :---: | :----: | :------: |
| 0.398 | 1.000 | 1.000  |  1.000   |

## MattNet 调参实验

