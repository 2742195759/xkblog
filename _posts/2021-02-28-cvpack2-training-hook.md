---
layout : post
title  : cvpack2-training-hook原理
date   : 2021-02-28 16:00:00 +0000
category : cvpack2
typora-copy-images-to: ../../../code/xkblog/public/img/
typora-root-url: ../../../code
---

## Hook 相关文件位置

1. cvpack2/engine/defaults.py 里面包含了 build_hooks 和 build_writers函数。这两个函数都是和hook有关的。
2. cvpack2/engine/hooks.py 里面包含了所有的 HookBase 类的子类。这些类包含了多个方面。如果想要创建新的也可以在这里创建
3. cvpack2/engine/utils/dump 里面包含了一些文件输出和屏幕输出的类。其中包括 EventStorage 作为一个上下文管理器，来管理所有的数据，例如put_scalar / put_image 之类的。然后history_buffer.py 负责管理单个变量的历史和滑动窗口。event.py: EventWriter 负责写出需要保存的变量。

## Hook 初始化流程

TODO

## 添加一个新的周期Hook

#### 需求：

需要添加一个新的周期训练hook，负责将需要保存的loss / metric 标量指标输出到visdom中形成一个训练曲线。

#### 实现：

我们使用 PeriodicWriter 作为Hook，所以我们不需要重写hook，只需要给这个hook一个writer，并且将这个writer放到 default.py: build_writer函数的返回列表中，就可以实现了。因此我们只需要仿照 TensorBoardXWriter这个函数实现我们的EventWriter就可以了。具体代码见下： 

```python
# __file__ : util/events.py
class VisdomWriter(EventWriter):
    """
    Write all scalars to a visdom env: scalar, and draw curves
    """

    def __init__(self, host:str, port:int, window_size: int = 20, interested_keys=[], **kwargs):
        """
        Args:
            host,port: the host and port of visdom server
            window_size (int): the scalars will be median-smoothed by this window size
            kwargs: other arguments passed to `torch.utils.tensorboard.SummaryWriter(...)`
        """
        self._window_size = window_size
        self._interested_keys = interested_keys
        from visdom import Visdom

        self._env_scalar = Visdom(host, port, env='cvpack2-scalar')
        #self._env_image  = Visdom(host, port, env='cvpack2-image')
        self._key2panel  = {}
        for key in interested_keys:
            self._key2panel[key] = self._env_scalar.line(
                X=np.array([0]),
                Y=np.array([0]),
                opts=dict(title='' + key))

    def write(self):
        storage = get_event_storage()
        for k, v in storage.latest_with_smoothing_hint(self._window_size).items():
            if k in self._interested_keys:
                self._env_scalar.line(
                    X=np.array([storage.iter]),
                    Y=np.array([v]),
                    win=self._key2panel[k],#win参数确认使用哪一个pane
                    update='append') #我们做的动作是追加，除了追加意外还有其他方式，这里我们不做介绍了

        if len(storage.vis_data) >= 1:
            #for img_name, img, step_num in storage.vis_data:
            #    self._writer.add_image(img_name, img, step_num)
            #storage.clear_images()
            ...

    def close(self):
        ...


```



