from typing import List, Any
from django.conf import settings
from django.http import HttpResponse
from ninja import Router
from django.db.models import Count, Sum
from django.shortcuts import get_object_or_404
from django.db.models import Q, F, Window
from ninja.pagination import paginate, PageNumberPagination
from django.db.models.functions import RowNumber, TruncHour, TruncDay
import openpyxl


from shares.models import (
    CpcGoodKeywords,
    CpcGoodKeywordsRankLog,
    CpcKeywordsGoods,
    ShopCampagnsBudget,
    ShopCampagnsBudgetLog,
    TopKeywords,
)
from cpc.schemas import (
    CampaignsMonthSchema,
    CpcGoodKeywordsSchema,
    CpcKeywordEnableChangeINSchema,
    CpcProductsSchema,
    KeyValueTopKeywordsSchema,
    KeywordsRankLogSchema,
    Message,
    ShopCampagnsBudgetLogSchema,
    ShopCampagnsBudgetSEditchema,
    ShopCampagnsBudgetSchema,
)
from ninja_jwt.authentication import JWTAuth

router = Router()

_PAGE_SIZE = getattr(settings, "PAGE_SIZE", 30)

# ===========================cpc products==========================================


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
    # print(qs.query)
    return qs


# =====================================================================


# =============================cpc keywords========================================


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

    query = Q(shopid=shopid)
    query &= Q(is_deleted=False)
    if q:
        query &= Q(keyword__icontains=q) | Q(itemmngid__icontains=q)

    qs = CpcGoodKeywords.objects.filter(query).order_by(
        "-enabled_cpc", "itemmngid", "-cpc_rank_updatedat", "-natural_rank_updatedat"
    )
    # print(qs.query)
    return qs


@router.get(
    "/keywords/{int:shopid}/{str:itemmngid}",
    response=List[CpcGoodKeywordsSchema],
    tags=["cpc_keywords"],
    auth=JWTAuth(),
)
@paginate(PageNumberPagination, page_size=_PAGE_SIZE)
def get_cpc_keywords_by_itemmngid(request, shopid: int, itemmngid: str):
    """
    获取指定shopid下的指定itemmngid下的CPC关键词列表
    """
    query = Q(shopid=shopid)
    query &= Q(itemmngid=itemmngid)
    query &= Q(is_deleted=False)
    qs = CpcGoodKeywords.objects.filter(query).order_by(
        "-enabled_cpc", "keyword", "-cpc_rank_updatedat", "-natural_rank_updatedat"
    )
    return qs


@router.patch(
    "/keywords/checkenable",
    response={200: CpcGoodKeywordsSchema, 422: Message},
    tags=["cpc_keywords"],
    auth=JWTAuth(),
    # auth=None,
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
    # print(update_data)
    CpcGoodKeywords.objects.filter(id=item.id).update(**update_data)

    obj.refresh_from_db()
    return obj


@router.get(
    "/keywords/histories/{int:shopid}",
    response=List[KeywordsRankLogSchema],
    tags=["cpc_keywords"],
    auth=JWTAuth(),
    # auth=None,
)
# @paginate(PageNumberPagination, page_size=_PAGE_SIZE)
def get_keywords_rank_history_datas(
    request,
    shopid: int,
    itemid: str,
    kw: str,
    ranktype: str,
    start: str,
    end: str,
    dtype: str = "day",
):
    # print(".......")
    query = Q(shopid=shopid)
    query &= Q(itemid=itemid)
    query &= Q(keyword=kw)
    query &= Q(rank_type=ranktype)
    query &= Q(created_at__range=(start, end))

    qs = (
        CpcGoodKeywordsRankLog.objects.filter(query)
        .annotate(
            row_number=Window(
                expression=RowNumber(),
                partition_by=(
                    TruncHour("created_at")
                    if dtype == "hour"
                    else TruncDay("created_at")
                ),
                order_by=F("created_at").desc(),
            ),
        )
        .filter(row_number=1)
        .order_by("created_at")
    )

    # print(qs.query)
    # print(qs)

    return qs


# =====================================================================


# =============================top_keywords api=============================
@router.get(
    "top_keywords/products/{int:shopid}",
    response=List[Any],
    tags=["top_five_keywords"],
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
    if month and month != "all" and month != "null":
        # print("month:===========", month)
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
    tags=["top_five_keywords"],
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

    queryset = (
        TopKeywords.objects.filter(query)
        .values("search_word")
        .annotate(show_count=Count("search_word"))
        .order_by("-show_count")
    )

    # 判断数据是否超过10条
    if queryset.count() > 20:
        # 取出前9条数据
        top_19 = list(queryset[:19])

        # 计算第10条及之后的金额总和
        other_amount_sum = (
            queryset[19:].aggregate(total=Sum("show_count"))["total"] or 0
        )

        # 组合前19条数据和“其他”条目
        result = top_19 + [{"search_word": "其他", "show_count": other_amount_sum}]

        return result
    else:
        # 数据不足20条，直接返回所有数据
        return queryset


@router.get(
    "/top_keywords/list",
    response=List[KeyValueTopKeywordsSchema],
    tags=["top_five_keywords"],
    auth=None,
)
# @paginate(PageNumberPagination, page_size=_PAGE_SIZE)
def get_top_keywords_list(
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
    query = Q(shopid=shopid)
    if month and month != "all" and month != "null":
        query &= Q(term_start_date=f"{month}-01")
    if itemmngid and itemmngid != "all" and itemmngid != "null":
        query &= Q(itemmngid=itemmngid)
    if rank and rank != "all" and rank != "null":
        query &= Q(search_word_rank=rank)

    if q:
        query &= Q(search_word__icontains=q) | Q(itemmngid__icontains=q)

    queryset = (
        TopKeywords.objects.filter(query)
        .values("search_word")
        .annotate(show_count=Count("search_word"))
        .order_by("-show_count")
    )

    return queryset


@router.get(
    "/top_keywords/{int:shopid}/day",
    response=List[Any],
    tags=["top_five_keywords"],
    auth=JWTAuth(),
)
@paginate(PageNumberPagination, page_size=150)
def get_day_keywords_visit_datas(request, shopid: int, select_date: str, q: str = ""):
    query = Q(shopid=shopid)
    query &= Q(term_end_date=select_date)
    if q:
        query &= Q(search_word__icontains=q) | Q(itemmngid__icontains=q)
    """
    获取 指定日期下的 top_keywords 表中的数据
    """
    qs = (
        TopKeywords.objects.filter(query)
        .values(
            "search_word",
            "itemmngid",
            "item_rank",
            "item_visit",
            "item_visit_all",
            "item_order_count_all",
            "search_word_order_count",
            "item_cvr_all",
            "search_word_cvr",
            "search_word_rank",
            "search_word_ichiba_rank",
            "search_word_visit",
            "search_word_ichiba_visit",
        )
        .order_by("itemmngid", "-search_word_visit")
    )

    return qs


@router.get(
    "/top_keywords/export/{int:shopid}/day",
    tags=["top_five_keywords"],
    auth=JWTAuth(),
)
def export_day_keywords_visit_datas(
    request, shopid: int, select_date: str, q: str = ""
):
    query = Q(shopid=shopid)
    query &= Q(term_end_date=select_date)
    if q:
        query &= Q(search_word__icontains=q) | Q(itemmngid__icontains=q)
    """
    获取 指定日期下的 top_keywords 表中的数据
    """
    qs = TopKeywords.objects.filter(query).order_by("itemmngid", "-search_word_visit")
    # print(qs.query)

    # 创建一个新的工作簿
    workbook = openpyxl.Workbook()
    sheet = workbook.active

    # 写入表头
    sheet.append(
        [
            "商品番号",
            "日付",
            "关键词",
            "关键词转化率",
            "关键词访问量",
            "关键词乐天访问量",
            "关键词排行",
            "关键词乐天排行",
            "总转化率",
            "商品排行",
            "访问量",
            "总访问量",
            "总订单量",
            "关键词订单量",
        ]
    )

    for obj in qs:
        sheet.append(
            [
                obj.itemmngid,
                obj.term_end_date,
                obj.search_word,
                obj.search_word_cvr,
                obj.search_word_visit,
                obj.search_word_ichiba_visit,
                obj.search_word_rank,
                obj.search_word_ichiba_rank,
                obj.item_cvr_all,
                obj.item_rank,
                obj.item_visit,
                obj.item_visit_all,
                obj.item_order_count_all,
                obj.search_word_order_count,
            ]
        )

    workbook.active = sheet

    # 创建 HTTP 响应
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = 'attachment; filename="data.xlsx"'
    workbook.save(response)

    return response


# =====================================================================


# ============================ 店铺活动=============================


@router.get(
    "/shop_campaigns/{int:shopid}",
    response=List[ShopCampagnsBudgetSchema],
    tags=["shop_campaigns"],
    auth=JWTAuth(),
)
def get_shop_campaigns(request, shopid: int):
    """
    获取指定shopid的活动预算信息
    :param request:
    :param shopid: 店铺ID
    """
    query = Q(shopid=shopid)

    qs = ShopCampagnsBudget.objects.filter(query)
    # print(qs.query)
    return qs


@router.patch(
    "/shop_campaigns/edit",
    response={200: ShopCampagnsBudgetSchema, 422: Message},
    tags=["shop_campaigns"],
    auth=JWTAuth(),
    # auth=None,
)
def update_campaign_info(request, item: ShopCampagnsBudgetSEditchema):
    """
    更新：店铺活动预算信息
    """
    # print("....................", item.id, item.enabled_cpc)
    obj = get_object_or_404(
        ShopCampagnsBudget, campaignid=item.campaignid, shopid=item.shopid
    )

    update_data = {k: v for k, v in item.dict().items() if v is not None}
    # print(update_data)
    ShopCampagnsBudget.objects.filter(campaignid=item.campaignid).update(**update_data)

    obj.refresh_from_db()
    return obj


@router.get(
    "/shop_campaigns/logs/{int:shopid}",
    # response=List[ShopCampagnsBudgetLogSchema],
    response=List[ShopCampagnsBudgetLogSchema],
    tags=["shop_campaigns"],
    auth=JWTAuth(),
    # auth=None,
)
def get_each_hour_campaign_infos(request, shopid: int, start: str, end: str):

    q = Q(shopid=shopid)
    if start and end:
        q &= Q(created_at__range=(start, end))

    qs = (
        ShopCampagnsBudgetLog.objects.filter(q)
        .annotate(
            hour=TruncHour("created_at"),
            row_number=Window(
                expression=RowNumber(),
                partition_by=F("hour"),
                order_by=F("created_at").desc(),
            ),
        )
        .filter(row_number=1)
        .order_by("created_at")
    )

    return qs


# =====================================================================
