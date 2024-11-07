from typing import Any, List
from ninja import Router

from django.shortcuts import get_object_or_404
from django.db.models import Q, F
from ninja.pagination import paginate, PageNumberPagination

from ninja_jwt.authentication import JWTAuth
from django.conf import settings
from reports.models import ReportCampagns, ReportGoods, ReportKeywords
from reports.schemas import (
    ReportCampagnsSchema,
    ReportGoodsSchema,
    ReportKeywordsSchema,
)

router = Router()

_PAGE_SIZE = getattr(settings, "PAGE_SIZE", 30)

# =============================================campaigns reports===================================================


@router.get(
    "/campaigns/{int:shopid}",
    response=List[ReportCampagnsSchema],
    tags=["reports"],
    auth=JWTAuth(),
)
@paginate(PageNumberPagination, page_size=_PAGE_SIZE)
def get_campaigns(request, shopid: int, periodtype: int = 1):
    """
    获取指定 shopid 的 活动报表数据
    :param request:
    :param shopid: 店铺ID
    :param periodtype: 0或2: 日报,  1:月报
    """
    query = Q(shopid=shopid)
    if periodtype == 0:
        query &= Q(periodtype=0) | Q(periodtype=2)
    else:
        query &= Q(periodtype=periodtype)
    qs = ReportCampagns.objects.filter(query).order_by("-effectdate")
    print(qs.query)
    return qs


@router.get(
    "/campaigns/chart/{int:shopid}",
    response=List[ReportCampagnsSchema],
    tags=["reports"],
    auth=JWTAuth(),
)
def get_campaigns_reports_by_date(
    request, shopid: int, periodtype: int = 2, start: str = None, end: str = None
):
    """
    获取指定 shopid 的 活动报表数据,根据日期，并且不需要进行分页
    :param request:
    :param shopid: 店铺ID
    :param periodtype: 0或2: 日报,  1:月报
    """
    query = Q(shopid=shopid)
    if start and end:
        query &= Q(startdate__range=(start, end))
    if periodtype == 0:
        query &= Q(periodtype=0) | Q(periodtype=2)
    else:
        query &= Q(periodtype=periodtype)
    qs = ReportCampagns.objects.filter(query, startdate=F("enddate")).order_by(
        "effectdate"
    )
    # print("************")
    # print(qs.query)
    return qs


# ================================================================================================

# =============================================keywords reports===================================================


@router.get(
    "/keywords/chart/{int:shopid}",
    response=List[ReportKeywordsSchema],
    tags=["reports"],
    auth=JWTAuth(),
)
def get_keywords_reports_by_con(
    request,
    shopid: int,
    start: str = None,
    end: str = None,
    kw: str = None,
    itemurl: str = None,
    ptype: int = 1,
):
    """
    获取指定 shopid 的 关键词报表数据
    :param request:
    :param shopid: 店铺ID
    :param periodtype: 0或2: 日报,  1:月报
    """
    # print("^^^^^^^^^^^^^^^^^^^^^")
    query = Q(shopid=shopid)
    query &= Q(periodtype=ptype)
    if start and end:
        query &= Q(effectdate__range=(start, end))
    if kw:  # and kw != "all" and kw != "null":
        query &= Q(keywordstring=kw)
    if itemurl:
        query &= Q(itemurl=itemurl)
    qs = ReportKeywords.objects.filter(query).order_by("effectdate")
    print(qs.query)

    return qs


@router.get(
    "/keywords/{int:shopid}",
    response=List[ReportKeywordsSchema],
    tags=["reports"],
    auth=JWTAuth(),
)
@paginate(PageNumberPagination, page_size=_PAGE_SIZE)
def get_keywords_reports(
    request,
    shopid: int,
    start: str = None,
    end: str = None,
    kw: str = None,
    itemurl: str = None,
    ptype: int = 1,
):
    """
    获取指定 shopid 的 关键词报表数据
    :param request:
    :param shopid: 店铺ID
    :param periodtype: 0或2: 日报,  1:月报
    """
    # print("^^^^^^^^^^^^^^^^^^^^^")
    query = Q(shopid=shopid)
    query &= Q(periodtype=ptype)
    if start and end:
        query &= Q(effectdate__range=(start, end))
    if kw and kw != "all" and kw != "null":
        query &= Q(keywordstring=kw)
    if itemurl:
        query &= Q(itemurl=itemurl)
    qs = ReportKeywords.objects.filter(query).order_by("-effectdate")
    print(qs.query)

    return qs


# ================================================================================================

# =============================================product reports===================================================


@router.get(
    "/products/{int:shopid}",
    response=List[ReportGoodsSchema],
    tags=["reports"],
    auth=JWTAuth(),
)
@paginate(PageNumberPagination, page_size=_PAGE_SIZE)
def get_products_reports(request, shopid: int, periodtype: int = 1):
    """
    获取指定 shopid 的 商品报表数据
    :param request:
    :param shopid: 店铺ID
    :param periodtype: 0: 日报,  1:月报
    """

    query = Q(shopid=shopid) & Q(periodtype=periodtype)
    qs = ReportGoods.objects.filter(query).order_by("-effectdate")
    print(qs.query)
    return qs


@router.get(
    "/products/chart/{int:shopid}",
    response=List[ReportGoodsSchema],
    tags=["reports"],
    auth=JWTAuth(),
)
def get_products_reports_by_date(
    request,
    shopid: int,
    itemurl: str,
    periodtype: int = 0,
    start: str = None,
    end: str = None,
):
    """
    获取指定 shopid 的 商品报表数据,根据日期，并且不需要进行分页
    :param request:
    :param shopid: 店铺ID
    :param periodtype: 0或2: 日报,  1:月报
    """
    query = Q(shopid=shopid)
    query &= Q(periodtype=periodtype)
    if itemurl:
        query &= Q(itemurl=itemurl)
    if start and end:
        query &= Q(effectdate__range=(start, end))
    # if periodtype:

    qs = ReportGoods.objects.filter(query).order_by("effectdate")
    print("************sssssss")
    print(qs.query)
    print(len(qs))
    return qs


# =================================================================================================
