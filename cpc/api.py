from typing import List
from ninja import Router

from django.shortcuts import get_object_or_404
from django.db.models import Q
from ninja.pagination import paginate, PageNumberPagination

from cpc.models import CpcGoodKeywords, CpcKeywordsGoods, TopKeywords
from cpc.schemas import (
    CpcGoodKeywordsSchema,
    CpcKeywordEnableChangeINSchema,
    CpcProductsSchema,
    Message,
    TopKeywordsSchema,
)
from ninja_jwt.authentication import JWTAuth

router = Router()

_PAGE_SIZE = 30


@router.get(
    "/products/{int:shopid}",
    response=List[CpcProductsSchema],
    tags=["cpc_products"],
    auth=JWTAuth(),
)
@paginate(PageNumberPagination, page_size=_PAGE_SIZE)
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
@paginate(PageNumberPagination, page_size=_PAGE_SIZE)
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
@paginate(PageNumberPagination, page_size=_PAGE_SIZE)
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
@paginate(PageNumberPagination, page_size=_PAGE_SIZE)
def get_top_keywords_by_shopid(request, shopid: int, dtype: int = 1, q: str = ""):
    """
    获取指定shopid的CPC关键词排行榜
    """
    # print(shopid, dtype, q)
    query = Q(shopid=shopid) & Q(date_type=dtype)
    if q:
        query &= Q(search_word__icontains=q) | Q(itemmngid__icontains=q)

    qs = TopKeywords.objects.filter(query).order_by("-ldate")
    # print("=============top keyword:\n", qs.query)
    return qs


@router.patch(
    "/keywords/checkenable",
    response={200: CpcGoodKeywordsSchema, 422: Message},
    tags=["update_cpc_keywords"],
    # auth=JWTAuth(),
    auth=None,
)
def update_goods_keywords(request, item: CpcKeywordEnableChangeINSchema):
    """
    更新指定id的CPC关键词的 enabled_cpc 字段
    """
    # print("....................", item.id, item.enabled_cpc)
    obj = get_object_or_404(CpcGoodKeywords, id=item.id)

    if item.weightvalue:
        query = (
            Q(weightvalue=item.weightvalue)
            & Q(shopid=item.shopid)
            & Q(keyword=item.keyword)
            & ~Q(id=item.id)
        )
        other_same_keywords = CpcGoodKeywords.objects.filter(query)
        if other_same_keywords.exists():
            return 422, {"message": "已存在相同权重值的关键词"}

    update_data = {k: v for k, v in item.dict().items() if v is not None}
    print(update_data)
    CpcGoodKeywords.objects.filter(id=item.id).update(**update_data)

    obj.refresh_from_db()
    return obj
