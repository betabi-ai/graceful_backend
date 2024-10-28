from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# 设置 Django 的默认 settings 模块
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "graceful_backend.settings")

# 实例化 Celery
app = Celery("graceful_backend")

# 使用 Django 的 settings 作为配置来源
app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.broker_transport_options = {
    "visibility_timeout": 3600,
}

app.conf.update(
    broker_transport_options={
        "visibility_timeout": 3600,  # Set the timeout for a task
        "max_retries": 5,  # Max number of retry attempts
        "interval_start": 0,  # Initial retry interval in seconds
        "interval_step": 0.2,  # Step by which interval increases per retry
    }
)

app.control.purge()  # 清除所有队列中的任务

# print("app.conf: ", app.conf.result_backend)

# 自动发现所有 Django app 中的 tasks.py 文件
app.autodiscover_tasks()
