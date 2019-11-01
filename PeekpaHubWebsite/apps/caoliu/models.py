from django.db import models

# Create your models here.
from mongoengine.fields import *
from mongoengine.document import Document
from PeekpaHubWebsite.settings.base import CONFIG_JSON


class CaoliuBase(Document):
    meta = {'abstract': True}
    block_id = StringField()
    post_id = StringField()
    post_title = StringField()
    post_time = StringField()
    post_url = StringField()
    post_part_url = StringField()
    post_day_time = StringField()


class CaoliuFid2(CaoliuBase):
    meta = {'collection': CONFIG_JSON.get("mongo_databses").get("aliyun").get("collection_name_caoliu").get('fid2')}


class CaoliuFid4(CaoliuBase):
    meta = {'collection': CONFIG_JSON.get("mongo_databses").get("aliyun").get("collection_name_caoliu").get('fid4')}


class CaoliuFid7(CaoliuBase):
    meta = {'collection': CONFIG_JSON.get("mongo_databses").get("aliyun").get("collection_name_caoliu").get('fid7')}


class CaoliuFid15(CaoliuBase):
    meta = {'collection': CONFIG_JSON.get("mongo_databses").get("aliyun").get("collection_name_caoliu").get('fid15')}


class CaoliuFid25(CaoliuBase):
    meta = {'collection': CONFIG_JSON.get("mongo_databses").get("aliyun").get("collection_name_caoliu").get('fid25')}


class CaoliuFid26(CaoliuBase):
    meta = {'collection': CONFIG_JSON.get("mongo_databses").get("aliyun").get("collection_name_caoliu").get('fid26')}
