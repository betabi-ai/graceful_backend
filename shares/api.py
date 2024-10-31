from typing import List, Any
from django.conf import settings
from ninja import Router
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.db.models import Q
from ninja.pagination import paginate, PageNumberPagination

from ninja_jwt.authentication import JWTAuth

from shares.models import CpcKeywordsGoods

router = Router()


@router.get(
    "/cpc_products/{int:shopid}",
    response=List[Any],
    tags=["cpc.reports"],
    auth=None,
)
def get_all_cpc_products(request, shopid: int):
    return (
        CpcKeywordsGoods.objects.filter(shopid=shopid)
        .values("itemmngid", "itemid")
        .order_by("itemmngid")
    )
