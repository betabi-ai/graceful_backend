from typing import List
from ninja import Router, Schema

from django.shortcuts import get_object_or_404
from django.db.models import Q
from ninja.pagination import paginate, PageNumberPagination

from cpc.models import CpcGoodKeywords, CpcKeywordsGoods, TopKeywords
from cpc.schemas import (
    CpcGoodKeywordsSchema,
    CpcKeywordEnableChangeINSchema,
    CpcProductsSchema,
    TopKeywordsSchema,
)
from helpers.custom_pagination import CustomPagination
from ninja_jwt.authentication import JWTAuth

router = Router()


@router.get(
    "/products/{int:shopid}",
    response=List[CpcProductsSchema],
    tags=["cpc_products"],
    auth=JWTAuth(),
)
@paginate(PageNumberPagination, page_size=50)
def get_cpc_products(request, shopid: int, q: str = None):
    """
    获取指定shopid的CPC商品
    如果有查询参数q，则根据商品管理ID或商品名称进行模糊查询
    """
    query = Q(shopid=shopid)
    if q:
        query &= Q(itemmngid__icontains=q) | Q(itemname__icontains=q)
    qs = CpcKeywordsGoods.objects.filter(query).order_by("itemmngid")
    print(qs.query)
    return qs


@router.get(
    "/keywords/{int:shopid}",
    response=List[CpcGoodKeywordsSchema],
    tags=["cpc_keywords"],
    auth=JWTAuth(),
)
@paginate(PageNumberPagination, page_size=50)
# @paginate(CustomPagination)
def get_cpc_keywords_by_shopid(request, shopid: int, q: str = ""):
    """
    获取指定shopid的CPC关键词
    """
    print(shopid, q)
    print(shopid)
    query = Q(shopid=shopid)
    if q:
        query &= Q(keyword__icontains=q) | Q(itemmngid__icontains=q)

    qs = CpcGoodKeywords.objects.filter(query).order_by("-enabled_cpc", "itemmngid")
    # print(qs.query)
    return qs


@router.get(
    "/keywords/{int:shopid}/{str:itemmngid}",
    response=List[CpcGoodKeywordsSchema],
    tags=["cpc_itemmngid_keywords"],
    auth=JWTAuth(),
)
@paginate(PageNumberPagination)
def get_cpc_keywords_by_itemmngid(request, shopid: int, itemmngid: str):
    """
    获取指定shopid下的指定itemmngid下的CPC关键词列表
    """
    query = Q(shopid=shopid)
    query &= Q(itemmngid=itemmngid)
    qs = CpcGoodKeywords.objects.filter(query).order_by("-enabled_cpc", "keyword")
    return qs


@router.get(
    "/top_keywords/{int:shopid}",
    response=List[TopKeywordsSchema],
    tags=["top_five_keywords"],
    auth=JWTAuth(),
)
@paginate(PageNumberPagination)
def get_top_keywords_by_shopid(request, shopid: int, dtype: int = 1, q: str = ""):
    """
    获取指定shopid的CPC关键词排行榜
    """
    # print(shopid, dtype, q)
    query = Q(shopid=shopid) & Q(date_type=dtype)
    if q:
        query &= Q(search_word__icontains=q) | Q(itemmngid__icontains=q)

    qs = TopKeywords.objects.filter(query).order_by("-ldate")
    return qs


@router.patch(
    "/keywords/checkenable",
    response=CpcGoodKeywordsSchema,
    tags=["update_cpc_keywords"],
    # auth=JWTAuth(),
    auth=None,
)
def check_cpc_enabled(request, item: CpcKeywordEnableChangeINSchema):
    """
    更新指定id的CPC关键词的 enabled_cpc 字段
    """
    # print("....................", item.id, item.enabled_cpc)
    obj = get_object_or_404(CpcGoodKeywords, id=item.id)
    # print(obj)
    obj.enabled_cpc = item.enabled_cpc
    obj.save()
    return obj
