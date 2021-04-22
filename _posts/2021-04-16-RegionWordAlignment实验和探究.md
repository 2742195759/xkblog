---
layout : post
title  : Region Word Alignment 实验和探究
date   : 2021-04-14 15:12:00 +0000
category : phraseground
typora-copy-images-to: ../../../code/xkblog/public/img/
typora-root-url: ../../../code
---

##### 问题定义

本文主要研究Word2Region层面的grounding。当给定一个句子和一个视觉区域的匹配关系，如何挖掘出句子中的单词对视觉区域的对应关系。
$$
输入数据：训练样本为(W,V,i)。其中W为R^{D \times N}, V为R^{E \times M}。其中D和E为特征维度。 \\
测试过程：每个W_{i}和V中的对应概率。 \\
期望目的：训练之后可以对W_{i}中的名词寻找到正确的视觉对应关系。\\
评价指标：使用什么指标来衡量正确性。
$$


评价指标：??? 人工查看 ??? 选100个图片自己标 ?



##### XKLIB / RefCOCO数据集

使用数据集配置：

```python
    DATASETS=dict(
        DATA_ROOT="/home/data/dataset", 
        TRAIN=("referitfast_refcoco_unc_train", ),
        TEST=("referitfast_refcoco_unc_test", ),
        IMAGE_ONLY=False, 
        EVAL_TYPE="phrasegrounding", 
        PHRASE_GROUNDING=dict(
            TRAIN_PROPOSAL_ROOT="/home/data/Output/FrcnProposal/proposal-0.2-train", 
            TEST_PROPOSAL_ROOT="/home/data/Output/FrcnProposal/proposal-0.2-test", 
            #TEST_PROPOSAL_ROOT="/home/data/Output/FrcnProposal/proposal-0.08-train", 
        ),
        NUM_NEG_REGION=3,  # 一个正样本对应多少个负样本
        SAMPLE_RATIO=0.5,  # 采样同一个Image内的Region的概率
        TEST_TYPE='det',    # when in the test model, use the FrcnProposals
    ),
```

记录一下实现的过程的函数：

```sh
>>> batched_input['props_ins']._fields['features'].shape
torch.Size([3, 256, 7, 7]) #表示了上述的V一部分，Proposals部分

>>> batched_input['gt_ins']#表示了上述的V一部分，gt部分。
torch.Size([1, 256, 7, 7])

>>> batched_input['token_ids'] # 表示了word seq的id, 7是终止符号
tensor([  1, 530,  16,  27,   7,   7,   7,   7,   7,   7,   7,   7,   7,   7,
          7])
```

##### 理解