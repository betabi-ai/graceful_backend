from datetime import datetime
from typing import Any, List
from ninja import Router, File
from ninja_jwt.authentication import JWTAuth
from django.db import connection


from django.db.models import Q, Sum, F
from ninja.pagination import paginate, PageNumberPagination
from django.conf import settings

from shares.models import OrderDetailsCalc
from shares.time_utils import get_previous_months_first_day

router = Router(auth=JWTAuth())
_PAGE_SIZE = getattr(settings, "PAGE_SIZE", 30)


# 获取 jan code  的 在库数据情况
@router.get(
    "/jan_sales",
    response=List[Any],
    tags=["sale_datas"],
)
@paginate(PageNumberPagination, page_size=_PAGE_SIZE)
def get_jancode_sales_amount_infos(request, q: str = ""):

    now = datetime.now()
    months = get_previous_months_first_day(now, 3)

    # 构造查询条件
    where_clauses = []
    params = []

    if q:
        where_clauses.append("csku.jan_code = %s")
        params.append(q)

    # 构造完整 SQL 查询
    where_str = f"WHERE {' AND '.join(where_clauses)}" if where_clauses else ""

    sql_query = f"""
        SELECT 
            COALESCE(stock_data.jan_code, sales_data.jan_code) AS jan_code,
            COALESCE(stock_data.stock, 0) AS stock,
            COALESCE(sales_data.sale_count, 0) AS sale_count 
        FROM 
            (
                SELECT  
                    csku.jan_code, 
                    SUM(cstocks.stock) AS stock
                FROM 
                    crossmall_item_stocks cstocks 
                JOIN 
                    crossmall_item_sku csku
                    ON cstocks.item_cd = csku.item_code
                    AND cstocks.attribute1_name = csku.attribute1_name
                    AND cstocks.attribute2_name = csku.attribute2_name 
                    {where_str}
                GROUP BY 
                    csku.jan_code
            ) AS stock_data
        LEFT JOIN 
            (
                SELECT 
                    sjsai.jan_cd as jan_code,  
                    SUM(sjsai.amount) AS sale_count 
                FROM 
                    order_details_calc sjsai
                WHERE 
                    sjsai.order_month IN (%s, %s, %s)
                GROUP BY 
                    sjsai.jan_cd
            ) AS sales_data
        ON 
            stock_data.jan_code = sales_data.jan_code
        ORDER BY 
            jan_code DESC
    """

    # 添加日期参数
    params.extend(months)

    # 执行查询
    with connection.cursor() as cursor:
        cursor.execute(sql_query, params)
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        # print(columns)
        results = [dict(zip(columns, row)) for row in rows]
        for result in results:
            sale_count = result["sale_count"]
            stock = result["stock"]
            if stock <= 0:
                stock_days = 0
            else:
                if sale_count <= 0:
                    stock_days = stock
                else:
                    stock_days = stock / (sale_count / 90)
            result.update({"stock_days": stock_days})
    return results


# 获取指定jancode 的 按年，按月，按日的销售统计数据
@router.get(
    "/jan_sales/{str:jan_code}",
    response=List[Any],
    tags=["sale_datas"],
)
def get_jancode_sale_data_list(
    request,
    jan_code: str,
    start: str,
    end: str,
    dtype: str = "month",
):
    query = Q(jan_cd=jan_code)
    groupby = "order_month"
    match (dtype):
        case "month":
            if start and end:
                query &= Q(order_month__range=[start, end])
            groupby = "order_month"
        case "day":
            if start and end:
                query &= Q(order_day__range=[start, end])
            groupby = "order_day"
        case "year":
            groupby = "order_year"

    qs = (
        OrderDetailsCalc.objects.filter(query)
        .values("jan_cd")
        .annotate(
            date_str=F(groupby),
            sales_count=Sum("amount"),
            sales_amount=Sum("amount_price"),
        )
    ).order_by(groupby)

    # print(qs)

    return qs
