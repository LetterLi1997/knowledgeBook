# -ubuntu科学上网-ss-qt5 + SwitchyOmega-
linux这么优秀的系统竟然软件生态圈支持这么不受重视。且不说一堆软件都是windows版本，近年来mac版也是火速跟上，就剩下linux被无视了。
这篇文章主要分享下如何用最简洁的步骤在ubuntu16.04科学上网。

## Step One：安装shadowsocks-qt5

    sudo add-apt-repository ppa:hzwhuang/ss-qt5
    sudo apt-get update
    sudo apt-get install shadowsocks-qt5

1. 安装完毕后，可以看到如下界面

[图1 ssr]..硬盘损坏ubuntu系统登不上去了..

2. 接下来就是很重要的编辑部分了！

我是买了“熊猫翻滚”的学术熊猫vpn，又快又稳，如果便宜点就更好了。根据它提供的服务器ip、端口、密码、加密方式这几个关键参数就可以编辑好啦。

[图2 ssr编辑界面]..硬盘损坏ubuntu系统登不上去了..

但是这时候要是你试一下ping www.google.com 可能会失望的哦。。这就涉及到用terminal传输，它不直接支持socks5协议。
要是想要用终端ping通google的话，需要terminal设置socks5代理
具体教程连接：  https://www.jianshu.com/p/ff4093ed893f

因为咱们主要是用浏览器查资料，我接下来继续介绍的是Step Two
## Step Two：chrome安装SwitchyOmega插件
[图  proxy]

### 接下来设置auto switch
[图 auto]
1. 条件设置：        raw.githubusercontent.com
2. 规则列表网址：    https://raw.githubusercontent.com/gfwlist/gfwlist/master/gfwlist.txt
3. 设置完毕后   立即更新情景模式  按钮

## Step Three:
点击chrome右上角的插件按钮，选择auto switch就可以啦！

## Step Final：
能够翻墙了= =  第一步当然是上youtube啦= =
