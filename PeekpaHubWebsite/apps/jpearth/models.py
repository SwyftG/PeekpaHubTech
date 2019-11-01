from django.db import models

# Create your models here.
from mongoengine.fields import *
from mongoengine.document import Document
from PeekpaHubWebsite.settings.base import CONFIG_JSON


class JpEarthQuake(Document):
    meta = {'collection': CONFIG_JSON.get("mongo_databses").get("aliyun").get("collection_name")[2]}
    jp_create_time = StringField()
    jp_url = URLField()
    jp_title = StringField()
    jp_id = StringField()
    jp_time_num = StringField()
    jp_location_image_url = StringField()
    jp_location = StringField()
    jp_level = StringField()
    jp_max_level = StringField()
    jp_time_text = StringField()

    class Meta:
        get_latest_by = 'jp_id'
        collection = 'jpearch'