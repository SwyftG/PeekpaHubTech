  复制 一键排版  代码行数  代码紧凑  代码主题：
**全网第一篇系列讲述Django线上项目实战的文章。**

上一篇我们主要完成了Gua的API很简单的GET操作，那么这一节，我们要说这么几个东西：
- 使用RESTful API的规范来完善Gua的API
- 完善Gua的GET返回数据格式
- 实现Gua的POST请求
- 实现查询分页功能

### config.json

如果你关注了『皮爷撸码』公众号，并且从公众号里面得知了代码的下载地址，下载代码之后，会看到一个`config/config.json` 文件，别慌，这个是皮爷故意这么写的。目的就是：
- 隐藏配置，因为我的项目代码完全开源放到了GitHub上，如果我把数据库，接口信息什么的都原封不动的上传上去，会对我个人造成损失；
- 方便修改，如果以后需要修改比如端口号什么的，就只需要在一个地方修改就可以，然后重启服务，重新读取配置文件就可以，也可以写程序出发读取配置信息的操作。

不过，为了让大家读懂代码，我会在`config/config.json` 文件里面对应的key添加一些解释说明的。

### RESTful规范设计

我们在上一篇文章讨论了RESTful API的设计规范，但是在前一篇文章，我们的接口只是很简单的：

```
http://127.0.0.1:8000/gua?checkNum=111111
```

这个不符合我们的规范啊，我们的规范，至少应该是长这个样子的：

```
http://127.0.0.1:8000/v1/api/gua?checkNum=111111
```

那么，我们今天就来实现这样的接口。

首先，还是需要来修改我们的`urls.py` 文件，将之前的:

```Python
from apps.Gua.views import GuaView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('gua', GuaView.as_view()),
]
```

改成

```Python
from django.urls import path,include
import apps.Gua

urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/api/gua', include('apps.Gua.urls')),
]
```

这里看到，有一个`include()` 的东西，显然，这里的代码的意思就是，我们需要在`apps/Gua/` 目录下面，也创建一个`urls.py`文件，我们创建好，需要在这里面添加以下代码：

```Python
from django.urls import path
from .views import GuaView

urlpatterns = [
        path('', GuaView.as_view())
    ]
```

你看，这里我们是不是把上一节课的URL给拆成了两个部分来解析？放到两个文件里面做处理。

但是，这里写的这个：

```Python
path('', GuaView.as_view())
```

实际对应的URL是：

```
http://127.0.0.1:8000/v1/api/gua
```

我们其实还是需要后面的`checkNum`的，但是，为了符合RESTful API的规范：如果要访问单个资源，请将资源ID也放入到URL中，那么，这个正确的URL就应该是：

```
http://127.0.0.1:8000/v1/api/gua/111111
```

想要实现这样，不难啊，只需要将之前的那个`path`改成：

```Python
path('/<str:check_num>', GuaView.as_view())
```

同时，我们的`GuaView`里面的`get()`方法，也得做一些修改，将`check_num`作为参数传进去：

```Python
def get(self, request, check_num):
    #下面的逻辑代码省略，只需要注意第三个参数check_num就可以
```

好了，这个部分就匹配成功了。其实合起来，我们是通过：

```Python
path('v1/api/gua/<str:check_num>', GuaView.as_view())
```

来匹配URL:

```
http://127.0.0.1:8000/v1/api/gua/111111
```

只不过为了灵活性和扩展性，我们拆开来了。

接着，肯定会有小伙伴问`<str:check_num>` 这是个啥？

其实，这个是Django的路由机制。格式就是：

```
<类型：变量名>
```

| 转换格式类型 | 说明 |
| :--- | :--- |
| str | 匹配除分隔符（/）外的非空字符，默认类型<year>等价于<str:year> |
| int | 匹配0和正整数 |
| slug | 匹配字母、数字、横杠、下划线组成的字符串，str的子集 |
| uuid | 匹配格式化的UUID，如075194d3-6885-417e-a8a8-6c931e272f00 |
| path | 匹配任何非空字符串，包括路径分隔符，是全集 |

同样，URL的匹配还支持**正则表达式**。

以后如果想要扩展自己的API的话，别忘了使用RESTful 规范。

### 完善数据返回

上一篇我们的数据返回，是在数据库里面拿到数据，经过了一层序列化，把数据转换成Json格式，然后直接返回的，其实，在RESTful规范里面，这样做有些不妥，所有的数据，都应该放到`data`里面，这里我们就来简单实现一下这个。

来到`Gua/views.py`文件里面，把我们的`GuaView`的`get()`方法做一些调整就好。皮爷这里仅仅只是做了简单的修改，其实应该考虑到各种情况，各种错误的处理，不同错误还应该有不同的错误代码等等。我们目前就先简单来做一下：

```Python
    def get(self, request, check_num):
        response = {'code': 200}
        result = Gua.objects.filter(gua_serial=check_num).first()
        if result is None:
            response['code'] = '100090'
            response['msg'] = 'search_failed'
            return Response(data=response, status=200)
        response['msg'] = 'success'
        serializer = GuaSerializer(result)
        response['data'] = serializer.data
        return Response(data=response, status=200)
```

可以看到，在最后的`Response()`里面的`data`， 我们传入了一个`dict()` 类型的数据，这个数据是我们自己封装好的。最后的返回结果如下图：

![](https://mmbiz.qpic.cn/mmbiz_png/1jWFxptiajlKqq1IJRsNd1Ml8F4LzTWVf0wU31y3LqLNsPTuZhILbQJUjwWMqCZflBO4Weok7o3T81gZ4bGXxPQ/0?wx_fmt=png)

可以看到，搜搜结果数据是在`data`里面放着。

### 实现POST方法

其实，对于一个后端程序来说，POST的方法和GET方法都是很常见的，我们之前，在`GuaView`里面编写的`get()`方法，其实就是对应的GET method。对于一些操作，我们需要将数据存储到服务器上，这个时候，我们就要使用POST方法了。那么，实现POST方法其实也很简单，只需要编写对应的`post()`方法就可以了。

常规来说，POST的请求，如果请求成功，服务器需要将存储的数据返回到前端，以表示请求成功。这里，我就来列举代码中的一个`post()`方法，来给大家说一下写post有哪些注意的地方：

```Python
# 这里的model之类的就都先省略了，直接来说方法
    def post(self, request):
        app_version = request.data.get('appVersion')
        checkNum = request.data.get('checkNum')
        gender = request.data.get('gender', "")
        fromPage = request.data.get('fromPage')
        gua_r = GuaRModel()
        gua_r.appVersion = app_version
        gua_r.checkNum = checkNum
        gua_r.gender = gender
        gua_r.fromPage = fromPage
        year = str(datetime.datetime.now().year)
        month = str(datetime.datetime.now().month).zfill(2)
        day = str(datetime.datetime.now().day).zfill(2)
        gua_r.dayTime = "{}{}{}".format(year, month, day)
        gua_r.guaName = Gua.objects.filter(gua_serial=checkNum).first().gua_title
        result = gua_r.save()
        response = {}
        if result is None:
            response['code'] = '100093'
            response['msg'] = 'Report failed'
            return Response(datetime=response)
        response['code'] = '200'
        response['msg'] = 'success'
        serializer = GuaReportSerializer(gua_r)
        response['data'] = serializer.data
        return Response(data=response)
```

可以看到，这个方法首先是来处理POST请求传过来的那些参数的值。然后，创建一个我们需要存储的类，再将这些数值赋给它，最后调用一个`model.save()`方法就好，最后在把刚才的数据序列化，返回到前端就好。是不是很简单啊？当然，这里只是最简单的POST操作，POST还有很多复杂的操作，以后慢慢给大家道来。

### Restframework的分页实现

Restframework的分页有好几种实现方式：
- 可以在`settings.py`中直接设置；
- 可以用`PageNumberPagination`实现分页；
- 可以用`LimitOffsetPagination`实现分页；
- 可以用`CursorPagination`实现分页。

这里，皮爷使用的是自定义`PageNumberPagination`来实现的分页。

首先，我们先来收一下如何在`settings.py`里面，只需要直接加入以下配置就可以：

```Python
#  rest framework系统自带的分页
REST_FRAMEWORK = {
    # 分页
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',  # LimitOffsetPagination 分页风格
    'PAGE_SIZE': 30,  # 每页多少条记录
}
```

接下来，我们说一下如何自定义`PageNumberPagination`来实现的分页。

我们在`Gua/views.py`里面，首先写一个class，继承`PageNumberPagination`：

```Python
from rest_framework.pagination import PageNumberPagination

class GuaRPagination(PageNumberPagination):
    page_size = 30  # 表示每页的默认显示数量
    page_size_query_param = 'page_size'  # 表示url中每页数量参数
    page_query_param = 'page'  # 表示url中的页码参数
    max_page_size = 100  # 表示每页最大显示数量，做限制使用，避免突然大量的查询数据，数据库崩溃
```

然后，我们只需要在需要分页的地方，这么写就可以：

```Python
    def get(self, request,*args,**kwargs):
        response = {'code': 200}
        result = GuaRModel.objects.all()
        response['msg'] = 'success'
        response['size'] = len(result)
        # 以下几行代码是关键
        pg = GuaRPagination()
        page_role = pg.paginate_queryset(queryset=result, request=request, view=self)
        serializer = GuaReportSerializer(page_role, many=True)
        response['data'] = serializer.data
        return Response(data=response, status=200)
```

因为我们在`GuaRPagination`里面定义了请求URL里面可以携带分页的参数：`page`和`page_size`，分别表示`请求第几页内容`和`当前页面最大显示条数`。所以，我们的请求URL就可以变成这个样子：

```
# 表示请求第三页，每页最大显示10条数据
http://127.0.0.1:8000/v1/api/gua/list?page=3&page_size=10
```

比如测试，我们如果请求以下接口：

```
http://127.0.0.1:8000/v1/api/gua/list?page=3&page_size=6
```

那么应该表示的是第三页，并且显示的是六条数据：

![](https://mmbiz.qpic.cn/mmbiz_png/1jWFxptiajlKqq1IJRsNd1Ml8F4LzTWVfvuqA2rUha1BQ3vkiaympAfPp9Px3Cuf9LNbfYeibc3YIE6Zw5qPibfiaLQ/0?wx_fmt=png)

看到，是不是这样？哈哈哈哈啊。


### To Be Continue

好了，今天说的内容很多，接口还有很多内容，比如权限管理啊等等，这些我日后都会说道。皮爷只有一个宗旨：**就是要让你通过我的这个系列的文章，能够开发出来一套完整的系统。**

这些所有代码，我都会上传到GitHub上，获取方式就是请关注微信公众号『**皮爷撸码**』，然后回复『**网站代码**』即可获得链接地址。

好了，系列文章今天这一章节就先说到这里，正好马上就要**双11**了，又到了**一年一度买服务器的时候了**。照目前的趋势，皮爷今年肯定又会购买服务器了，服务器是真的不嫌多啊，一台服务器可以写网站，两台服务器就可以玩 RPC，三台可以搞集群。。。

下面这个链接大家可以在双十一的时候在阿里云享受优惠，注意，每年就此一次，错过了可就要等一年的哦：

> https://www.aliyun.com/1111/2019/group-buying-share?ptCode=59102A206508DC8B402167FFD766D480647C88CF896EF535&userCode=nrkmbo9q&share_source=copy_link

喜欢的同学，可以把皮爷的文章分享出来，让跟多的人一起来学习。这个系列教程的文章，皮爷都会讲源代码放到 GitHub 上，想要获取代码的同学，请关注微信公众号『**皮爷撸码**』，然后回复『**网站代码**』即可获得链接地址。这里有更多更好玩的东西，等你一起来学习提高。








全网第一篇系列讲述Django线上项目实战的文章。

上一篇我们主要完成了Gua的API很简单的GET操作，那么这一节，我们要说这么几个东西：

使用RESTful API的规范来完善Gua的API
完善Gua的GET返回数据格式
实现Gua的POST请求
实现查询分页功能
config.json
如果你关注了『皮爷撸码』公众号，并且从公众号里面得知了代码的下载地址，下载代码之后，会看到一个config/config.json 文件，别慌，这个是皮爷故意这么写的。目的就是：

隐藏配置，因为我的项目代码完全开源放到了GitHub上，如果我把数据库，接口信息什么的都原封不动的上传上去，会对我个人造成损失；
方便修改，如果以后需要修改比如端口号什么的，就只需要在一个地方修改就可以，然后重启服务，重新读取配置文件就可以，也可以写程序出发读取配置信息的操作。
不过，为了让大家读懂代码，我会在config/config.json 文件里面对应的key添加一些解释说明的。

RESTful规范设计
我们在上一篇文章讨论了RESTful API的设计规范，但是在前一篇文章，我们的接口只是很简单的：

http://127.0.0.1:8000/gua?checkNum=111111
这个不符合我们的规范啊，我们的规范，至少应该是长这个样子的：

http://127.0.0.1:8000/v1/api/gua?checkNum=111111
那么，我们今天就来实现这样的接口。

首先，还是需要来修改我们的urls.py 文件，将之前的:

from apps.Gua.views import GuaView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('gua', GuaView.as_view()),
]
改成

from django.urls import path,include
import apps.Gua

urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/api/gua', include('apps.Gua.urls')),
]
这里看到，有一个include() 的东西，显然，这里的代码的意思就是，我们需要在apps/Gua/ 目录下面，也创建一个urls.py文件，我们创建好，需要在这里面添加以下代码：

from django.urls import path
from .views import GuaView

urlpatterns = [
        path('', GuaView.as_view())
    ]
你看，这里我们是不是把上一节课的URL给拆成了两个部分来解析？放到两个文件里面做处理。

但是，这里写的这个：

path('', GuaView.as_view())
实际对应的URL是：

http://127.0.0.1:8000/v1/api/gua
我们其实还是需要后面的checkNum的，但是，为了符合RESTful API的规范：如果要访问单个资源，请将资源ID也放入到URL中，那么，这个正确的URL就应该是：

http://127.0.0.1:8000/v1/api/gua/111111
想要实现这样，不难啊，只需要将之前的那个path改成：

path('/<str:check_num>', GuaView.as_view())
同时，我们的GuaView里面的get()方法，也得做一些修改，将check_num作为参数传进去：

def get(self, request, check_num):
    #下面的逻辑代码省略，只需要注意第三个参数check_num就可以
好了，这个部分就匹配成功了。其实合起来，我们是通过：

path('v1/api/gua/<str:check_num>', GuaView.as_view())
来匹配URL:

http://127.0.0.1:8000/v1/api/gua/111111
只不过为了灵活性和扩展性，我们拆开来了。

接着，肯定会有小伙伴问<str:check_num> 这是个啥？

其实，这个是Django的路由机制。格式就是：

<类型：变量名>
转换格式类型	说明
str	匹配除分隔符（/）外的非空字符，默认类型等价于
int	匹配0和正整数
slug	匹配字母、数字、横杠、下划线组成的字符串，str的子集
uuid	匹配格式化的UUID，如075194d3-6885-417e-a8a8-6c931e272f00
path	匹配任何非空字符串，包括路径分隔符，是全集
同样，URL的匹配还支持正则表达式。

以后如果想要扩展自己的API的话，别忘了使用RESTful 规范。

完善数据返回
上一篇我们的数据返回，是在数据库里面拿到数据，经过了一层序列化，把数据转换成Json格式，然后直接返回的，其实，在RESTful规范里面，这样做有些不妥，所有的数据，都应该放到data里面，这里我们就来简单实现一下这个。

来到Gua/views.py文件里面，把我们的GuaView的get()方法做一些调整就好。皮爷这里仅仅只是做了简单的修改，其实应该考虑到各种情况，各种错误的处理，不同错误还应该有不同的错误代码等等。我们目前就先简单来做一下：

    def get(self, request, check_num):
        response = {'code': 200}
        result = Gua.objects.filter(gua_serial=check_num).first()
        if result is None:
            response['code'] = '100090'
            response['msg'] = 'search_failed'
            return Response(data=response, status=200)
        response['msg'] = 'success'
        serializer = GuaSerializer(result)
        response['data'] = serializer.data
        return Response(data=response, status=200)
可以看到，在最后的Response()里面的data， 我们传入了一个dict() 类型的数据，这个数据是我们自己封装好的。最后的返回结果如下图：


可以看到，搜搜结果数据是在data里面放着。

实现POST方法
其实，对于一个后端程序来说，POST的方法和GET方法都是很常见的，我们之前，在GuaView里面编写的get()方法，其实就是对应的GET method。对于一些操作，我们需要将数据存储到服务器上，这个时候，我们就要使用POST方法了。那么，实现POST方法其实也很简单，只需要编写对应的post()方法就可以了。

常规来说，POST的请求，如果请求成功，服务器需要将存储的数据返回到前端，以表示请求成功。这里，我就来列举代码中的一个post()方法，来给大家说一下写post有哪些注意的地方：

# 这里的model之类的就都先省略了，直接来说方法
    def post(self, request):
        app_version = request.data.get('appVersion')
        checkNum = request.data.get('checkNum')
        gender = request.data.get('gender', "")
        fromPage = request.data.get('fromPage')
        gua_r = GuaRModel()
        gua_r.appVersion = app_version
        gua_r.checkNum = checkNum
        gua_r.gender = gender
        gua_r.fromPage = fromPage
        year = str(datetime.datetime.now().year)
        month = str(datetime.datetime.now().month).zfill(2)
        day = str(datetime.datetime.now().day).zfill(2)
        gua_r.dayTime = "{}{}{}".format(year, month, day)
        gua_r.guaName = Gua.objects.filter(gua_serial=checkNum).first().gua_title
        result = gua_r.save()
        response = {}
        if result is None:
            response['code'] = '100093'
            response['msg'] = 'Report failed'
            return Response(datetime=response)
        response['code'] = '200'
        response['msg'] = 'success'
        serializer = GuaReportSerializer(gua_r)
        response['data'] = serializer.data
        return Response(data=response)
可以看到，这个方法首先是来处理POST请求传过来的那些参数的值。然后，创建一个我们需要存储的类，再将这些数值赋给它，最后调用一个model.save()方法就好，最后在把刚才的数据序列化，返回到前端就好。是不是很简单啊？当然，这里只是最简单的POST操作，POST还有很多复杂的操作，以后慢慢给大家道来。

Restframework的分页实现
Restframework的分页有好几种实现方式：

可以在settings.py中直接设置；
可以用PageNumberPagination实现分页；
可以用LimitOffsetPagination实现分页；
可以用CursorPagination实现分页。
这里，皮爷使用的是自定义PageNumberPagination来实现的分页。

首先，我们先来收一下如何在settings.py里面，只需要直接加入以下配置就可以：

#  rest framework系统自带的分页
REST_FRAMEWORK = {
    # 分页
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',  # LimitOffsetPagination 分页风格
    'PAGE_SIZE': 30,  # 每页多少条记录
}
接下来，我们说一下如何自定义PageNumberPagination来实现的分页。

我们在Gua/views.py里面，首先写一个class，继承PageNumberPagination：

from rest_framework.pagination import PageNumberPagination

class GuaRPagination(PageNumberPagination):
    page_size = 30  # 表示每页的默认显示数量
    page_size_query_param = 'page_size'  # 表示url中每页数量参数
    page_query_param = 'page'  # 表示url中的页码参数
    max_page_size = 100  # 表示每页最大显示数量，做限制使用，避免突然大量的查询数据，数据库崩溃
然后，我们只需要在需要分页的地方，这么写就可以：

    def get(self, request,*args,**kwargs):
        response = {'code': 200}
        result = GuaRModel.objects.all()
        response['msg'] = 'success'
        response['size'] = len(result)
        # 以下几行代码是关键
        pg = GuaRPagination()
        page_role = pg.paginate_queryset(queryset=result, request=request, view=self)
        serializer = GuaReportSerializer(page_role, many=True)
        response['data'] = serializer.data
        return Response(data=response, status=200)
因为我们在GuaRPagination里面定义了请求URL里面可以携带分页的参数：page和page_size，分别表示请求第几页内容和当前页面最大显示条数。所以，我们的请求URL就可以变成这个样子：

# 表示请求第三页，每页最大显示10条数据
http://127.0.0.1:8000/v1/api/gua/list?page=3&page_size=10
比如测试，我们如果请求以下接口：

http://127.0.0.1:8000/v1/api/gua/list?page=3&page_size=6
那么应该表示的是第三页，并且显示的是六条数据：


看到，是不是这样？哈哈哈哈啊。

To Be Continue
好了，今天说的内容很多，接口还有很多内容，比如权限管理啊等等，这些我日后都会说道。皮爷只有一个宗旨：就是要让你通过我的这个系列的文章，能够开发出来一套完整的系统。

这些所有代码，我都会上传到GitHub上，获取方式就是请关注微信公众号『皮爷撸码』，然后回复『网站代码』即可获得链接地址。

好了，系列文章今天这一章节就先说到这里，正好马上就要双11了，又到了一年一度买服务器的时候了。照目前的趋势，皮爷今年肯定又会购买服务器了，服务器是真的不嫌多啊，一台服务器可以写网站，两台服务器就可以玩 RPC，三台可以搞集群。。。

下面这个链接大家可以在双十一的时候在阿里云享受优惠，注意，每年就此一次，错过了可就要等一年的哦：

https://www.aliyun.com/1111/2019/group-buying-share?ptCode=59102A206508DC8B402167FFD766D480647C88CF896EF535&userCode=nrkmbo9q&share_source=copy_link

喜欢的同学，可以把皮爷的文章分享出来，让跟多的人一起来学习。这个系列教程的文章，皮爷都会讲源代码放到 GitHub 上，想要获取代码的同学，请关注微信公众号『皮爷撸码』，然后回复『网站代码』即可获得链接地址。这里有更多更好玩的东西，等你一起来学习提高。

![](https://mmbiz.qpic.cn/mmbiz_png/1jWFxptiajlLsEBtF0E1Bdub2EibbgsUrw8xJC6XZicWrx0ddHKa1WVQgj0CJEwaPWX2JIgtiaz6mzibvQJ5xhFKO0w/0?wx_fmt=png)