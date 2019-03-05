from __future__ import absolute_import, unicode_literals
import os
from celery import Celery


# 把置默认的django settings模块配置给celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dailyfresh.settings')

app = Celery('dailyfresh')
app.autodiscover_tasks()

# 这里使用字符串以使celery的worker不用为子进程序列化配置对象。
# 命名空间 namespace='CELERY'定义所有与celery相关的配置的键名要以'CELERY_'为前缀。
app.config_from_object('django.conf:settings', namespace='CELERY')

