# java基础注意点
在讨论对象之前，我们简单回顾一下什么是“类与对象”。比如，狗是一个类，它被抽象成一个个特征：毛发、大小（成员变量）和方法：犬吠、舔舌头（成员方法）。其中泰迪可以被认为是狗这个大类中的特定对象，我们通过 
`Dog 泰迪 = new Dog();`
创建出了一个泰迪对象。

### 编译单元
编译单元一次是一个java。一个编译单元里面其实可以有很多类，但一个编译单元只能有一个类是public
### (default)修饰符——friendly
我们常常可以看到
```
public class Demo{
    private int var = 0;

    public Demo func(){
        // TO DO.
    }
}
```
但如果稍作更改
```
public class Demo{
    int var = 0;    //changed.

    public Demo func(){
        // TO DO.
    }
}
```
不对这个变量var做任何修饰，它便是一个 friendly的变量，即只对包内的类及其对象可见。

### 包
包其实就是用文件夹目录来管理的，一个目录底下的所有文件就是一个包，如果要用到其他包里面的类，就在最上面
```
package other;
```

### static是啥？
```
public class Demo{
    private static int var = 0;

    public Demo func(){
        // TO DO.
    }

    public static void main(String[] args){
        //..
    }
}
```
我们可以看到main方法的函数头中有static，其实这样的main方法被称为类方法；var变量被称为类变量，可以用如下方式直接访问
```
类名.类变量
    Demo.var
类名.类方法
    Demo.func();
```
当我们创建一个新对象时
```
    Demo demo1 = new Demo();
    demo1.var = 1;
    Demo demo2 = new Demo();
    demo2.var = 10;
    System.out.println(demo1.var+" and "+demo2.var);
    >> 10 and 10
```
上面代码的意思是说static修饰的类变量与类方法是只初始化一次的，某个对象修改这个值时便会引起所有对象调用该值都发生变化。

## 对象容器
想象我们要实现一个notebook的程序，能够在里面不断添加新的记录并且可以删除一些旧的记录。如果使用String数组一定要定义初始容量：
```
String[] notebook = new String[100];
```
这显然是无法实现一个真正可用的笔记本的。

我们需要引入一个概念叫做**对象容器**
```
ArrayList<String> notebook = new ArrayList<String>();
```
![]()