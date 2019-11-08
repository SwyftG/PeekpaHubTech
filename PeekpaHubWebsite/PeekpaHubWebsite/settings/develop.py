from .base import *   #NOQA
from mongoengine import connect

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

connect(CONFIG_JSON.get("mongo_databses").get("aliyun").get("config").get("database_name"),
        host=CONFIG_JSON.get("mongo_databses").get("aliyun").get("config").get("host"),
        port=CONFIG_JSON.get("mongo_databses").get("aliyun").get("config").get("port"))


# 设置邮件域名
EMAIL_HOST = CONFIG_JSON.get("email_setting").get("daily_check").get("EMAIL_HOST")
# 设置端口号，为数字
EMAIL_PORT = CONFIG_JSON.get("email_setting").get("daily_check").get("EMAIL_PORT")
#设置发件人邮箱
EMAIL_HOST_USER = CONFIG_JSON.get("email_setting").get("daily_check").get("EMAIL_HOST_USER")
# 设置发件人 授权码
EMAIL_HOST_PASSWORD = CONFIG_JSON.get("email_setting").get("daily_check").get("EMAIL_HOST_PASSWORD")
# 设置是否启用安全链接
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
EMAIL_USE_SSL = True