---
layout : post
title  : TOREAD+PaperPOOL
date   : 2022-08-16 16:00:00 +0000
category : todo
typora-copy-images-to: ../../../code/xkblog/public/img/
typora-root-url: ../../../code
---

#### 构建`2742195759:vim`

1. 首先编写dockerfile，期中的dockerfile可以用来参考，dockerfile的文件如下： 

   ```dockerfile
   FROM  ubuntu:latest
   LABEL description="this file can add xk_vim to any image"
   LABEL maintainer="xiongkun: xk18@mails.tsinghua.edu.cn"
   #EXPOSE 8080
   #EXPOSE 23456
   ENV TERM=xterm-256color
   WORKDIR /root
   COPY    ./to_copy  /root
   RUN     ["/bin/bash", "-i", "-c", \
           "mkdir -p /tmp && chmod 777 /tmp && apt update && apt install --no-install-recommends -y vim python-dev libtinfo5 exuberant-ctags cmake make gcc g++ xz-utils git\
           && cd /root/Important/MyVim/_MY_VIM_/ && sh ./vim_setup.sh \
           && rm -rf ~/.cache  \
           && rm -rf /var/lib/apt/lists/* "]
   ```

   可以看到，dockerfile其实很容易编写。注意，docker不适合频繁更新的场景。所以只有在需要环境依赖的时候在更新docker，其他时候将需要频繁更新的代码、文件放到文件服务器、或者是github上，然后通过一个安装.sh的文件进行安装。例如将xkvim脚本作为所有的vim文件存放处，然后使用install.sh的文件配置安装，这样可以实现最少操作实现更新。

2. 使用如下命令进行build

   ```
   docker build -t xiongkun:vim ./
   ```

3. 登录自己的 dockerhub账号： 2742195759。然后进行push即可上传到自己的服务器。实现重用！！

   ```sh
   docker login -u 2742195759 #登录，输入密码登录成功
   docker push 2742195759/vim #push传入镜像。即可以。
   ```

4. 最后说明一下vim的更新方法

   ```sh
   git pull 
   ./install.sh 
   ```

   即可以实现最新版本的安装。记得进入vim之后需要 BundleInstall。如果安装了新的plugin。其实最复杂的就是vim版本限制和YCM需要一些依赖，所以docker其实不太需要更新。

