from .base import *   #NOQA
from mongoengine import connect

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

MONGODB_DATABASES = {
    "aliyun": {
        "name": CONFIG_JSON.get("mongo_databses").get("aliyun")[0].get("gua").get("database_name"),
        "host": CONFIG_JSON.get("mongo_databses").get("aliyun")[0].get("gua").get("host"),
        "tz_aware": True,
    },
}

connect(CONFIG_JSON.get("mongo_databses").get("aliyun")[0].get("gua").get("database_name"),
        host=CONFIG_JSON.get("mongo_databses").get("aliyun")[0].get("gua").get("host"),
        port=CONFIG_JSON.get("mongo_databses").get("aliyun")[0].get("gua").get("port"))