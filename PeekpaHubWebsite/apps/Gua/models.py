from mongoengine.fields import *
from mongoengine.document import Document
from PeekpaHubWebsite.settings.base import CONFIG_JSON

# Create your models here.

class Gua(Document):
    meta = {'collection': CONFIG_JSON.get("mongo_databses").get("aliyun").get("collection_name")[0]}
    gua_number = StringField()
    gua_sub_title = StringField()
    gua_title = StringField()
    gua_serial_text = StringField()
    gua_serial = StringField()
    gua_one = StringField()
    gua_two = StringField()
    gua_three = StringField()
    gua_four = StringField()
    gua_five = StringField()


class GuaRModel(Document):
    meta = {'collection': CONFIG_JSON.get("mongo_databses").get("aliyun").get("collection_name")[1]}
    appVersion = StringField()
    checkNum = StringField()
    reportTime = StringField()
    nickName = StringField()
    avatarUrl = StringField()
    city = StringField()
    province = StringField()
    country = StringField()
    gender = StringField()
    fromPage = StringField()
    _class = StringField()
    dayTime = StringField()
    guaName = StringField()
