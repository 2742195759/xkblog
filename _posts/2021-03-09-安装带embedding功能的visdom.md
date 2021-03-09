---
layout : post
title  : Visdom-Embedding功能使用
date   : 2021-03-09 13:00:00 +0000
category : cvpack2
typora-copy-images-to: ../../../code/xkblog/public/img/
typora-root-url: ../../../code
---

visdom其实在 [issue611](https://github.com/fossasia/visdom/pull/611)中添加了对Embedding可视化的支持。但是如果想要使用这个功能，需要安装一些额外的依赖库，同时使用的文档其实也不多。所以这里总结一下，记录对visdom embedding的vis.embedding函数的使用，以及碰到的一些坑点。

#### 安装方法

如果是单纯的visdom传统功能，只需要很简单的pip install visdom来进行安装，同时使用 visdom 就可以打开服务器了。但是如果想要使用embedding功能，需要额外的几个步骤。

1. 从github库下载最新的visdom代码。（虽然版本一样，但是我做过尝试，如果使用pip自动安装的，显示界面会有问题，只要使用了vis.embedding函数，那么前端会报错，然后什么都显示不了。估计是有些前端没有更新啥的，虽然版本都是一样的：0.1.8.9）。下载的代码是：

   ```
   git clone https://github.com/fossasia/visdom
   ```

2. 下载完毕之后，启动服务器： 终端输入visdom命令即可，然后提示下载scripts，下载完毕之后就可以了。

3. 在客户端处，需要额外下载一个T-SNE的实现库：[bhtsne](https://github.com/lvdmaaten/bhtsne)。下载安装方法如下：

   ```sh
   # 首先找到自己的visdom安装的目录，不同的电脑可能不一样，也可以直接看后面的demo的报错知道安装在哪里。
   cd /usr/local/lib/python3.6/dist-packages/visdom/
   mkdir extra_deps
   cd extra_deps
   git clone https://github.com/lvdmaaten/bhtsne
   cd bhtsne
   g++ sptree.cpp tsne.cpp tsne_main.cpp -o bh_tsne -O2
   ```

4. 安装完毕，启动服务器，然后使用下面的脚本进行测试，记得吧 host 和 ip设置为你的server运行的ip地址。

   ```python
   import visdom
   import numpy as np
   env = visdom.Visdom('127.0.0.1', env='main')
   X = np.arange(0, 1, 0.1)
   Y = X * X
   env.line(
       X = X , Y = Y 
   )
   feats = np.random.rand(2000, 10)
   labels = [0] * 2000  # 不同的labels会使用不同的颜色
   env.embeddings(feats, labels)
   ```

   当然，如果你能下载大数据集，可以参考 visdom issue611 中官方的example，这个example还展示了如何展示图片。这里直接给出参考代码：

   ```python
   #!/usr/bin/env python3
   
   # Copyright 2017-present, The Visdom Authors
   # All rights reserved.
   #
   # This source code is licensed under the license found in the
   # LICENSE file in the root directory of this source tree.
   
   import visdom
   import numpy as np
   from PIL import Image  # type: ignore
   import base64 as b64  # type: ignore
   from io import BytesIO
   import sys
   
   try:
       features = np.loadtxt("example/data/mnist2500_X.txt")
       labels = np.loadtxt("example/data/mnist2500_labels.txt")
   except OSError:
       print("Unable to find files mmist2500_X.txt and mnist2500_labels.txt "
             "in the example/data/ directory. Please download from "
             "https://github.com/lvdmaaten/lvdmaaten.github.io/"
             "blob/master/tsne/code/tsne_python.zip")
       sys.exit()
   
   vis = visdom.Visdom()
   
   image_datas = []
   for feat in features:
       img_array = np.flipud(np.rot90(np.reshape(feat, (28, 28))))
       im = Image.fromarray(img_array * 255)
       im = im.convert('RGB')
       buf = BytesIO()
       im.save(buf, format='PNG')
       b64encoded = b64.b64encode(buf.getvalue()).decode('utf-8')
       image_datas.append(b64encoded)
   
   
   def get_mnist_for_index(id):
       image_data = image_datas[id]
       display_data = 'data:image/png;base64,' + image_data
       return "<img src='" + display_data + "' />"
   
   
   vis.embeddings(features, labels, data_getter=get_mnist_for_index, data_type='html')
   
   input('Waiting for callbacks, press enter to quit.')
   
   ```

5. 最后的展示图如下：

   <img src="/xkblog/public/img/截屏2021-03-09 下午3.29.03.png" alt="截屏2021-03-09 下午3.29.03" style="zoom:50%;" />

完美收工！！

坑点： bhtsne 的放置位置注意。

坑点：labels会使用不同的颜色，然后是随机的颜色，最多支持10个。所以注意！！颜色没有了，那么可能是labels太多了。最多支持10个labels。