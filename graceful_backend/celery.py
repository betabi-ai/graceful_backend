from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# 设置 Django 的默认 settings 模块
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "graceful_backend.settings")

# 实例化 Celery
app = Celery("graceful_backend")

# 使用 Django 的 settings 作为配置来源
app.config_from_object("django.conf:settings", namespace="CELERY")

# 自动发现所有 Django app 中的 tasks.py 文件
app.autodiscover_tasks()
