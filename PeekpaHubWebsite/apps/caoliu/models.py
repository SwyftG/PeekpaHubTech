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

    def __str__(self):
        return "block_id: {}, {}".format(self.block_id, self.post_title)


class CaoliuFid2(CaoliuBase):
    meta = {'collection': CONFIG_JSON.get("mongo_databses").get("aliyun").get("collection_name_caoliu").get('fid2')}

    @staticmethod
    def check_by_time(time):
        try:
            result = CaoliuFid2.objects(post_day_time=time).all()
        except CaoliuFid2.DoesNotExist:
            result = None
        return result, str(result.count())


class CaoliuFid4(CaoliuBase):
    meta = {'collection': CONFIG_JSON.get("mongo_databses").get("aliyun").get("collection_name_caoliu").get('fid4')}

    @staticmethod
    def check_by_time(time):
        try:
            result = CaoliuFid4.objects(post_day_time=time).all()
        except CaoliuFid4.DoesNotExist:
            result = None
        return result, str(result.count())


class CaoliuFid7(CaoliuBase):
    meta = {'collection': CONFIG_JSON.get("mongo_databses").get("aliyun").get("collection_name_caoliu").get('fid7')}

    @staticmethod
    def check_by_time(time):
        try:
            result = CaoliuFid7.objects(post_day_time=time).all()
        except CaoliuFid7.DoesNotExist:
            result = None
        return result, str(result.count())


class CaoliuFid15(CaoliuBase):
    meta = {'collection': CONFIG_JSON.get("mongo_databses").get("aliyun").get("collection_name_caoliu").get('fid15')}

    @staticmethod
    def check_by_time(time):
        try:
            result = CaoliuFid15.objects(post_day_time=time).all()
        except CaoliuFid15.DoesNotExist:
            result = None
        return result, str(result.count())


class CaoliuFid25(CaoliuBase):
    meta = {'collection': CONFIG_JSON.get("mongo_databses").get("aliyun").get("collection_name_caoliu").get('fid25')}

    @staticmethod
    def check_by_time(time):
        try:
            result = CaoliuFid25.objects(post_day_time=time).all()
        except CaoliuFid25.DoesNotExist:
            result = None
        return result, str(result.count())


class CaoliuFid26(CaoliuBase):
    meta = {'collection': CONFIG_JSON.get("mongo_databses").get("aliyun").get("collection_name_caoliu").get('fid26')}

    @staticmethod
    def check_by_time(time):
        try:
            result = CaoliuFid26.objects(post_day_time=time).all()
        except CaoliuFid26.DoesNotExist:
            result = None
        return result, str(result.count())
