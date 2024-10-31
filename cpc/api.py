from typing import List, Any
from django.conf import settings
from ninja import Router
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.db.models import Q
from ninja.pagination import paginate, PageNumberPagination

from shares.models import CpcGoodKeywords, CpcKeywordsGoods, TopKeywords
from cpc.schemas import (
    CampaignsMonthSchema,
    CpcGoodKeywordsSchema,
    CpcKeywordEnableChangeINSchema,
    CpcProductsSchema,
    Message,
)
from ninja_jwt.authentication import JWTAuth

router = Router()

_PAGE_SIZE = getattr(settings, "PAGE_SIZE", 30)


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


# =============================top_keywords api=============================
@router.get(
    "top_keywords/products/{int:shopid}",
    response=List[Any],
    tags=["campagns_reports"],
    auth=JWTAuth(),
)
def get_products_from_top_keywords(request, shopid: int, month: str = ""):
    """
    获取指定 shopid 的 top_keywords 表中有数据的月份
    只有 date_type=1 的才需要月份
    :param request:
    :param shopid: 店铺ID
    """
    #     select distinct itemmngid, itemid from top_keywords_datas where shopid='421947' and term_start_date ='2024-10-01' order by itemmngid
    query = Q(shopid=shopid)
    if month:
        query &= Q(term_start_date=f"{month}-01")
    qs = (
        TopKeywords.objects.filter(query)
        .distinct("itemmngid", "itemid")
        .order_by("itemmngid")
        .values("itemmngid", "itemid")
    )
    return qs


@router.get(
    "top_keywords/months/{int:shopid}",
    response=List[CampaignsMonthSchema],
    tags=["campagns_reports"],
    auth=JWTAuth(),
)
def get_months_from_top_keywords(request, shopid: int):
    """
    获取指定 shopid 的 top_keywords 表中有数据的月份
    只有 date_type=1 的才需要月份
    :param request:
    :param shopid: 店铺ID
    """
    query = Q(shopid=shopid)
    # query &= Q(date_type=1)
    qs = (
        TopKeywords.objects.filter(query)
        .distinct("term_start_date")
        .order_by("-term_start_date")
        .values("term_start_date")
    )
    # print(qs.query)
    return [
        CampaignsMonthSchema(
            formatted_date=item["term_start_date"].strftime("%Y-%m"),
        )
        for item in qs
    ]


@router.get(
    "/top_keywords",
    response=List[Any],
    tags=["top_five_keywords"],
    auth=JWTAuth(),
)
@paginate(PageNumberPagination, page_size=_PAGE_SIZE)
def get_top_keywords_by_shopid(
    request,
    shopid: int,
    month: str = "",
    rank: str = "",
    itemmngid: str = "",
    q: str = "",
):
    """
    获取指定shopid的CPC关键词排行榜
    """
    # print(shopid, dtype, q)
    query = Q(shopid=shopid)
    if month and month != "all" and month != "null":
        query &= Q(term_start_date=f"{month}-01")
    if itemmngid and itemmngid != "all" and itemmngid != "null":
        query &= Q(itemmngid=itemmngid)
    if rank and rank != "all" and rank != "null":
        query &= Q(search_word_rank=rank)

    if q:
        query &= Q(search_word__icontains=q) | Q(itemmngid__icontains=q)

    qs = (
        TopKeywords.objects.filter(query)
        .values("search_word")
        .annotate(show_count=Count("search_word"))
        .order_by("-show_count")[:20]
    )
    # print("=============top keyword:\n", qs.query)
    return qs
