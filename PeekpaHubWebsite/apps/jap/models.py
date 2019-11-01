from django.db import models

# Create your models here.
from mongoengine.fields import *
from mongoengine.document import Document
from PeekpaHubWebsite.settings.base import CONFIG_JSON


class JapLanguage(Document):
    meta = {'collection':CONFIG_JSON.get("mongo_databses").get("aliyun").get("collection_name")[3]}
    levelNum = StringField()
    classNum = StringField()
    chinese = StringField()
    jp_only = StringField()
    jp_chinese = StringField()
    change = StringField()
