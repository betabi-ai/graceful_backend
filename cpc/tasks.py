from django.conf import settings
from celery import shared_task

import requests


@shared_task()
def cpc_data_rmsglogin_task():
    """
    执行 rmsgloginforcpcdatas 爬虫任务
    """
    """
    curl http://localhost:6800/schedule.json -d arg1=val1 -d project=gracefulRakutenSpiders -d spider=rmsgloginforcpcdatas
    """
    print("Task started")
    r = requests.post(
        f"{settings.SCRAPYD_URL}/schedule.json",
        data={"project": "gracefulRakutenSpiders", "spider": "rmsgloginforcpcdatas"},
    )
    print(r.text)


@shared_task()
def keywords_goods_task():
    """
    执行 cpcgoodspider 爬虫任务
    """
    """
    curl http://localhost:6800/schedule.json -d arg1=val1 -d project=gracefulRakutenSpiders -d spider=cpcgoodspider
    """
    print("Task started")
    r = requests.post(
        f"{settings.SCRAPYD_URL}/schedule.json",
        data={"project": "gracefulRakutenSpiders", "spider": "cpcgoodspider"},
    )
    print(r.text)


@shared_task()
def get_goods_keywords_task():
    """
    执行 goodskeywords 爬虫任务
    """
    """
    curl http://localhost:6800/schedule.json -d arg1=val1 -d project=gracefulRakutenSpiders -d spider=goodskeywords
    """
    print("Task started")
    r = requests.post(
        f"{settings.SCRAPYD_URL}/schedule.json",
        data={"project": "gracefulRakutenSpiders", "spider": "goodskeywords"},
    )
    print(r.text)


@shared_task()
def get_goodskeywordsrank_task():
    """
    执行 goodskeywordsrank 爬虫任务
    """
    """
    curl http://localhost:6800/schedule.json -d arg1=val1 -d project=gracefulRakutenSpiders -d spider=goodskeywordsrank
    """
    print("Task started")
    r = requests.post(
        f"{settings.SCRAPYD_URL}/schedule.json",
        data={"project": "gracefulRakutenSpiders", "spider": "goodskeywordsrank"},
    )
    print(r.text)


@shared_task()
def handle_shopgoodglogin_task():
    """
    执行 shopgoodglogin 爬虫任务
    """
    """
    curl http://localhost:6800/schedule.json -d arg1=val1 -d project=gracefulRakutenSpiders -d spider=shopgoodglogin
    """
    print("Task started")
    r = requests.post(
        f"{settings.SCRAPYD_URL}/schedule.json",
        data={"project": "gracefulRakutenSpiders", "spider": "shopgoodglogin"},
    )
    print(r.text)


@shared_task()
def get_shopgoodsspider_task():
    """
    执行 shopgoodsspider 爬虫任务
    """
    """
    curl http://localhost:6800/schedule.json -d arg1=val1 -d project=gracefulRakutenSpiders -d spider=shopgoodsspider
    """
    print("Task started")
    r = requests.post(
        f"{settings.SCRAPYD_URL}/schedule.json",
        data={"project": "gracefulRakutenSpiders", "spider": "shopgoodsspider"},
    )
    print(r.text)
