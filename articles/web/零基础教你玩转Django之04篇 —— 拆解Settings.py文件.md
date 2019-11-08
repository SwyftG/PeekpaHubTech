**全网第一篇系列讲述Django线上项目实战的文章。**

上一篇我们主要完成了Gua的POST请求，完善了RESTful API，实现了查询分页。那么这一节，我们就要来说一下如何把配置文件分离开来，以应对不一样的工作环境。

### 为啥要拆解配置

众所周知，在实际的软件开发过程中，我们写程序，肯定是现在开发环境编写代码；当在开发环境编写完成我们会把工程切换到测试环境，开始测试工作；在完成测试所有任务之后，确认项目正常运转，最后我们就会切换到正式环境，也就是线上环境。所以，在这其中，就有三个环境需要我们分别配置：
- 开发环境；
- 测试环境；
- 线上环境

大家是否想过，在我们的Django工程里，只有一个`PeekpaHubTech/settings.py`文件是配置文件。如果我们每次都为了切换不同的环境，而修改我们的`setting.py`文件，会不会很麻烦？而且很容易发生错误。那么今天，皮爷就交给大家如何来拆分`setting.py`文件，来针对不同的开发环境来做不同的项目配置。

### 拆分settings.py文件

#### 第一步：

首先，在`PeekpaHubTech`文件夹下面，也就是和`settings.py`文件夹同级。我们先创建一个`settings`文件夹，同时，里面，里面要有一个叫`__init__.py`的空文件。

这个文件的作用就是让我们的`settings`文件夹底下的`py`文件，可以被其他地方的代码作为`impot`的对象引入。


#### 第二步：

接着，我们在`settings`文件夹底下，创建一个`base.py`文件和`develop.py`文件。当然，你有多少环境，就可以创建多少个`py`文件夹。比如`online.py`，`test.py`等等


#### 第三步：

我们把原先的`settings.py`文件里面的内容，全部移动到`base.py`文件中。

#### 第四步：

在你创建的不同环境的`py`文件的第一行，写入一下代码：

```Python
from .base import *   #NOQA
```

后面加了一个`#NOQA`只是为了不让PEP8来检查我们这个文件。

我这里是之创建了一个`develop.py`文件，所以，你可以把你在开发环境下面的配置信息，都填写到你对应的`py`文件夹下面，比如，我这里就把`base.py`文件夹里面的`DATABASE`移动到了`develop.py`文件夹下，当然，一般来说，我们不同环境之间的切换，数据库环境的切换算是一个大头。

下面就是我的`develop.py`文件：

```Python
from .base import *   #NOQA
from mongoengine import connect

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': None,
    },
}

connect(CONFIG_JSON.get("mongo_databses").get("aliyun").get("config").get("database_name"),
        host=CONFIG_JSON.get("mongo_databses").get("aliyun").get("config").get("host"),
        port=CONFIG_JSON.get("mongo_databses").get("aliyun").get("config").get("port"))
```

非常的简介。这样，你就可以保证你在切换不同的环境的时候，让系统启动时，读取不同的配置信息就可以了。

这个时候，项目的工程样子就长这样：

![](https://mmbiz.qpic.cn/mmbiz_png/1jWFxptiajlIKqMSlwcwQvsMHO1XOz2VibUicRtuQIAB54J9newYo9pMBJmRw9MCJWX0gvAr3T7VM6wOsCbuB8CuQ/0?wx_fmt=png)

#### 第五步，最重要的一步：

这个时候，因为你已经把之前的`settings.py`文件移动到了`settings`文件夹下面，所以`PeekpahubTech/settings.py`文件你就可以删掉了。

在配置好`PeekpahubTech/settings/base.py`文件和`PeekpahubTech/settings/develop.py`文件之后，我们需要在项目的两个地方做一下修改：

- `manage.py`
- `PeekpahubTech/wsgi.py`

这里，先说`manage.py`文件。我们需要把：

```Python
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PeekpaHubWebsite.settings')
```

改成：

```Python
profile = os.environ.get('PROJECT_PROFILE', 'develop')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PeekpaHubWebsite.settings.%s' % profile)
```

同样的，在`PeekpahubTech/wsgi.py`文件里，我们需要把：

```Python
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PeekpaHubWebsite.settings')
```

改成

```Python
profile = os.environ.get('PROJECT_PROFILE', 'develop')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PeekpaHubWebsite.settings.%s' % profile)
```

至此，所有操作就都算是修改完成了。

如果你在终端，通过命令行的命令`python manage.py runserver`

记住，这两个地方一定要改。这里的代码也很简单，就是把我们的项目换成了`develop`环境而已。

#### 最有提一下PyCharm运行
如果都修改好了，但是点击PyCharm右上角的绿色运行按钮发现报错，那么别慌，我们需要调整一下PyCharm运行的参数环境。

![](https://mmbiz.qpic.cn/mmbiz_png/1jWFxptiajlIKqMSlwcwQvsMHO1XOz2VibFZvhbUy9bia62RuJC8DzicrqqCu0hcxAicbUEeQf92R5UiaONAKaJwGonA/0?wx_fmt=png)

点击那个`Edit Configuration`，然后来到这个界面：

![](https://mmbiz.qpic.cn/mmbiz_png/1jWFxptiajlIKqMSlwcwQvsMHO1XOz2Vib8ibbHyoh684YDcvAiavPyuyHgXA4tGAZbSMAGSichhguAvdIPRy1ImcLA/0?wx_fmt=png)

看到`Environment variables`，然后我们点进去：

![](https://mmbiz.qpic.cn/mmbiz_png/1jWFxptiajlIKqMSlwcwQvsMHO1XOz2VibzqF0oQicIzJvSaTiakbRMOWBbD8SXHxqibSRHKBYicqUN1xD9PRafsKFAQ/0?wx_fmt=png)

在`value`里面，填写正确的setting地址就可以了。

好了，系列文章今天这一章节就先说到这里，正好马上就要**双11**了，又到了**一年一度买服务器的时候了**。照目前的趋势，皮爷今年肯定又会购买服务器了，服务器是真的不嫌多啊，一台服务器可以写网站，两台服务器就可以玩 RPC，三台可以搞集群。。。

下面这个链接大家可以在双十一的时候在阿里云享受优惠，注意，每年就此一次，错过了可就要等一年的哦：

> https://www.aliyun.com/1111/2019/group-buying-share?ptCode=59102A206508DC8B402167FFD766D480647C88CF896EF535&userCode=nrkmbo9q&share_source=copy_link

喜欢的同学，可以把皮爷的文章分享出来，让跟多的人一起来学习。这个系列教程的文章，皮爷都会讲源代码放到 GitHub 上，想要获取代码的同学，请关注微信公众号『**皮爷撸码**』，然后回复『**网站代码**』即可获得链接地址。这里有更多更好玩的东西，等你一起来学习提高。


