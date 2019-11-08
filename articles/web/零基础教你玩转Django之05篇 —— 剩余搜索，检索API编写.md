**全网第一篇系列讲述Django线上项目实战的文章。**

上一篇我们主要完成了Settings文件的拆分，用以应对不同的开发环境，运行不同的配置文件。那么这一节，我们就要来说一下剩下的一些API的编写，主要有这么几个：
- 日语单词搜索API
- CL 列表API
- 日本地震列表搜索API

### 日语单词API

这个API主要说的是搜索。

这个API主要是目前peekhub的一个板块，通过中文，日语平假名和日语片假名来搜索单词：

![001]()

看到，点击`提交搜索`就能够查询单词，这个其实是一个`form`的`POST`提交。在后台那边，处理起来很简单。但是在咱们PeekpaHub里面，我们先写成get请求：

```Python
    def get(self, request):
        response = {'code': 200}
        search_type, search_key = self.process_paramter(request)
        print('search_type: ', search_type)
        result = None
        if search_type == 1:
            result = JapLanguage.objects.filter(chinese__contains=search_key).all().order_by('levelNum').order_by('classNum')
        elif search_type == 2:
            result = JapLanguage.objects.filter(jp_chinese__contains=search_key).all().order_by('levelNum').order_by('classNum')
        elif search_type == 3:
            result = JapLanguage.objects.filter(jp_only__contains=search_key).all().order_by('levelNum').order_by('classNum')
        response['search_word'] = search_key
        response['size'] = 0 if result is None else len(result)
        response['data'] = JapSerializer(result, many=True).data
        return Response(data=response, status=200)

    def process_paramter(self, request):
        if request.GET.get('chinese') is not None:
            return 1, request.GET.get('chinese')
        elif request.GET.get('jp_ch') is not None:
            return 2, request.GET.get('jp_ch')
        elif request.GET.get('jp_only') is not None:
            return 3, request.GET.get('jp_only')
        else:
            return 0, None

```

这里面使用到了`Megic Number`，这个其实应该规避一下。啥是`Magic Number`？其实就是代码里面，如果有用数字表示的地方，最好使用一个变量名来代替它。在这里，数字表示的就是搜索的三种type，1，2，3.所以，最好还是用比如`TYPE_SEARCH_CHINESE=1`这样的命名规则来让1,2,3能够读懂。

还有一点，就是搜索语句：

```Python
result = JapLanguage.objects.filter(chinese__contains=search_key).all().order_by('levelNum').order_by('classNum')
```

这里的`filter()`函数里面，用到了`__contains`字段，这个表示在`chinese`这个变量名下面的内容，如果包含了`search_key`的就返回。同时，最后还用`levelNum`和`classNum`来做升序排列；如果要降序排列，则只需要在`className`前面加个`负号`就可以，变成`-className`。

### 重头戏，CL的API

CL是啥，我也不知道，但是我知道这个API主要功能是：
- 通过传入不同的板块ID，来展示不同板块的内容；
- 通过传入日期，来展示不同日期的内容；
- 通过传入关键字，来在不同板块实现搜索功能。

其实这几个功能还是很简单的。

#### 传不同ID展示不同板块:
这个只需要通过ID值，来选取不同的Model就可以。

```Python
if fid == self.FID_2:
    result = CaoliuFid2.objects.filter(post_day_time=day).order_by('-post_time').all()
elif fid == self.FID_4:
    result = CaoliuFid4.objects.filter(post_day_time=day).order_by('-post_time').all()
```

比如这里，如果传入的是2，那么就选择CaoliuFid2来做相对于的数据操作；如果是4，则选择CaoliuFid4。

#### 传入日期显示那天的数据：

这个代码其实和上面的代码一样。看到上面有：

```Python
result = CaoliuFid2.objects.filter(post_day_time=day).order_by('-post_time').all()
```

在`filter()`方法里面，传入的就是`日期`作为关键搜索来处理的。

#### 关键字搜索

这个还是，第一步就是通过传入板块ID来寻找对应板块的Model；第二步就是传入关键字，因为有些时候关键字可能有大小写之分，这里用 `mongoengine.queryset.visitor`的`Q` 来做处理；最后一步，搜索。

```Python
if handle_type == self.TYPE_SEARCH:
    query_set = Q(post_title__contains=search_key) | Q(post_title__contains=search_key.upper()) | Q(post_title__contains=search_key.lower())
    if fid == self.FID_2:
        result = CaoliuFid2.objects(query_set).order_by('-post_time').all()
    elif fid == self.FID_4:
        result = CaoliuFid4.objects(query_set).order_by('-post_time').all()
```

这里的`query_set`里面用到了`Q`，他的作用就是将这几个`query_set`的条件`或`起来。
最后结果是这样：

![002]()

### 日本地震信息API

基于以上两个板块的API，这个其实没啥好说的，很简单，就是取特定日期的地震信息，或者去最近三天的地震信息。

```Python
def get(self, request):
    response = {'code': 200}
    days = int(request.GET.get('days', 3))
    response['days'] = days
    now = datetime.datetime.now()
    time_day_one = now.strftime('%Y-%m-%d')
    query_set = Q(jp_time_num__startswith=time_day_one)
    for i in range(days):
        before_day = (now + datetime.timedelta(days=-i)).strftime('%Y-%m-%d')
        query_set = Q(jp_time_num__startswith=before_day) | query_set
    result = JpEarthQuake.objects(query_set).order_by('-jp_id').all()
    jp_serialiazer = JpEarthSerializer(result, many=True)
    response['data'] = jp_serialiazer.data
    return Response(data=response, status=200)
```

这里的关键就在于，有一个可以查看天数的条件，这里通过一个`for`循环来做搜索条件的`或`。

![003]()


### To be continue

好了，系列文章今天这一章节就先说到这里，下一节，我们回来说一下Django的王牌重头戏:model的操作。

正好马上就要**双11**了，又到了**一年一度买服务器的时候了**。照目前的趋势，皮爷今年肯定又会购买服务器了，服务器是真的不嫌多啊，一台服务器可以写网站，两台服务器就可以玩 RPC，三台可以搞集群。。。

下面这个链接大家可以在双十一的时候在阿里云享受优惠，注意，每年就此一次，错过了可就要等一年的哦：

> https://www.aliyun.com/1111/2019/group-buying-share?ptCode=59102A206508DC8B402167FFD766D480647C88CF896EF535&userCode=nrkmbo9q&share_source=copy_link

喜欢的同学，可以把皮爷的文章分享出来，让跟多的人一起来学习。这个系列教程的文章，皮爷都会讲源代码放到 GitHub 上，想要获取代码的同学，请关注微信公众号『**皮爷撸码**』，然后回复『**网站代码**』即可获得链接地址。这里有更多更好玩的东西，等你一起来学习提高。


