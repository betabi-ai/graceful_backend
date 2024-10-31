from typing import Any, List
from ninja import Router

from django.shortcuts import get_object_or_404
from django.db.models import Q
from ninja.pagination import paginate, PageNumberPagination

from ninja_jwt.authentication import JWTAuth
from django.conf import settings
from reports.models import ReportCampagns, ReportKeywords
from reports.schemas import ReportCampagnsSchema, ReportKeywordsSchema

router = Router()

_PAGE_SIZE = getattr(settings, "PAGE_SIZE", 30)


@router.get(
    "/campaigns/{int:shopid}",
    response=List[ReportCampagnsSchema],
    tags=["reports"],
    # auth=JWTAuth(),
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
    "/keywords/{int:shopid}",
    response=List[ReportKeywordsSchema],
    tags=["reports"],
    auth=None,
)
def get_keywords_reports(
    request,
    shopid: int,
    start: str = None,
    end: str = None,
    kw: str = None,
    pd: str = None,
    ptype: int = 1,
):
    """
    获取指定 shopid 的 关键词报表数据
    :param request:
    :param shopid: 店铺ID
    :param periodtype: 0或2: 日报,  1:月报
    """
    print("^^^^^^^^^^^^^^^^^^^^^")
    query = Q(shopid=shopid)
    if ptype:
        query &= Q(periodtype=ptype)
    if start and end:
        query &= Q(effectdate__range=(start, end))
    if kw:
        query &= Q(keywordstring=kw)
    if pd:
        query &= Q(itemurl=pd)
    qs = ReportKeywords.objects.filter(query).order_by("effectdate")

    return qs
