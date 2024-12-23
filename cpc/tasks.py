from django.conf import settings
from celery import shared_task

import requests

SCHEDULE_URL = f"{settings.SCRAPYD_URL}/schedule.json"


@shared_task()
def handle_spider(**spider_args):
    """
    通用 爬虫任务
    spider_args参数中必须要包括【project】和【spider】：spider_args: {
        "project": "gracefulRakutenSpiders",
        "spider": "cpc_goods_spider",
        "shopid":"421947",
    }
    """
    project = spider_args.get("project", None)
    spider = spider_args.get("spider", None)
    if not project or not spider:
        return
    # data = {"project": "gracefulRakutenSpiders", "spider": "cpc_goods_spider"}
    # data.update(spider_args)
    try:
        response = requests.post(SCHEDULE_URL, data=spider_args)
        return response.json()
    except Exception as e:
        print(e)


@shared_task()
def cpc_goods_spider_task(**spider_args):
    """
    执行 cpc_goods_spider 爬虫任务
    获取设置了 关键词 的商品列表
    """
    """
    curl http://localhost:6800/schedule.json -d arg1=val1 -d project=gracefulRakutenSpiders -d spider=cpc_goods_spider
    """
    print("Task started")

    data = {"project": "gracefulRakutenSpiders", "spider": "cpc_goods_spider"}
    data.update(spider_args)
    response = requests.post(SCHEDULE_URL, data=data)
    return response.json()


@shared_task()
def goods_keywords_spider_task(**spider_args):
    """
    执行 goods_keywords_spider 爬虫任务
    获取所有设置了关键词广告的商品的关键词信息
    """
    """
    curl http://localhost:6800/schedule.json -d arg1=val1 -d project=gracefulRakutenSpiders -d spider=goods_keywords_spider
    """
    print("Task started")

    data = {"project": "gracefulRakutenSpiders", "spider": "goods_keywords_spider"}
    data.update(spider_args)
    response = requests.post(SCHEDULE_URL, data=data)
    return response.json()


@shared_task()
def report_campaigns_day_spider_task(**spider_args):
    """
    执行 report_campaigns_day_spider 爬虫任务
    下载广告活动数据日报告
    """
    """
    curl http://localhost:6800/schedule.json -d arg1=val1 -d project=gracefulRakutenSpiders -d spider=report_campaigns_day_spider
    """
    print("Task started")

    data = {
        "project": "gracefulRakutenSpiders",
        "spider": "report_campaigns_day_spider",
    }
    data.update(spider_args)
    response = requests.post(SCHEDULE_URL, data=data)
    return response.json()


@shared_task()
def report_campaigns_month_spider_task(**spider_args):
    """
    执行 report_campaigns_month_spider 爬虫任务
    下载广告活动数据月报告
    """
    """
    curl http://localhost:6800/schedule.json -d arg1=val1 -d project=gracefulRakutenSpiders -d spider=report_campaigns_month_spider
    """
    print("Task started")

    data = {
        "project": "gracefulRakutenSpiders",
        "spider": "report_campaigns_month_spider",
    }
    data.update(spider_args)
    response = requests.post(SCHEDULE_URL, data=data)
    return response.json()


@shared_task()
def report_goods_async_day_spider_task(**spider_args):
    """
    执行 report_goods_async_day_spider 爬虫任务
    生成商品类别的报告(按日)
    """
    """
    curl http://localhost:6800/schedule.json -d arg1=val1 -d project=gracefulRakutenSpiders -d spider=report_goods_async_day_spider
    """
    print("Task started")
    data = {
        "project": "gracefulRakutenSpiders",
        "spider": "report_goods_async_day_spider",
    }
    data.update(spider_args)
    response = requests.post(SCHEDULE_URL, data=data)
    return response.json()


@shared_task()
def report_goods_async_month_spider_task(**spider_args):
    """
    执行 report_goods_async_month_spider 爬虫任务
    生成商品类别的报告(按月)
    """
    """
    curl http://localhost:6800/schedule.json -d arg1=val1 -d project=gracefulRakutenSpiders -d spider=report_goods_async_month_spider
    """
    print("Task started")

    data = {
        "project": "gracefulRakutenSpiders",
        "spider": "report_goods_async_month_spider",
    }
    data.update(spider_args)
    response = requests.post(SCHEDULE_URL, data=data)
    return response.json()


@shared_task()
def report_goods_download_spider_task(**spider_args):
    """
    执行 report_goods_download_spider 爬虫任务
    下载商品类别报告(按日，按月)
    """
    """
    curl http://localhost:6800/schedule.json -d arg1=val1 -d project=gracefulRakutenSpiders -d spider=report_goods_download_spider
    """
    print("Task started")
    data = {
        "project": "gracefulRakutenSpiders",
        "spider": "report_goods_download_spider",
    }
    data.update(spider_args)
    response = requests.post(SCHEDULE_URL, data=data)
    return response.json()


@shared_task()
def report_keywords_async_day_spider_task(**spider_args):
    """
    执行 report_keywords_async_day_spider 爬虫任务
    生成关键词的报告(按日)
    """
    """
    curl http://localhost:6800/schedule.json -d arg1=val1 -d project=gracefulRakutenSpiders -d spider=report_keywords_async_day_spider
    """
    print("Task started")
    data = {
        "project": "gracefulRakutenSpiders",
        "spider": "report_keywords_async_day_spider",
    }
    data.update(spider_args)
    response = requests.post(SCHEDULE_URL, data=data)
    return response.json()


@shared_task()
def report_keywords_async_month_spider_task(**spider_args):
    """
    执行 report_keywords_async_month_spider 爬虫任务
    生成关键词的报告(按日)
    """
    """
    curl http://localhost:6800/schedule.json -d arg1=val1 -d project=gracefulRakutenSpiders -d spider=report_keywords_async_month_spider
    """
    print("Task started")
    data = {
        "project": "gracefulRakutenSpiders",
        "spider": "report_keywords_async_month_spider",
    }
    data.update(spider_args)
    response = requests.post(SCHEDULE_URL, data=data)
    return response.json()


@shared_task()
def report_keywords_download_spider_task(**spider_args):
    """
    执行 report_keywords_download_spider 爬虫任务
    下载关键词类别报告(按日，按月)
    """
    """
    curl http://localhost:6800/schedule.json -d arg1=val1 -d project=gracefulRakutenSpiders -d spider=report_keywords_download_spider
    """
    print("Task started")

    data = {
        "project": "gracefulRakutenSpiders",
        "spider": "report_keywords_download_spider",
    }
    data.update(spider_args)
    response = requests.post(SCHEDULE_URL, data=data)
    return response.json()


@shared_task()
def report_wait_download_spider_task(**spider_args):
    """
    执行 report_wait_download_spider 爬虫任务
    下载等待下载的报告列表
    """
    """
    curl http://localhost:6800/schedule.json -d arg1=val1 -d project=gracefulRakutenSpiders -d spider=report_wait_download_spider
    """
    print("Task started")

    data = {
        "project": "gracefulRakutenSpiders",
        "spider": "report_wait_download_spider",
    }
    data.update(spider_args)
    response = requests.post(SCHEDULE_URL, data=data)
    return response.json()


@shared_task()
def update_cpc_spider_task(**spider_args):
    """
    执行 update_cpc_spider 爬虫任务
    更新商品关键词的cpc
    """
    """
    curl http://localhost:6800/schedule.json -d arg1=val1 -d project=gracefulRakutenSpiders -d spider=update_cpc_spider
    """
    print("Task started")

    data = {
        "project": "gracefulRakutenSpiders",
        "spider": "update_cpc_spider",
    }
    data.update(spider_args)
    response = requests.post(SCHEDULE_URL, data=data)
    return response.json()


@shared_task()
def shop_goods_spider_task(**spider_args):
    """
    执行 shop_goods_spider 爬虫任务
    获取店铺所有商品列表
    """
    """
    curl http://localhost:6800/schedule.json -d arg1=val1 -d project=gracefulRakutenSpiders -d spider=shop_goods_spider
    """
    print("Task started")

    data = {
        "project": "gracefulRakutenSpiders",
        "spider": "shop_goods_spider",
    }
    data.update(spider_args)
    response = requests.post(SCHEDULE_URL, data=data)
    return response.json()


@shared_task()
def top_five_keyword_search_datas_spider_task(**spider_args):
    """
    执行 top_five_keyword_search_datas_spider 爬虫任务
    获取每月1号到当前日期的关键词搜索数据爬虫，乐天现只提供排名前30的商品数据
    """
    """
    curl http://localhost:6800/schedule.json -d arg1=val1 -d project=gracefulRakutenSpiders -d spider=top_five_keyword_search_datas_spider
    """

    data = {
        "project": "gracefulRakutenSpiders",
        "spider": "top_five_keyword_search_datas_spider",
    }
    data.update(spider_args)
    response = requests.post(SCHEDULE_URL, data=data)
    return response.json()


@shared_task()
def goods_keywords_rank_spider_task(**spider_args):
    """
    执行 goods_keywords_rank_spider 爬虫任务
    抓取关键词 商品排名
    """
    """
    curl http://localhost:6800/schedule.json -d arg1=val1 -d project=gracefulRakutenSpiders -d spider=goods_keywords_rank_spider
    """
    print("Task started")
    data = {
        "project": "gracefulRakutenSpiders",
        "spider": "goods_keywords_rank_spider",
    }
    data.update(spider_args)
    response = requests.post(SCHEDULE_URL, data=data)
    return response.json()


#


@shared_task()
def campaigns_budget_spider_task(**spider_args):
    """
    执行 campaigns_budget_spider 爬虫任务
    获取广告活动的预算数据
    """
    """
    curl http://localhost:6800/schedule.json -d arg1=val1 -d project=gracefulRakutenSpiders -d spider=campaigns_budget_spider
    """
    print("Task started")
    data = {
        "project": "gracefulRakutenSpiders",
        "spider": "campaigns_budget_spider",
    }
    data.update(spider_args)
    response = requests.post(SCHEDULE_URL, data=data)
    return response.json()


@shared_task()
def campaigns_budget_calc_tmp_task(**spider_args):
    """
    执行 campaigns_budget_calc_tmp 爬虫任务
    下载关键词类别报告(按日，按月)
    """
    """
    curl http://localhost:6800/schedule.json -d arg1=val1 -d project=gracefulRakutenSpiders -d spider=campaigns_budget_calc_tmp
    """
    print("Task started")

    data = {
        "project": "gracefulRakutenSpiders",
        "spider": "campaigns_budget_calc_tmp",
    }
    data.update(spider_args)
    response = requests.post(SCHEDULE_URL, data=data)
    return response.json()


@shared_task()
def refresh_rrp_cookies_task(**spider_args):
    """
    执行 refresh_rrp_cookies 爬虫任务
    刷新rrp的cookies
    """
    """
    curl http://localhost:6800/schedule.json -d arg1=val1 -d project=gracefulRakutenSpiders -d spider=refresh_rrp_cookies
    """
    print("Task started")

    data = {
        "project": "gracefulRakutenSpiders",
        "spider": "refresh_rrp_cookies",
    }
    data.update(spider_args)
    response = requests.post(SCHEDULE_URL, data=data)
    return response.json()


@shared_task()
def campaigns_budget_login_spider_task(**spider_args):
    """
    执行 campaigns_budget_login_spider 爬虫任务
    刷新rrp的cookies
    """
    """
    curl http://localhost:6800/schedule.json -d arg1=val1 -d project=gracefulRakutenSpiders -d spider=campaigns_budget_login_spider
    """
    print("Task started")

    data = {
        "project": "gracefulRakutenSpiders",
        "spider": "campaigns_budget_login_spider",
    }
    data.update(spider_args)
    response = requests.post(SCHEDULE_URL, data=data)
    return response.json()


@shared_task()
def ranking_rakuten_task(**spider_args):
    """
    执行 ranking_rakuten 爬虫任务
    刷新rrp的cookies
    """
    """
    curl http://localhost:6800/schedule.json -d arg1=val1 -d project=gracefulRakutenSpiders -d spider=ranking_rakuten
    """
    print("Task started")

    data = {
        "project": "gracefulRakutenSpiders",
        "spider": "ranking_rakuten",
    }
    data.update(spider_args)
    response = requests.post(SCHEDULE_URL, data=data)
    return response.json()
