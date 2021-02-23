---
layout: post
title: Markdown在xkblog的一些用法
date: 2021-02-19 19:20:23 +0000
category: markdown
typora-root-url: ../../../code
---

> 这个就是我的博客啦，第一个发表，现在感觉很nice
>
> 以后所有的 install doc 之类的文章都会发表到这里哦

## 对XKBLOG添加latex数学支持

对原来主题的改进，添加了数学支持:

[latex数学支持文档](https://www.jianshu.com/p/aa359b3aef0c) ： 其实很简单，就是添加2个script文档，然后 为了将默认的( -> $，添加第三个script就行。在模版中的 \_include/post.html 中添加了如下代码：

```html

<script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
<script>
    MathJax = {
      tex: {
        inlineMath: [['$', '$']],
        processEscapes: true
      }
    };
</script>

```

##### 用法：

 ```markdown
$$ x_1 = 2 $$
 ```

##### 效果：

$$
x_1 = 2
$$

## 对XKBLOG图片格式微调

首先对于图片显示，我们的需求是本地和服务器保持一致，本地 typora 显示什么样，服务器显示啥样就很nice。所以我们首先是进行了主题的替换，whitey.css 文件已经在我们的主题上得到了迁移。这个步骤很nice。现在其实就差了图片的行为。图片行为比较复杂，没有那么简单，所以这里给出保持一致性的方法：

1. 在文章前面加入 `typora-root-url: ../../../code` YAML代码块：

   其中的YAML代码块表示typora的图片的根路径会被替换成为上面的。由于我们的图片保存在 /xkblog/public/img/下面，所以我们保证我们的本地 root-url 下面的 /xkblog 刚好就是我们的项目文件就好了。

   

2. 将图片拷贝到 /xkblog/public/img/下面

3. 在md中添加 `<div align='center'><img src="/xkblog/public/img/example.jpg" alt="example" /></div>` 得到下面效果：

   <div align='center'><img src="/xkblog/public/img/example.jpg" alt="example" /></div>

4. 在md中如果直接添加 `![]()` 的图片代码，那么很不幸，在网站上会是左对齐，但是在typora会是居中对齐。所以我们使用div + img 的方式吧。这个方式可以支持更多的格式，同时可以保持一致性。目前也没有时间去尝试别的方法了。



## 对XKBLOG添加 Mermaid 数据流图功能

##### 用法和效果

 ```
graph LR
	KaTex--> A((标记 Accents))
	A-->撇,估计,均值,向量等写于符号上下的标记
	KaTex--> 分隔符_Delimiters
	分隔符_Delimiters-->小中大括号,竖杠,绝对值等分隔符的反斜杠写法
	KaTex--> 公式组_Enviroments
	公式组_Enviroments-->B(.....)
	KaTex-->C(...)
 ```

然后将上面的语言标志为 mermaid。然后网页就会自动渲染了。

```mermaid
graph LR
	KaTex--> A(标记 Accents)
	A-->撇,估计,均值,向量等写于符号上下的标记
	KaTex--> 分隔符_Delimiters
	分隔符_Delimiters-->小中大括号,竖杠,绝对值等分隔符的反斜杠写法
	KaTex--> 公式组_Enviroments
	公式组_Enviroments-->B(.....)
	KaTex-->C(...)
```

##### mermaid 功能开发细节

首先需要知道mermaid其实本身就是一个js项目，用来在网站上添加使用文本文档描述的SVG流程图。所以在github上可以看到mermaid的官方网站。然后发现如果想要添加 mermaid 只需要引入 .js 文件并且加入初始化代码即可，然后mermaid.initialize(config)会直接将当前已经加载的 .mermaid 类型的元素的内容当作是graph describ 然后编译出 SVG 图片插入回去。所以最简单的一个实例代码就是: 

```html
<html>
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <script src="jquery-1.10.2.min.js"></script>
    <body>
        <p style="font-family: Songti SC; font-weight: lighter"> 我的 </p>
        <code class='language-mermaid'>
            graph TD;
            A-->B;
            A-->C;
            B-->D;
            C-->D;
        </code>
    </body>
    <script>
            mermaid.initialize({
                startOnLoad:false, 
            });
            mermaid.init({}, '.language-mermaid')
     </script>
</html>
```

上述代码中的 mermaid.init(config, selector) 函数负责将 .language-mermaid 的class 也当作是图像定义处理，然后插入 SVG。因为通过开发者工具，发现在Jekyll 上面，我们会生成code.language-mermaid 的元素块。。。 

总结一下mermaid是集成良好的 javascript 插件，对于所有的可以直接使用js的地方，mermaid都可以很好的集成，这点非常的nice。然后更多的mermaid config 可以去github上的官网查看。