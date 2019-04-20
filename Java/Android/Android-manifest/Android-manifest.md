# AndroidManifest.xml 详解

**本文转载自简书 作者：闪电的蓝熊猫   https://www.jianshu.com/p/3b5b89d4e154**

我们在进行APP开发的时候都会遇到一个文件：AndroidManifest.xml。对于本人而言上手不久后只知道它是配置用的，但是这文件里的东西具体有什么用，该怎么用一直都没有理解。

研究AndroidManifest.xml最好的方式自然就是对照着官方文档详细理解项目中每个字段的作用，并且做出一些修改来验证。

## AndroidManifest是什么?
AndroidManifest官方解释是应用清单（manifest意思是货单），每个应用的根目录中都必须包含一个，并且文件名必须一模一样。这个文件中包含了APP的配置信息，系统需要**根据里面的内容运行APP**的代码，显示界面。
## AndroidManifest的作用是什么？
1. 为应用的 Java 软件包命名。软件包名称充当应用的唯一标识符。
2. 描述应用的各个组件，包括构成应用的 Activity、服务、广播接收器和内容提供程序。它还为实现每个组件的类命名并发布其功能，例如它们可以处理的 Intent 消息。这些声明向 Android 系统告知有关组件以及可以启动这些组件的条件的信息。
3. 确定托管应用组件的进程
4. 声明应用必须具备哪些权限才能访问 API 中受保护的部分并与其他应用交互。还声明其他应用与该应用组件交互所需具备的权限
5. 列出 Instrumentation类，这些类可在应用运行时提供分析和其他信息。这些声明只会在应用处于开发阶段时出现在清单中，在应用发布之前将移除。
6. 声明应用所需的最低 Android API 级别
7. 列出应用必须链接到的库

上面是官方的解释。很多东西笔者现在还不能理解，也没有用到，先挑笔者理解的进行解释。

- 第一条：提供软件包名。这就是我们的apk的名字，通常我们的名字都是类似"com.android.gles3jni"这种，和Java类名类似，目的是确定使其成为一个唯一值。

- 第二条：描述应用的各个组件。这是用来定义四大组件用的。我们最常用的就是Activity组件。它需要定义组件的表现形式（组件名、主题、启动类型），组件可以响应的操作（例如某个启动意图）等。

-  第五条：声明最低API级别。这个级别在build.gradle文件中也能定义，字段是minSdkVersion。在AndroidManifest.xml文件中定义的情况比较少。

- 第六条：列出必要的lib库。这东西在3.0以后的Android Studio似乎也没什么功能，因为在3.0以后编译用的是CMakeLists.txt文件，以及build.gradle文件来指定库。

## 一份真实的AndroidManifest.xml文件
```
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
          package="com.sample.teapot"
          android:versionCode="1"
          android:versionName="1.0.0.1" >

  <uses-feature android:glEsVersion="0x00020000"></uses-feature>

  <application
      android:allowBackup="false"
      android:fullBackupContent="false"
      android:supportsRtl="true"
      android:icon="@mipmap/ic_launcher"
      android:label="@string/app_name"
      android:theme="@style/AppTheme"
      android:name="com.sample.teapot.TeapotApplication"
      >

    <!-- Our activity is the built-in NativeActivity framework class.
         This will take care of integrating with our NDK code. -->
    <activity android:name="com.sample.teapot.TeapotNativeActivity"
              android:label="@string/app_name"
              android:configChanges="orientation|keyboardHidden">
      <!-- Tell NativeActivity the name of our .so -->
      <meta-data android:name="android.app.lib_name"
                 android:value="TeapotNativeActivity" />
      <intent-filter>
        <action android:name="android.intent.action.MAIN" />
        <category android:name="android.intent.category.LAUNCHER" />
      </intent-filter>
    </activity>
  </application>
</manifest>
```
这是Google官方示例中的teapots项目中的一个文件，我们就针对这份文件来分析字段的意义。字段的意义参考的是[官方文档](https://developer.android.com/guide/topics/manifest/manifest-element?hl=zh-cn)。
## `<manifest>`元素
首先，所有的xml都必须包含`<manifest>`元素。这是文件的根节点。它必须要包含`<application>`元素，并且指明xmlns:android和package属性。

### `<manifest>`元素中的属性
**xmlns:android**

这个属性定义了Android命名空间。必须设置成"http://schemas.android.com/apk/res/android"。不要手动修改。

**package**

这是一个完整的Java语言风格包名。包名由英文字母（大小写均可）、数字和下划线组成。每个独立的名字必须以字母开头。
构建APK的时候，构建系统使用这个属性来做两件事：

1. 生成R.java类时用这个名字作为命名空间（用于访问APP的资源）
比如：package被设置成com.sample.teapot，那么生成的R类就是：com.sample.teapot.R
2. 用来生成在manifest文件中定义的类的完整类名。比如package被设置成com.sample.teapot，并且activity元素被声明成`<activity android:name=".MainActivity">`，完整的类名就是com.sample.teapot.MainActivity。

包名也代表着唯一的application ID，用来发布应用。但是，要注意的一点是：在APK构建过程的最后一步，package名会被build.gradle文件中的applicationId属性取代。如果这两个属性值一样，那么万事大吉，如果不一样，那就要小心了。

**android:versionCode**

内部的版本号。用来表明哪个版本更新。这个数字不会显示给用户。显示给用户的是versionName。这个数字必须是整数。不能用16进制，也就是说不接受"0x1"这种参数。

**android:versionName**

显示给用户看的版本号。

[](https://upload-images.jianshu.io/upload_images/7822237-9a9177dd2a93a55a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1000/format/webp)

## `<manifest>`元素中的元素
### `<uses-feature>`元素
Google Play利用这个元素的值从不符合应用需要的设备上将应用过滤。

这东西的作用是将APP所依赖的硬件或者软件条件告诉别人。它说明了APP的哪些功能可以随设备的变化而变化。

使用的时候要注意，必须在单独的`<uses-feature>`元素中指定每个功能，如果要多个功能，需要多个`<uses-feture>`元素。比如要求设备同时具有蓝牙和相机功能：

```
<uses-feature android:name="android.hardware.bluetooth" />
<uses-feature android:name="android.hardware.camera" />
```
### `<uses-feature>`的属性

**android:name**

该属性以字符串形式指定了APP要用的硬件或软件功能。

**android:glEsVersion**

指明应用需要的Opengl ES版本。高16位表示主版本号，低16位表示次版本号。例如，如果是要3.2的版本，就是0x00030002。如果定义多个glEsVersion，应用会自动启用最高的设置。


### 与`<uses-feature>`类似的`<user-permission>`也可以写在mainfest节点下
```
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
package="com.photoeffect"
android:versionCode="1"
android:versionName="1.0" >

<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
<uses-permission android:name="android.permission.ACCESS_LOCATION_EXTRA_COMMANDS" />
<uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION" />
<uses-permission android:name="com.example.towntour.permission.MAPS_RECEIVE" />
<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
<uses-permission android:name="android.permission.CALL_PHONE" />
<uses-permission android:name="android.permission.READ_PHONE_STATE" />
<uses-permission android:name="com.google.android.providers.gsf.permission.READ_GSERVICES" />

<application
    ...
</application>

</manifest>
```


### `<application>`元素
此元素描述了应用的配置。这是一个必备的元素，它包含了很多子元素来描述应用的组件，它的属性影响到所有的子组件。许多属性（例如icon、label、permission、process、taskAffinity和allowTaskReparenting）都可以设置成默认值。

### `<application>`的属性
```
<application
    android:fullBackupContent="false"
    android:supportsRtl="true"
    android:icon="@mipmap/ic_launcher"
    android:label="@string/app_name"
    android:theme="@style/AppTheme"
    android:name="com.sample.teapot.TeapotApplication" >
    <activity
        android:name="com.photoeffect.MainActivity"
        android:label="@string/app_name" >
        <intent-filter>
            <action android:name="android.intent.action.MAIN" />

            <category android:name="android.intent.category.LAUNCHER" />
        </intent-filter>
    </activity>
    ...
</application>
```
**android:allowBackup**

表示是否允许APP加入到备份还原的结构中。如果设置成false，那么应用就不会备份还原。默认值为true。

**android:fullBackupContent**

这个属性指向了一个xml文件，该文件中包含了在进行自动备份时的完全备份规则。这些规则定义了哪些文件需要备份。此属性是一个可选属性。默认情况下，自动备份包含了大部分app文件。

**android:supportsRtl**

声明你的APP是否支持RTL（Right To Left）布局。如果设置成true，并且targetSdkVersion被设置成17或更高。很多RTL API会被集火，这样你的应用就可以显示RTL布局了。如果设置成false或者targetSdkVersion被设置成16或更低。哪些RTL API就不起作用了。

**android:icon**

APP的图标，以及每个组件的默认图标。可以在组价中自定义图标。这个属性必须设置成一个引用，指向一个可绘制的资源，这个资源必须包含图片。系统不设置默认图标。例如mipmap/ic_launcher引用的就是下面的资源：
[](https://upload-images.jianshu.io/upload_images/7822237-3b10b06e1b34709f.png?imageMogr2/auto-orient/)

### `<meta-data>`元素

指定额外的数据项，该数据项是一个name-value对，提供给其父组件。这些数据会组成一个Bundle对象，可以由PackageItemInfo.metaData字段使用。虽然可以使用多个`<meta-data>`元素标签，但是不推荐这么使用。如果有多个数据项要指定，推荐做法是：将多个数据项合并成一个资源，然后使用一个`<meta-data>`包含进去。
该元素有三个属性：

***android:name***

数据项名称，这是一个唯一值。

***android:resource***

一个资源的引用。

***android:value***

数据项的值。

### `<intent-filter>`元素
指明这个activity可以以什么样的意图(intent)启动。该元素有几个子元素可以包含。我们先介绍遇到的这两个：

### `<action>`元素
表示activity作为一个什么动作启动，android.intent.action.MAIN表示作为主activity启动。

### `<category>`元素
这是action元素的额外类别信息，android.intent.category.LAUNCHER表示这个activity为当前应用程序优先级最高的Activity。