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



##### sents.json 文件格式

```
>>> ttt.__len__()
142210

>>> ttt[0]
{'parse': {'parsetree': '(ROOT (NP (NP (DT the) (NN lady)) (PP (IN with) (NP (DT the) (JJ blue) (NN shirt)))))', 'text': 'the lady with the blue shirt', 'dependencies': [['root', 'ROOT', '0', 'lady', '2'], ['det', 'lady', '2', 'the', '1'], ['det', 'shirt', '6', 'the', '4'], ['amod', 'shirt', '6', 'blue', '5'], ['prep_with', 'lady', '2', 'shirt', '6']], 'words': [['the', {'CharacterOffsetEnd': '3', 'CharacterOffsetBegin': '0', 'PartOfSpeech': 'DT', 'Lemma': 'the'}], ['lady', {'CharacterOffsetEnd': '8', 'CharacterOffsetBegin': '4', 'PartOfSpeech': 'NN', 'Lemma': 'lady'}], ['with', {'CharacterOffsetEnd': '13', 'CharacterOffsetBegin': '9', 'PartOfSpeech': 'IN', 'Lemma': 'with'}], ['the', {'CharacterOffsetEnd': '17', 'CharacterOffsetBegin': '14', 'PartOfSpeech': 'DT', 'Lemma': 'the'}], ['blue', {'CharacterOffsetEnd': '22', 'CharacterOffsetBegin': '18', 'PartOfSpeech': 'JJ', 'Lemma': 'blue'}], ['shirt', {'CharacterOffsetEnd': '28', 'CharacterOffsetBegin': '23', 'PartOfSpeech': 'NN', 'Lemma': 'shirt'}]]}, 'atts': {'r4': ['none'], 'r5': ['prep_with'], 'r6': ['shirt'], 'r7': ['none'], 'r1': ['lady'], 'r2': ['none'], 'r3': ['none'], 'r8': ['blue']}, 'sent_id': 0, 'tokens': ['the', 'lady', 'with', 'the', 'blue', 'shirt'], 'raw': 'THE LADY WITH THE BLUE SHIRT', 'sent': 'the lady with the blue shirt', 'left': [['blue', 'JJ']]}

>>> ttt[0]['atts']
{'r4': ['none'], 'r5': ['prep_with'], 'r6': ['shirt'], 'r7': ['none'], 'r1': ['lady'], 'r2': ['none'], 'r3': ['none'], 'r8': ['blue']}

## 其中的 sent_id 可以从 sentence 中得到
```



#### 2. Referit Api 记录



