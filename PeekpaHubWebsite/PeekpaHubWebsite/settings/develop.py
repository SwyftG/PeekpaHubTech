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