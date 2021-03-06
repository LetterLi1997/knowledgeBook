# FT/FS 傅里叶之掐死教程的理解
[原文详见Heinrich知乎教程](https://zhuanlan.zhihu.com/p/19763358)

## 一、写在前面
1. 我们习惯了从时域的角度看世界
2. 频域也是一种看待世界、问题的角度
3. 从时域角度看起来纷繁复杂变幻莫测的世界，在频域角度看来其实是完全静止的

## 二、什么是频域
> 从我们出生，我们看到的世界都以时间贯穿，股票的走势、人的身高、汽车的轨迹都会随着时间发生改变。这种以时间作为参照来观察动态世界的方法我们称其为时域分析。而我们也想当然的认为，世间万物都在随着时间不停的改变，并且永远不会静止下来。但如果我告诉你，用另一种方法来观察世界的话，你会发现世界是永恒不变的，你会不会觉得我疯了？我没有疯，这个静止的世界就叫做频域。

首先我们看一段音乐：

![](https://github.com/LetterLi1997/knowledgeBook/blob/master/images/%E9%9F%B3%E4%B9%90%E6%97%B6%E5%9F%9F.jpg?raw=true)


就像是用手机录音机录下自己的声音一样，屏幕上就会有这样的一段声音波形。

但是我们上音乐课时候看的谱子老师叫我们哼曲子都不是按波形来教学的呀？！所以我们一起来看看以前看到的乐谱到底是用什么描述的？？

![](https://github.com/LetterLi1997/knowledgeBook/blob/master/images/%E9%9F%B3%E4%B9%90%E9%A2%91%E5%9F%9F.gif?raw=true)

对！我们以前教的方法都是 

|1：do | 2：re | 3：mi |
|:------|:------|:------|
|4：fa | 5：so | 6： ci|

每一个音符对应的相当于什么呢？

就相当于我们的 
- ![](https://github.com/LetterLi1997/knowledgeBook/blob/master/images/CodeCogsEqn%20(1).gif?raw=true)
- ![](https://github.com/LetterLi1997/knowledgeBook/blob/master/images/CodeCogsEqn%20(2).gif?raw=true)
- ![](https://github.com/LetterLi1997/knowledgeBook/blob/master/images/CodeCogsEqn%20(3).gif?raw=true)
- ……

所以当我们弹奏钢琴，每个音符发出时都是一个个独立且不断衰减的正弦波，这些正弦波之间由于各自的相位差在时域上叠加，形成我们看起来如此复杂的音乐/声音波形

在时域上，如同股票般起伏变幻莫测的乐章；在频域上，只有那几个永恒的音符（频率）

几个简单的频率和任意组合的相位差就可以产生现实世界中缤纷多彩的各种音乐、图像、自然景象……

**你看似落叶纷飞变化无常的世界，实际只是躺在上帝怀中一份早已铺好的乐章**

时隔两年因为看文章时难以理解一张平平无奇的频谱图，竟然可以通过IFFT还原它在时域中呈现的信号s(t)，不得不承认当时学习信号分析与处理时没有弄懂傅里叶变换的真正物理意义：

![](https://github.com/LetterLi1997/knowledgeBook/blob/master/images/%E9%A2%91%E8%B0%B1%E5%9B%BE.PNG?raw=true)
    
**1. 频域只是看待世界的另一个角度，从这个角度看问题有时候会比是与看简单得多！
就像前面提到的乐章，其实用频域中的特定几个频率和各自的相位就可以将时域的信号完全恢复出来。**

**2. 只有频谱没有相位谱，这个世界就是一个矩形波！**

![](https://github.com/LetterLi1997/knowledgeBook/blob/master/images/%E6%96%B9%E6%B3%A2.jpg?raw=true)

**3. 有频谱和相位谱，我就可以恢复出原信号！**

![](https://github.com/LetterLi1997/knowledgeBook/blob/master/images/CodeCogsEqn.gif?raw=true) 
由相位谱得到T的值