from __future__ import absolute_import, unicode_literals

# 使 Celery 应用在 Django 项目加载时启动
from .celery import app as celery_app

__all__ = ("celery_app",)
