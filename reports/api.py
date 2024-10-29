from typing import List
from ninja import Router

from django.shortcuts import get_object_or_404
from django.db.models import Q
from ninja.pagination import paginate, PageNumberPagination

from ninja_jwt.authentication import JWTAuth
from django.conf import settings
from reports.models import ReportCampagns
from reports.schemas import ReportCampagnsSchema

router = Router()

_PAGE_SIZE = getattr(settings, "PAGE_SIZE", 30)


@router.get(
    "/campaigns/{int:shopid}",
    response=List[ReportCampagnsSchema],
    tags=["campagns_reports"],
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
