from typing import List, Any
from django.conf import settings
from ninja import Router
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.db.models import Q
from ninja.pagination import paginate, PageNumberPagination

from ninja_jwt.authentication import JWTAuth

from shares.models import CpcGoodKeywords, CpcKeywordsGoods

router = Router()


@router.get(
    "/products/{int:shopid}",
    response=List[Any],
    tags=["shares"],
    auth=JWTAuth(),
)
def get_all_cpc_products(request, shopid: int):
    """
    获取店铺所有的cpc商品,只返回商品id和商品管理id
    """
    return (
        CpcKeywordsGoods.objects.filter(shopid=shopid)
        .values("itemmngid", "itemid")
        .order_by("itemmngid")
    )


@router.get(
    "/products/{int:shopid}/{str:itemmngid}",
    response=List[Any],
    tags=["shares"],
    auth=JWTAuth(),
)
def get_product_keywords(request, shopid: int, itemmngid: str):
    """
    获取指定商品的关键词
    """
    return (
        CpcGoodKeywords.objects.filter(shopid=shopid, itemmngid=itemmngid)
        .values("keyword", "id")
        .order_by("keyword")
    )