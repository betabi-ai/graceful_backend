from typing import List
from ninja import Router

from django.shortcuts import get_object_or_404
from django.db.models import Q
from ninja.pagination import paginate, PageNumberPagination

from ninja_jwt.authentication import JWTAuth

from reports.models import ReportCampagns
from reports.schemas import ReportCampagnsSchema

router = Router()

_PAGE_SIZE = 30


@router.get(
    "/campaigns/{int:shopid}",
    response=List[ReportCampagnsSchema],
    tags=["campagns_reports"],
    # auth=JWTAuth(),
    auth=None,
)
@paginate(PageNumberPagination, page_size=_PAGE_SIZE)
def get_cpc_products(request, shopid: int, periodtype: int = 1):
    """
    获取指定shopid的CPC商品
    如果有查询参数q，则根据商品管理ID或商品名称进行模糊查询
    """
    query = Q(shopid=shopid)
    if periodtype == 0:
        query &= Q(periodtype=0) | Q(periodtype=2)
    else:
        query &= Q(periodtype=periodtype)
    qs = ReportCampagns.objects.filter(query).order_by("-effectdate")
    print(qs.query)
    return qs
