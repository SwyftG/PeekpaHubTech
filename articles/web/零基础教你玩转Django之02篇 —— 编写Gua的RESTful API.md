**全网第一篇系列讲述Django线上项目实战的文章。**

上一篇我们主要讲了一下环境的搭建，那么这一节，我们要说这么几个东西：
- 什么是RESTful API
- 在Django中如何使用MongoDB
- 编写Gua的API

### 啥是RESTful？

现在一提起来API，就都会提到一个叫 RESTful 的概念。那到底啥事 RESTful API 呢？

最通读是讲法，就是 `RESTful API 就是正确是使用 http 请求`。只要是用正确的姿势，正确的使用http，就是 RESTful API。

RESTful API 有以下几大特征：

1. 请使用正确的http request method来请求数据。GET/POST/PUT/DELETE/PATCH；
2. 面向资源编程，通过API提交的参数最好是名词，就像下面的gua：
```
http://www.peekpa.tech/gua
```
3. API应该体现版本，需要在URL中加入v1，v2这种版本号：
```
http://www.peekpa.tech/v1/gua
```
4. 需要体现API，所以最好加上api字样：
```
http://www.peekpa.tech/api/v1/gua
```
5. 使用 HTTPS：
```
https://www.peekpa.tech/api/v1/gua
```
6. 响应式设置代码状态；
7. API的参数，可以加入变量：
```
http://www.peekpa.tech/api/v1/gua?num=100100&style=1
```
8. 针对不同的method，对应的返回值要规范：
```
GET: 返回列表或者单条数据
POST: 新增的数据
PUT: 返回更新数据
PATCH: 局部更新，返回更新数据
DELETE: 返回空文档
```
9. 如果有错误信息，则需要在返回的数据里面，将错误码写在`code`里；
10. 返回的数据详细内容，放在`data`里面：
```
{
    "code":10001,
    "data": {
        "id": 1,
        "name": "peekpa"
    }
}
```

以上就是RESTful API的规范，实际操作起来，可能多多少少会有出入，请以具体的需求为准来设计API。

### Django和MongoDB的结合

一般情况，Django使用的都是 RDB(Relational Database)，比如MySQL，还有自带的sqllite。我们这里将要使用的是MongoDB，非关系型数据库。

为啥这里要使用MongoDB，是因为之前项目的数据都在MongoDB里面存储的，所以这里为了省事儿，就直接使用原来的数据库了。

在Django里面使用MongoDB，首先，我们需要安装库：
```
mongoengine==0.15.0
djangorestframework==3.10.3
Markdown==3.1.1
django-filter==2.2.0
```
可以直接通过命令来安装：
```
$ pip install djangorestframework markdown Django-filter mongoengine
```
安装好之后，我们需要在`settings.py`改一些设置。

首先将`DATABASES`改为，将原来系统模板生成的配置修改为None：
```
DATABASES = {
    'default': {
        'ENGINE': None,
    }
}
```
然后我们需要加入以下代码：
```
from mongoengine import connect

MONGODB_DATABASES = {
    "default": {
        "name": <DatabaseName>, #这里填写的是MongoDB的DatabaseName
        "host": <88.88.88.88>, # MongoDB的host IP地址
        "tz_aware": True, #设置时区
    },
}

connect(<DatabaseName>, host=<IP address>, port=<port Num>)
```
这里说的可能有点抽象，我们拿下面的一个具体例子来说一下：

![](https://mmbiz.qpic.cn/mmbiz_png/1jWFxptiajlLbWGp8EskTVxEpO4N8ymuaepfdYUuQKU1Elbb4O1MK9rWPszrNoLjKqLepHlsYHzgNlM5SlIWYrw/0?wx_fmt=png)

上图是我云服务器上的一个MongoDB内容截图，假设我的云服务器的公网IP地址是`11.12.13.15`，那么我们看到这张图里面，对应的`DatabseName`是`ZhouyiTest`，`CollectionName`是`gua64`，MongoDB的`端口号`是`27017`

那么我们按照上面的参数，就需要把之前的代码填写成一下这个样子：
```
from mongoengine import connect

MONGODB_DATABASES = {
    "default": {
        "name": "ZhouyiTest", 
        "host": "11.12.13.15", 
        "tz_aware": True, #设置时区
    },
}

connect("ZhouyiTest", host="11.12.13.15", port=27017)
```

接着，在`settings.py`文件里，我们要把`rest_framework`加到`INSTALLED_APPS`里面：
```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.Gua.apps.GuaConfig',
    'rest_framework' #新加的内容
]
```

然后，我们去`Gua/models.py`文件里面，去编写 Gua 的bean：
```Python
from mongoengine.fields import *
from mongoengine.document import Document

# Create your models here.

class Gua(Document):
    meta = {'collection': 'gua64'} #这里和之前提到的CollectionName一一对应
    gua_number = StringField()
    gua_sub_title = StringField()
    gua_title = StringField()
    gua_serial_text = StringField()
    gua_serial = StringField()
    gua_onw = StringField()
    gua_two = StringField()
    gua_three = StringField()
    gua_four = StringField()
    gua_five = StringField()
```
接着，我们在`Gua`目录下面，创建一个`serializer.py`文件，用来编写序列化，将里面的代码改写成这样：
```Python
from rest_framework import serializers
from .models import Gua


class GuaSerializer(serializers.Serializer):
    gua_number = serializers.CharField()
    gua_sub_title = serializers.CharField()
    gua_title = serializers.CharField()
    gua_serial_text = serializers.CharField()
    gua_serial = serializers.CharField()
    gua_onw = serializers.CharField()
    gua_two = serializers.CharField()
    gua_three = serializers.CharField()
    gua_four = serializers.CharField()
    gua_five = serializers.CharField()
    
    class Meta:
        model = Gua
        fields = "__all__"
```
接着，我们就要编写View了，修改`Gua/views.py`文件：
```Python
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from .models import Gua
from .serializer import GuaSerializer


# Create your views here.
class GuaView(APIView):
    renderer_classes = [JSONRenderer]
    
    def get(self, request, format=None):
        check_num = request.GET.get('checkNum')
        result = Gua.objects.filter(gua_serial=check_num).first()
        serializer = GuaSerializer(result)
        return Response(data=serializer.data)
```
最后一步，我们需要将URL注册到`urls.py`文件里，所以，`urls.py`文件修改为：
```Python
from apps.Gua.views import GuaView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('gua', GuaView.as_view()),
]
```
这个时候，启动Django项目，我们在浏览器里面，输入:
```
http://127.0.0.1:8000/gua?checkNum=111111
```
来看一下页面：

![](https://mmbiz.qpic.cn/mmbiz_png/1jWFxptiajlLbWGp8EskTVxEpO4N8ymuaovLK9f41E9hM19J1ICLhOH7oWLcO0vbSpYkrOh6DXab3RRQPvxyeAA/0?wx_fmt=png)

好的，说明我们的接口已经完成，通过URL可以顺利的从数据库里面捞数据了。

这里有个小细节，就是我们看到这个json结果里面，所有的key都是按照顺序排列的，如何能够修改顺序呢？当然，在Java里面，我们使用LinkedHashMap就可以实现，但是在Python里面，我们可以在`serializer.py`文件里面修改。

假设我们把`gua_two`修改到最后一个，也就是把代码编程下面这样：
```
class GuaSerializer(serializers.Serializer):
    gua_number = serializers.CharField()
    gua_sub_title = serializers.CharField()
    gua_title = serializers.CharField()
    gua_serial_text = serializers.CharField()
    gua_serial = serializers.CharField()
    gua_one = serializers.CharField()
    gua_three = serializers.CharField()
    gua_four = serializers.CharField()
    gua_five = serializers.CharField()
    gua_two = serializers.CharField() #移动到最后
    class Meta:
        model = Gua
        fields = "__all__"

```
那么这个时候再请求一下接口，就会发现，`gua_two`那个已经到了最下面了：

![](https://mmbiz.qpic.cn/mmbiz_png/1jWFxptiajlLbWGp8EskTVxEpO4N8ymuaPibxPHMfuTYQBSMvBPH4Zlq4S3AbjCwGLwPLXibIpUufXib9FAO5JPfrg/0?wx_fmt=png)

好了，系列文章今天这一章节就先说到这里，正好马上就要**双11**了，又到了**一年一度买服务器的时候了**。照目前的趋势，皮爷今年肯定又会购买服务器了，服务器是真的不嫌多啊，一台服务器可以写网站，两台服务器就可以玩 RPC，三台可以搞集群。。。

下面这个链接大家可以在双十一的时候在阿里云享受优惠，注意，每年就此一次，错过了可就要等一年的哦：

> https://www.aliyun.com/1111/2019/group-buying-share?ptCode=59102A206508DC8B402167FFD766D480647C88CF896EF535&userCode=nrkmbo9q&share_source=copy_link

喜欢的同学，可以把皮爷的文章分享出来，让跟多的人一起来学习。这个系列教程的文章，皮爷都会讲源代码放到 GitHub 上，想要获取代码的同学，请关注微信公众号『**皮爷撸码**』，然后回复『**网站代码**』即可获得链接地址。

![](https://mmbiz.qpic.cn/mmbiz_png/1jWFxptiajlLsEBtF0E1Bdub2EibbgsUrw8xJC6XZicWrx0ddHKa1WVQgj0CJEwaPWX2JIgtiaz6mzibvQJ5xhFKO0w/0?wx_fmt=png)