全网第一篇系列讲述Django线上项目实战的文章。

从今天开始，皮爷要给大家来说一说如何玩转Python 的 Django 网络框架。使用 Django 来编写一套完全成熟的项目。首先，这个项目的有这么几个特点：
- 整体项目分为：爬虫，后端，前端三部分；
- 爬虫和后端，全部使用Python开发；
- 数据库使用MongoDB存储信息；
- 后端项目可以提供一套完整的RESTful API;
- 前后端完全分离;
- 项目部署到云服务器上，100%的正式环境项目。

大家可能就问，皮爷为啥要弄这个东西啊？这其中主要是由于皮爷想把之前的 PeekpaHub 网站重构了，将原来的 Spring Boot 转化为 Django 框架。同时，要做到前后端分离。

大家可以先去皮爷的网站看一下：
```
https://www.peekpa.tech/
```
这个只是目前的版本，这个系列文章皮爷会一边写，一边把代码放到 GitHub 上，大家可以看着文章，一起来参考学习【想要获取代码的童鞋，请看文末】。当写道一定程度的时候，我会把 Django 版本的网站部署到服务器上，正式替代掉当前的这个版本。

>所以，废话不多说，正好马上就要**双11**了，又到了**一年一度买服务器的时候了**。照目前的趋势，皮爷今年肯定又会购买服务器了，服务器是真的不嫌多啊，一台服务器可以写网站，两台服务器就可以玩 RPC，三台可以搞集群。。。
>
>下面这两个链接大家可以在双十一的时候享受优惠，注意，每年就此一次，错过了可就要等一年的哦：
>
>https://www.aliyun.com/1111/2019/group-buying-share?ptCode=59102A206508DC8B402167FFD766D480647C88CF896EF535&userCode=nrkmbo9q&share_source=copy_link

好了，接下来我们进入正题。

今天是这个系列的第一篇文章，所以，第一篇文章主要就是给大家来说一下整体项目的思路以及工程的搭建。

### PeekpaHub思路

目前，PeekpaHub的功能主要是有以下几点：
- 为《六十四卦》小程序做后端服务，提供数据；
- 为《标准日本语》学习提供查单词的接口；
- 每日定期启动爬虫；
- 每日定期检查爬虫运行情况，通过邮件汇报结果；
- 创建拥有不同权限的用户；
- 权限不同的用户，登录系统之后，显示的板块内容也不同；
- 将爬取的某论坛数据作为Json数据提供出去
- 。。。

所以，针对这次重构改动，我们暂定使用以下方案：
- 网络爬虫部分，还是独立出来，使用Python 的 Scrapy 爬虫框架开发，或者是其他的 Python 爬虫。具体选取哪一个，取决于爬取的网站。
- 前端网页版本展示，决定独立出来；
- 后端则是使用Django开发，使之成为一个完全的后端项目，为前端项目暴露接口，访问接口提供数据。

所以我们目前阶段，先来开发 Django 部分，做一套完整的 RESTful API出来。

### 项目搭建

整个项目，使用的环境如下：
- Pyton 3.6
- Django 2.2
- IDE使用的是 PyCharm

这些基本的软件和环境是怎么安装的，这里皮爷就不多说了，很基础，希望大家如果遇到问题，自己百度搜索一下就能找到答案。

那么我们这里就直接来用PyCharm创建Django工程吧。
创建工程的时候，我们在左侧选择 Django 项目：

![](https://mmbiz.qpic.cn/mmbiz_png/1jWFxptiajlKGhj3Ltpz5gN5hELFDvRZjvmhk7aE9PnDevcxKxK3w7raccsibezJzJzRLY6hcMJzVZJXa9s1JJ9w/0?wx_fmt=png)

然后，interpreter 选择你本地的 Python 3.6，最下面的 Applicatin Name，你在这里可以填写，也可以创建好之后，通过命令行的方式来创建，在以后的文章中，我们都会通过命令行方式创建，这里我们就先让系统使用模板帮我们创建好，我这里写了名字叫 Gua，因为我首先想要拿《六十四卦》小程序的接口来写。

![](https://mmbiz.qpic.cn/mmbiz_png/1jWFxptiajlKGhj3Ltpz5gN5hELFDvRZjwGKLgduQfD4qQSnJxLqyiadtUYdYTSWzowjGBXvlB6G19KeujCAlxCA/0?wx_fmt=png)

创建好之后，我们的目录结构长这个样子，但是，先别着急，我们需要再在这地下多做一些东西：

![](https://mmbiz.qpic.cn/mmbiz_png/1jWFxptiajlKGhj3Ltpz5gN5hELFDvRZjbbUjic5gH5icl9UHg934RVVhPosyKPsYmpzlrYlICqQhic2kkibnqZH4gA/0?wx_fmt=png)

- 创建文件夹`apps` ，将 `Gua` 目录移到这个文件目录下，这个地方就是以后管理 Django Application的地方；
- 创建`extra_apps`，存放第三方应用；
- 创建`media`，存放媒体文件；
- 创建`static`，存放静态文件；
- 这里看到我还创建了`config`文件，这里主要是存放一些配置文件，稍后的文章中我会说道这里的用法。

接着，我们就点击 IDE 右上角的运行图标：

![](https://mmbiz.qpic.cn/mmbiz_png/1jWFxptiajlKGhj3Ltpz5gN5hELFDvRZj2ZybGnEjDjqMiaWGfJZKafs58zup2GIQ7ibpmybtkwW3WH0cwGuKIjGA/0?wx_fmt=png)

然后在浏览器里面输入网址:
```
http://127.0.0.1:8000/
```

看到页面：

![](https://mmbiz.qpic.cn/mmbiz_png/1jWFxptiajlKGhj3Ltpz5gN5hELFDvRZjJEiaJMzuItNOkibXe3xSRGAhOk78L8ib7rOuZCyTV3IEzgYBWTDbGTNgQ/0?wx_fmt=png)

就说明你的程序已经搭建起来了。

好了，系列文章今天这一章节就先说到这里，下一节，我们来说一下如何在Django里面配置 MongoDB 数据库并且开发我们的 Gua API 接口。

喜欢的同学，可以把皮爷的文章分享出来，让跟多的人一起来学习。这个系列教程的文章，皮爷都会讲源代码放到 GitHub 上，想要获取代码的同学，请关注微信公众号『**皮爷撸码**』，然后回复『**网站代码**』即可获得链接地址。
![](https://mmbiz.qpic.cn/mmbiz_png/1jWFxptiajlLsEBtF0E1Bdub2EibbgsUrw8xJC6XZicWrx0ddHKa1WVQgj0CJEwaPWX2JIgtiaz6mzibvQJ5xhFKO0w/0?wx_fmt=png)