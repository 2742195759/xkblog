---
layout : post
title  : PairWise Phrase Attention方法
date   : 2021-04-25 16:00:00 +0000
category : phraseground
typora-copy-images-to: ../../../code/xkblog/public/img/
typora-root-url: ../../../code
---

#### 背景

1. 发现SCAN的Stack Cross Attention方法可以学习到很好的对应关系，78%GT精度左右，然后case study中可以看到很好的效果。

2. case study 中，单纯的SCAN方法虽然效果不错，但是如果直接将分数进行累加，容易出现覆盖情况：

3. ***<font color='blue'>覆盖现象！</font>***：man in black，因为man比较多，black比较少，所以man的权重会普遍高于black，因此man会起到决定性的作用，但是其实应该是black起到决定性的作用。man in black，如下case：

   <img src="/xkblog/public/img/截屏2021-04-25 下午9.51.03.png" alt="截屏2021-04-25 下午9.51.03" style="zoom:30%;" />

4. 如果将LSTM得到的hidden vector作为keys，然后LSTM的输入word emb作为values，regions作为query，可以得到一个attention方法，这个方法通过建模$P(W_i|S,R)$条件概率来作为Attention。效果是 80%左右

5. 分析得到，对于不同的pair来说，单词的重要性其实应该不同才对。所以引入对$P(R_1 > R_2|S)$的建模，通过这个概率来进行计算。加权。

#### 算法整体框架

1. Eval阶段统一成为$O(n^2)$的复杂度：针对所有的regions，设置为regions pair。inference的时候，首先将proposals的pairs展开为$n^2$个pairs，然后对每个pairs计算attention，然后进行加权，计算两个的得分差。然后使用BPR-LOSS来作为概率统计。最后+率最大的作为最终的形状。由于使用了BPR-LOSS，因此不使用Cosine Similarity。而是使用dot作为结果



$P(R_1 \gt R_2|S) = \mathbf{Sigmoid}(\mathbf{Score}(R_1,R_2,S) - \mathbf{Score}(R_2,R_1,S))$

$\mathbf{Score}(R_1,R_2,S) = \mathbf{CM}({\mathbf{PhraseAttention}(R_1,R_2,S)}, R)$

文字表示就是，首先计算一个Score的分值，从[-inf, inf]。这个输出表示logits。然后通过两个Region对S的每个word进行一个PhraseAttention。目的是使的不同的单词的重要性随着R的不同而不同。CM是跨模态的评分函数。

```python
def PhraseAttention(R1, R2, S):
		"""输入R1和R2两个区域的特征，S是文本的特征
		   输出vector表示最后的文本Attention之后的文本向量。
		"""
		return 
  
def CM(textual_vec, visual_vec):
  	"""输入文本的向量和视觉的向量
  	   输出两个向量的评分。[-inf, inf]
  	"""
    
def BPR_LOSS(S1, S2):
  	return -ln(sigmoid(S1-S2))
```

#### 实验设计

