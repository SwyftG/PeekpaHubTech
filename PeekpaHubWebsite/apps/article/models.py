from django.db import models

# Create your models here.
from mongoengine.document import Document
from mongoengine.fields import StringField


class Article(Document):
    meta = {'collection': 'Article'}
    title = StringField()
    author = StringField()
    content = StringField()
    context_html = StringField()
    image = StringField()

