import csv
from datetime import date, datetime
from decimal import Decimal
from io import StringIO
from typing import Any, List
from django.http import HttpResponse
from ninja import Router, File, UploadedFile
from ninja_jwt.authentication import JWTAuth
from django.db import connection
from dateutil.relativedelta import relativedelta

from django.db.models import Q, Sum, F
from ninja.pagination import paginate, PageNumberPagination
from django.conf import settings
from openpyxl import Workbook

from sales_data.schemas import ShopFixedFeesSchema
from shares.models import (
    GracefulShops,
    OrderDetailsCalc,
    ShopDailySalesTagets,
    ShopFixedFees,
)
from shares.schemas import ShopDailySalesTagetsSchema
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


# 获取所有店铺指定日期的销售数据
@router.get(
    "/shop_sales",
    response=List[Any],
    tags=["sale_datas"],
)
def get_shop_sales_data_list(request, delivery_date: str):

    sql_query = """
                SELECT 
                    gs.shopname
                    ,gs.shop_code
                    ,sds.subtotal_price - sds.coupon AS amount_price
                    ,sds.order_count 
                FROM 
                    graceful_shops gs
                LEFT JOIN
                    sales_daily_summary sds on gs.shop_code = sds.shop_code and sds.delivery_date = %s
                ORDER BY 
                    gs.shop_code;
            """
    # 执行查询
    with connection.cursor() as cursor:
        cursor.execute(sql_query, [delivery_date])
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
        # print(columns)
        results = [dict(zip(columns, row)) for row in rows]
    return results


# 获取指定日期内的指定店铺的会计数据
@router.get(
    "/shop_accounting_detaldatas",
    response=List[Any],
    tags=["sale_datas"],
)
def get_shop_saledatas(
    request, start: str, end: str, shop_code: str, dtype: str = "day"
):
    if dtype == "day":
        sql_query = """      
            SELECT 
                gs.shop_code,
                gs.shopname,
                os.delivery_date,
                SUM(odc.amount_price - odc.coupon) AS amount_price,
                COUNT(DISTINCT os.order_number) AS order_count,
                SUM(odc.tax_price) AS tax_price,
                SUM(odc.coupon) AS coupon,
                SUM(odc.rewards) AS rewards
            FROM 
                graceful_shops gs 
            LEFT JOIN 
                orders os 
            ON 
                gs.shop_code = os.shop_code  
                AND os.cancel_flag <> 2   
                AND os.detail_downloaded = TRUE
                AND os.delivery_date BETWEEN %s AND %s 
            LEFT JOIN 
                order_details_calc odc 
            ON 
                odc.order_number = os.order_number
            WHERE 
                os.shop_code = %s
            GROUP BY 
                gs.shop_code, 
                gs.shopname, 
                os.delivery_date
            ORDER BY 
                os.delivery_date DESC;

        """
    else:
        sql_query = """
                SELECT 
                    gs.shop_code,
                    gs.shopname, 
                    odc.order_month AS delivery_date,
                    SUM(odc.amount_price - odc.coupon) AS amount_price,
                    COUNT(DISTINCT os.order_number) AS order_count,
                    SUM(odc.tax_price) AS tax_price,
                    SUM(odc.coupon) AS coupon,
                    SUM(odc.rewards) AS rewards
                FROM 
                    graceful_shops gs 
                LEFT JOIN 
                    orders os 
                ON 
                    gs.shop_code = os.shop_code
                    AND os.cancel_flag <> 2   
                    AND os.detail_downloaded = TRUE
                LEFT JOIN 
                    order_details_calc odc 
                ON 
                    odc.order_number = os.order_number
                WHERE 
                    odc.order_month BETWEEN %s AND %s  
                    AND os.shop_code = %s 
                GROUP BY 
                    gs.shop_code, 
                    gs.shopname, 
                    odc.order_month
                ORDER BY 
                    delivery_date DESC;

            """

    # 执行查询
    with connection.cursor() as cursor:
        cursor.execute(
            sql_query,
            [
                start,
                end,
                shop_code,
            ],
        )
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
        # print(columns)
        results = [dict(zip(columns, row)) for row in rows]
    return results


# 获取指定店铺的指定月份的商品页面的销售数据
@router.get(
    "/month_sales",
    response=List[Any],
    tags=["sale_datas"],
)
def get_month_sales_data(request, shopcode: str = "01", month: str = ""):
    """
    获取指定店铺的指定月份的商品页面的销售数据
    :param request:
    :param shopcode: 店铺code
    :param month: 月份
    """

    resutls, _ = _get_month_sales_data(shopcode, month)
    return resutls


@router.get(
    "/month_sales_data/export",
    tags=["sale_datas"],
)
def export_month_sales_data(request, shopcode: str = "01", month: str = ""):

    shop = GracefulShops.objects.filter(shop_code=shopcode).first()
    if not shop:
        return HttpResponse("店铺不存在", status=404)

    results, column_names = _get_month_sales_data(shopcode, month)

    wb = Workbook()
    ws = wb.active
    ws.title = f"{shop.shopname}({month[:7]})"

    # 映射表头
    headers = [FIELD_TO_HEADER[col] for col in column_names if col in FIELD_TO_HEADER]

    ws.append(headers)

    # 写入查询结果
    for row in results:
        filtered_row = [
            format_value(row[field])
            for field in column_names
            if field in FIELD_TO_HEADER
        ]
        ws.append(filtered_row)

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = f'attachment; filename="customs_{month}.xlsx"'

    wb.save(response)

    return response


def format_value(value):
    """格式化值为字符串以兼容 Excel"""
    if isinstance(value, Decimal):
        return float(value)
    if isinstance(value, date):
        return value.strftime("%Y-%m-%d")
    return value


def _get_month_sales_data(shopcode: str, month: str):
    sql_query = """
                -- Step 1: 基础数据过滤
                WITH base_data AS (
                    SELECT 
                        shopid,
                        shop_code,
                        effect_month,
                        item_code,
                        manage_code,
                        amount_price,
                        ABS(coupon) AS abs_coupon, -- 优惠券金额取绝对值
                        tax_price,
                        order_count,
                        jan_count,
                        total720hcv,
                        total720hgms,
                        afl_order_count,
                        afl_rewards,
                        ca_sales_count,
                        ca_actual_amount,
                        total_orginal_price,
                        shipping_fee,
                        pointsawarded,
                        advertisingfees,
                        deal_sales_value,
                        rmail_chargefee
                    FROM sales_page_months_summary
                    WHERE shop_code = %s AND effect_month = %s
                ),
                -- Step 2: 计算派生数据
                calculated_data AS (
                    SELECT 
                        shopid,
                        shop_code,
                        effect_month,
                        item_code,
                        manage_code,
                        ROUND((amount_price - abs_coupon), 0) AS ad_amount, -- 扣除优惠券后的销售额（含税）
                        ROUND((amount_price - abs_coupon - tax_price), 0) AS adut_amount, -- 扣除优惠券和税后的销售额
                        abs_coupon AS coupon, -- 优惠券金额
                        order_count, -- 订单数
                        jan_count, -- 销售件数
                        total720hcv AS rpp_count, -- RPP 件数
                        ROUND(total720hgms * 1.1, 0) AS rpp_amount, -- RPP 商品金额（含税）
                        ROUND(CASE WHEN order_count = 0 THEN 0 ELSE (total720hcv * 100.0 / order_count) END, 2) AS rpp_percentage, -- RPP 占比 
                        afl_order_count, -- Affiliate 订单数
                        ROUND(CASE WHEN order_count = 0 THEN 0 ELSE (afl_order_count * 100.0 / order_count) END, 2) AS afl_percentage, -- Affiliate 占比
                        ca_sales_count, -- CA 订单数
                        ROUND(CASE WHEN order_count = 0 THEN 0 ELSE (ca_sales_count * 100.0 / order_count) END, 2) AS ca_percentage, -- CA 占比 
                        ROUND(ca_actual_amount * 1.1, 0) AS ca_amount, -- CA 商品金额（含税）
                        ROUND(afl_rewards * 1.1, 0) AS afl_rewards, -- Affiliate 报酬（含税）
                        ROUND(afl_rewards * 0.3 * 1.1, 0) AS afl_commission, -- Affiliate 手续费（含税）
                        (order_count - total720hcv - afl_order_count - ca_sales_count) AS other_count, -- 其他订单数
                        ROUND(CASE WHEN order_count = 0 THEN 0 ELSE ((order_count - total720hcv - afl_order_count - ca_sales_count) * 100.0 / order_count) END, 2) AS other_percentage, -- 其他订单占比
                        total_orginal_price, -- 原价之和
                        ROUND(shipping_fee, 0) AS shipping_fee, -- 物流费用之和
                        ROUND((amount_price - abs_coupon) * 0.07 * 1.1, 0) AS commission, -- 平台佣金
                        pointsawarded, -- 平台奖励积分
                        advertisingfees, -- 广告支出
                        deal_sales_value, -- DEAL 广告支出
                        rmail_chargefee, -- 邮件广告支出
                        amount_price - abs_coupon - tax_price - total_orginal_price - shipping_fee 
                        - ((amount_price - abs_coupon) * 0.07 * 1.1) 
                        - (total720hgms * 1.1) - (ca_actual_amount * 1.1) 
                        - afl_rewards * 1.1 - afl_rewards * 0.3 * 1.1 AS benefit -- 利润计算
                    FROM base_data
                ),
                -- Step 3: 汇总数据
                summary_data AS (
                    SELECT 
                        bd.shop_code,
                        bd.effect_month,
                        SUM(amount_price - abs_coupon - tax_price) AS total_amount, -- 总销售额（扣除优惠券和税）
                        pointsawarded, -- 平台奖励积分总和
                        discount_rate -- 折扣率
                    FROM base_data bd
                    LEFT JOIN rpp_discount_infos rdi 
                        ON rdi.shopid = bd.shopid AND rdi.effect_month = bd.effect_month
                    GROUP BY bd.shop_code, bd.effect_month, pointsawarded, discount_rate
                ),
                -- Step 4: 总利润计算
                total_datas AS (
                    SELECT  
                        A.shop_code,
                        A.effect_month,  
                        SUM(A.benefit - (
                            (A.adut_amount * 1.1 / B.total_amount) 
                            * (B.pointsawarded + A.advertisingfees + A.deal_sales_value + A.rmail_chargefee)
                        )) AS total_benefit
                    FROM calculated_data AS A
                    LEFT JOIN summary_data AS B
                        ON A.shop_code = B.shop_code AND A.effect_month = B.effect_month 
                    GROUP BY A.shop_code, A.effect_month
                ),

                -- 提前计算净收益以减少重复计算
                benefit_data AS (
                    SELECT 
                        A.*,
                        ROUND(
                            CASE 
                                WHEN B.total_amount = 0 THEN 0
                                ELSE A.benefit - ((A.adut_amount * 1.1 / B.total_amount) * 
                                (B.pointsawarded + A.advertisingfees + A.deal_sales_value + A.rmail_chargefee))
                            END, 
                        0) AS net_benefit
                    FROM calculated_data AS A
                    LEFT JOIN summary_data AS B
                        ON A.shop_code = B.shop_code AND A.effect_month = B.effect_month
                )
                -- Step 5: 最终查询
                SELECT 
                    bd.shopid,
                    bd.shop_code,
                    bd.effect_month,
                    bd.item_code,
                    bd.manage_code,
                    bd.ad_amount,
                    bd.adut_amount,
                    bd.coupon,
                    bd.order_count,
                    bd.jan_count,
                    bd.rpp_count,
                    bd.rpp_amount,
                    bd.rpp_percentage,
                    bd.afl_order_count,
                    bd.afl_percentage,
                    bd.ca_sales_count,
                    bd.ca_percentage,
                    bd.ca_amount,
                    bd.afl_rewards,
                    bd.afl_commission,
                    bd.other_count,
                    bd.other_percentage,
                    bd.total_orginal_price,
                    bd.shipping_fee,
                    bd.commission,
                    ROUND(C.total_benefit, 0) AS total_benefit,
                    bd.net_benefit, -- 当前商品净收益
                    ROUND(
                        CASE 
                            WHEN bd.adut_amount = 0 THEN 0
                            ELSE (bd.net_benefit * 100.0 / bd.adut_amount)
                        END, 
                    2) AS benefit_percentage, -- 利益率
                    ROUND(
                        CASE 
                            WHEN C.total_benefit = 0 THEN 0
                            ELSE (bd.net_benefit * 100.0 / C.total_benefit)
                        END, 
                    2) AS total_benefit_percentage, -- 总利益占比
                    ROUND(
                        CASE 
                            WHEN bd.jan_count = 0 THEN 0
                            ELSE (bd.net_benefit / bd.jan_count)
                        END, 
                    0) AS avg_benefit -- 每件商品平均收益
                FROM benefit_data AS bd
                LEFT JOIN total_datas AS C
                    ON bd.shop_code = C.shop_code AND bd.effect_month = C.effect_month
                ORDER BY total_benefit_percentage DESC;

                """

    # 执行查询
    with connection.cursor() as cursor:

        cursor.execute(sql_query, [shopcode, month])
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
        results = [dict(zip(columns, row)) for row in rows]

        return results, columns

    return [], None


# 字段与表头映射关系
FIELD_TO_HEADER = {
    "manage_code": "页面管理番号",
    "item_code": "商品番号",
    "ad_amount": "売上値引後(税込)",
    "adut_amount": "売上値引後(税抜)",
    "coupon": "クーポン",
    "jan_count": "販売SKU数",
    "order_count": "販売订单数",
    "rpp_count": "RPP件数",
    "rpp_percentage": "RPP割合",
    "afl_order_count": "AF件数",
    "afl_percentage": "AF割合",
    "ca_sales_count": "CA件数",
    "ca_percentage": "CA割合",
    "other_count": "その他件数",
    "other_percentage": "その他割合",
    "total_orginal_price": "原価",
    "shipping_fee": "送料(税込)",
    "commission": "手数料(マージン+決済)",
    "pointsawarded": "ポイント",
    "rpp_amount": "RPP商品別(税込)",
    "ca_amount": "CA商品別(税込)",
    "afl_rewards": "アフィリエイト報酬(税込)",
    "advertisingfees": "CPA",
    "deal_sales_value": "DEAL",
    "rmail_chargefee": "おス(店舗)",
    "rrp_discount": "RPP値引き",
    "benefit": "商品利益",
    "benefit_percentage": "商品利益率",
    "total_benefit_percentage": "商品利益割合率",
    "avg_benefit": "平均利益",
}


# ================================== shop_daily_sales_tagets ============================================


# 获取指定店铺的指定月份的销售目标
@router.get(
    "/dailysalestagets",
    response=List[Any],
    tags=["sale_datas"],
)
def get_shop_daily_sales_tagets(request, shopcode: str, month: str):

    start_date = datetime.strptime(month, "%Y-%m-01").date()
    end_date = start_date + relativedelta(months=1) - relativedelta(days=1)

    query = (
        Q(shop_code=shopcode)
        & Q(effect_date__gte=start_date)
        & Q(effect_date__lte=end_date)
    )

    qs = (
        ShopDailySalesTagets.objects.filter(query)
        .values("id", "taget_amount", "effect_date", "shop_code", "is_done")
        .order_by("effect_date")
    )

    return qs


@router.post(
    "/dailysalestagets/upload/{str:shopcode}/{str:month}",
    response={200: Any, 422: Any},
    tags=["datas_management"],
)
def upload_daily_sales_tagets(
    request,
    shopcode: str,
    month: str,
    file: UploadedFile = File(...),
):
    """
    上传 报关信息 文件
    """
    try:

        shop = GracefulShops.objects.filter(shop_code=shopcode).first()
        if not shop:
            return 422, {"message": "店铺不存在"}

        # 读取并解码文件内容
        file_content = file.read().decode("utf-8")
        csv_reader = csv.DictReader(StringIO(file_content))

        _FIELDNAME_MAPPING = {"日にち": "effect_date", "目標(税別)": "taget_amount"}

        # 替换字段名
        csv_reader.fieldnames = [
            _FIELDNAME_MAPPING.get(field, field) for field in csv_reader.fieldnames
        ]

        # 检查文件是否包含必要字段
        required_fields = {"effect_date", "taget_amount"}
        if not required_fields.issubset(csv_reader.fieldnames):
            missing_fields = required_fields - set(csv_reader.fieldnames or [])
            return 422, {"message": f"缺少必要字段: {', '.join(missing_fields)}"}

        # 解析并处理数据
        user = request.user
        targets = []
        is_check = False
        for row in csv_reader:
            # 去除空行
            if not any(row.values()):
                continue

            effect_date = row["effect_date"].replace("/", "-")
            taget_amount = row["taget_amount"].replace(",", "")

            if not is_check:
                target = ShopDailySalesTagets.objects.filter(
                    effect_date=effect_date,
                    shop_code=shopcode,
                ).first()

                if target:
                    return 422, {"message": "已存在相同日期的销售目标"}

                is_check = True

            if user:
                targets.append(
                    ShopDailySalesTagets(
                        shopid=shop.shopid,
                        shop_name=shop.shopname,
                        shop_code=shopcode,
                        effect_date=effect_date,
                        taget_amount=taget_amount,
                        is_done=False,
                        updated_by=user,
                    )
                )
            else:
                targets.append(
                    ShopDailySalesTagets(
                        shopid=shop.shopid,
                        shop_name=shop.shopname,
                        shop_code=shopcode,
                        effect_date=effect_date,
                        taget_amount=taget_amount,
                        is_done=False,
                    )
                )

        # ShopDailySalesTagets.objects.bulk_create(targets)
        ShopDailySalesTagets.objects.bulk_update(targets)

        return 200, {"message": f"上传成功！！！"}

    except UnicodeDecodeError:
        return 422, {"message": "文件解码失败，请确保文件是 UTF-8 编码"}
    except Exception as e:
        return 422, {"message": f"处理文件时发生错误: {str(e)}"}


@router.post(
    "/dailysalestagets/upsert",
    response={200: ShopDailySalesTagetsSchema, 422: Any},
    tags=["sale_datas"],
)
def upsert_shop_daily_sales_tagets(request, data: ShopDailySalesTagetsSchema):

    target = data.dict()

    user = request.user
    if user:
        target["updated_by"] = user

    new_target, _ = ShopDailySalesTagets.objects.update_or_create(
        id=data.id, defaults=target
    )

    return new_target


# ================================== shop_daily_sales_summary ============================================


# 获取指定店铺的指定日期范围内的销售数据
@router.get(
    "/shop/dailysales/summary",
    response=List[Any],
    tags=["sale_datas"],
)
def get_shop_daily_sales_summary(request, shopcode: str, start: str, end: str):
    sql_query = """
            SELECT 
                sds.shop_code,
                sds.delivery_date,  -- 日にち 
                EXTRACT(ISODOW FROM sds.delivery_date) AS weekday_number,  -- 星期数 1（Monday）到 7（Sunday）
                sds.order_count,  -- 订单数
                sdst.taget_amount,  -- 目標(税別) 不含税
                sds.subtotal_price - sds.coupon - sds.tax_price AS amount_untax,  -- 売上(税別) 不含税
                sds.subtotal_price - sds.coupon - sds.tax_price - sdst.taget_amount AS target_diff,  -- 目標差分
                sds.subtotal_price - sds.coupon AS amount_tax,  -- 売上(税込)(含锐)
                sds.coupon,  -- クーポン額
                ROUND(sds.coupon * 100.0 / sds.subtotal_price, 2) AS soupon_rate,  -- クーポン率
                sds.alf_amount,  -- アフィ売上
                sds.afl_rewards,  -- アフィ売上
                ROUND(sds.alf_amount * 100.0 / NULLIF((sds.subtotal_price - sds.coupon), 0), 2) AS afl_rewards_rate,  -- アフィ売上 比率
                sds.rpp_amount,  -- RPP
                ROUND(sds.rpp_amount * 100.0 / NULLIF((sds.subtotal_price - sds.coupon), 0), 2) AS rpp_rate,  -- RPP 比率
                sds.ca_amount,  -- CA
                sds.arrt_gms,  -- おス(店舗)
                sds.cpa_sales,  -- CPA
                sds.gmscd,  -- 純広
                sds.rsis_order_count,  -- 件数
                sds.rsis_sales_repeater_purchaser,  -- リピーター
                sds.rsis_sales_visit,  -- アクセス
                sds.rpp_totalclick,  -- RPP
                sds.ca_coupon,  -- CA
                sds.arrt_clickcount,  -- おス(店舗)
                sds.aprd_click,  -- 純広 クリック数
                sds.rsis_sales_cvr,  -- 転換率(売上指標)
                sds.rsis_sales_aov,  -- 客単価
                ROUND(sds.rpp_totaladcost * (100.0 - COALESCE(rdis.discount_rate, 0)) / 100.0, 0) AS rpp_totaladcost,  -- RPP(税抜) [実績額(合計)]
                sds.ca_adfee,  -- CA(税抜)
                sds.arrt_chargefee,  -- おス(店舗)(税抜)
                sds.aprd_dailyadsales,  -- 純広(税抜)
                sds.cpa_fees,  -- CPA(税抜)
                sds.rsis_deal_sales_value,  -- DEAL(税抜)
                sds.original_price,  -- 原価(税抜)
                sds.pointsawarded,  -- ポイント
                sds.shipping_cost,  -- 送料
                sds.envelope_cost,  -- 資材費
                ROUND(COALESCE(sds.coupon_count - sds.ca_usecount, 0) * 50, 0) AS rpp_coupon_fee,  -- クーポン発行手数料
                COALESCE(rdis.discount_rate, 0) AS discount_rate,  -- rpp 折扣率
                sds.ad_total_amount,  -- 广告销售总额
                sds.ad_total_visit,  -- 广告总访问量
                sds.ad_total_fees,  -- 广告销售总费用(不含税)
                sds.commision_total_fees,  -- 佣金总费用(不含税)
                sds.marginal_profit,  -- 利润
                ROUND(
                    CAST(COALESCE(sff.fee_amount, 0) / 
                        NULLIF(DATE_PART('days', DATE_TRUNC('month', sds.delivery_date) + INTERVAL '1 month' - INTERVAL '1 day'), 0) 
                    AS numeric), 
                    0
                ) AS fixed_fees  -- 固定费用 (按月平摊)
            FROM 
                sales_daily_summary sds
            LEFT JOIN 
                shop_daily_sales_tagets sdst ON sds.shop_code = sdst.shop_code AND sdst.effect_date = sds.delivery_date
            LEFT JOIN 
                rpp_discount_infos rdis ON rdis.shop_code = sds.shop_code AND sds.delivery_date >= rdis.effect_month AND sds.delivery_date < rdis.effect_month + INTERVAL '1 month'
            LEFT JOIN (
                -- 店铺 固定费用
                SELECT shop_code, effect_month, SUM(fee_amount) AS fee_amount
                FROM shop_fixed_fees
                GROUP BY shop_code, effect_month
            ) AS sff ON sff.shop_code = sds.shop_code AND TO_CHAR(sds.delivery_date, 'YYYY-MM') = TO_CHAR(sff.effect_month, 'YYYY-MM')
            WHERE 
                sds.shop_code = %s
                AND sds.delivery_date BETWEEN %s AND %s
            ORDER BY 
                sds.delivery_date DESC;
        """

    # 执行查询
    with connection.cursor() as cursor:

        cursor.execute(sql_query, [shopcode, start, end])
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
        results = [dict(zip(columns, row)) for row in rows]

        return results

    return []


# ================================== shop_fixed_fees ============================================


# 获取指定店铺的指定月份的固定费
@router.get(
    "/fixedfees",
    response=List[Any],
    tags=["sale_datas"],
)
def get_shop_fixed_fees(request, shopcode: str, month: str):

    query = Q(shop_code=shopcode) & Q(effect_month=month)

    qs = (
        ShopFixedFees.objects.filter(query)
        .values(
            "id", "shop_code", "shop_name", "effect_month", "fee_name", "fee_amount"
        )
        .order_by("effect_month")
    )

    return qs


# 新增或更新 固定费
@router.post(
    "/fixedfees/upsert",
    response={200: ShopFixedFeesSchema, 422: Any},
    tags=["sale_datas"],
)
def upsert_shop_fixed_fees(request, data: ShopFixedFeesSchema):
    info = data.dict()

    user = request.user
    if user:
        info["updated_by"] = user

    new_info, _ = ShopFixedFees.objects.update_or_create(id=data.id, defaults=info)

    return new_info


# 删除 固定费
@router.delete(
    "/fixedfees",
    response=Any,
    tags=["sale_datas"],
)
def delete_shop_fixed_fees(request, id: int):
    ShopFixedFees.objects.filter(id=id).delete()

    return {"message": "删除成功"}
