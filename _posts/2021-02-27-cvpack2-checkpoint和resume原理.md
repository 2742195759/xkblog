---
layout : post
title  : cvpack2-checkpoint和resume原理
date   : 2021-02-27 12:14:00 +0000
category : cvpack2
typora-copy-images-to: ../../../code/xkblog/public/img/
typora-root-url: ../../../code
---

#### Abstract：

本文章主要讲的是 xkcv 库中，checkpoint 和 恢复的逻辑。这里进行记录。

1. 如果设置了MODEL.WEIGHTS，那么默认会从这个检查点进行恢复。会将对应的名字进行匹配。恢复的Root是build_model返回的model。
2. WEIGHTS 没有设置 / = "" 。那么在训练的时候不会有检查点。但是如果 cvpack2_train --resume ，那么会从log下的last_checkpoint下的model_XXXX中进行读取。类似于将WEIGHTS设置为了last_checkpoint文件指向的那个文件。