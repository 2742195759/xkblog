---
layout : post
title  : Urwid源码阅读-Signal部分
date   : 2021-05-14 22:00:00 +0000
category : urwid
typora-copy-images-to: ../../../code/xkblog/public/img/
typora-root-url: ../../../code
---

#### Preface

这个系列的文章是阅读urwid源代码得到的总结，主要目的在于学习Python3的高级特征和达到对Urwid得心应手的程度。阅读代码的Urwid包的版本是2.1.2。

查看Urwid安装地址可以通过`pip3 show urwid`命令查看。

#### Signal 部分

***第一遍：功能性***

本小节主要是对Urwid Signal部分的阅读，对应源代码目录下的 signal.py 部分。约303行。



***第二遍：架构性***

