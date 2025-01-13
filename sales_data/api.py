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

from shares.models import GracefulShops, OrderDetailsCalc, ShopDailySalesTagets
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
                select gs.shopname, 
                gs.shop_code,
                sum(os.subtotal_price) as amount_price, 
                count(os.order_number) as order_count
                from
                graceful_shops gs 
                left join  orders  os  
                    on gs.shop_code = os.shop_code and os.phase_name = '完了' and os.cancel_flag = 0 and  os.delivery_date = %s
                group by gs.shopname, gs.shop_code
                order by gs.shop_code
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
            select gs.shop_code,
            gs.shopname,
            os.delivery_date,
            sum(odc.amount_price) as amount_price,
            count(distinct os.order_number) as order_count,
            sum(odc.tax_price) as tax_price,
            sum(odc.coupon) as coupon,
            sum(odc.rewards) as rewards
            from 
            graceful_shops gs 
            left join orders os on gs.shop_code = os.shop_code  and os.delivery_date between %s and %s 
            and os.phase_name = '完了' and os.cancel_flag = 0   and detail_downloaded=true
            left join order_details_calc odc on odc.order_number = os.order_number
            where  os.shop_code = %s
            group by gs.shop_code,gs.shopname,os.delivery_date
            order by os.delivery_date desc
        """
    else:
        sql_query = """
                select gs.shop_code,
                gs.shopname, 
                odc.order_month as delivery_date,
                sum(odc.amount_price) as amount_price,
                count(distinct os.order_number) as order_count,
                sum(odc.tax_price) as tax_price,
                sum(odc.coupon) as coupon,
                sum(odc.rewards) as rewards
                from 
                graceful_shops gs 
                left join orders os on gs.shop_code = os.shop_code
                and os.phase_name = '完了' and os.cancel_flag = 0   and detail_downloaded = true
                left join order_details_calc odc on odc.order_number = os.order_number
                where  odc.order_month between  %s and %s  and  os.shop_code = %s  
                group by gs.shop_code,gs.shopname ,odc.order_month
                order by delivery_date desc
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
                    abs(coupon) AS abs_coupon, -- 绝对值的优惠券金额
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
                FROM public.sales_page_months_summary
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
                    ROUND((total720hcv * 100.0 / order_count), 2) AS rpp_percentage, -- RPP 占比
                    afl_order_count, -- Affiliate 订单数
                    ROUND((afl_order_count * 100.0 / order_count), 2) AS afl_percentage, -- Affiliate 占比
                    ca_sales_count, -- CA 订单数
                    ROUND((ca_sales_count * 100.0 / order_count), 2) AS ca_percentage, -- CA 占比
                    ROUND(ca_actual_amount * 1.1, 0) AS ca_amount, -- CA 商品金额（含税）
                    ROUND(afl_rewards * 1.1, 0) AS afl_rewards, -- Affiliate 报酬（含税）
                    ROUND(afl_rewards * 0.3 * 1.1, 0) AS afl_commission, -- Affiliate 手续费（含税）
                    (order_count - total720hcv - afl_order_count - ca_sales_count) AS other_count, -- 其他订单数
                    ROUND(((order_count - total720hcv - afl_order_count - ca_sales_count) * 100.0 / order_count), 2) AS other_percentage, -- 其他订单占比
                    total_orginal_price, -- 原价之和
                    ROUND(shipping_fee, 0) AS shipping_fee, -- 物流费用之和
                    ROUND((amount_price - abs_coupon) * 0.07 * 1.1, 0) AS commission, -- 平台佣金
                    pointsawarded, -- 平台奖励积分
                    advertisingfees, -- 广告支出
                    deal_sales_value, -- DEAL 广告支出
                    rmail_chargefee, -- 邮件广告支出
                    -- 利润计算（扣除所有支出后）
                    amount_price - abs_coupon - tax_price - total_orginal_price - shipping_fee 
                    - ((amount_price - abs_coupon) * 0.07 * 1.1) 
                    - (total720hgms * 1.1) - (ca_actual_amount * 1.1) 
                    - afl_rewards * 1.1 - afl_rewards * 0.3 * 1.1 AS benefit
                FROM base_data
            ),

            -- Step 3: 汇总数据
            summary_data AS (
                SELECT 
                    shop_code,
                    bd.effect_month,
                    SUM(amount_price - abs_coupon - tax_price) AS total_amount, -- 总销售额（扣除优惠券和税）
                    pointsawarded, -- 平台奖励积分总和
                    discount_rate -- 折扣率
                FROM base_data bd
                LEFT JOIN rpp_discount_infos rdi 
                    ON rdi.shopid = bd.shopid AND rdi.effect_month = bd.effect_month
                GROUP BY shop_code, bd.effect_month, pointsawarded, discount_rate
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
            )

            -- Step 5: 最终查询
            SELECT 
                A.shopid, -- 店铺ID
                A.shop_code, -- 店铺代码
                A.effect_month, -- 生效月份
                A.item_code, -- 商品编号
                A.manage_code, -- 商品管理编号 (通常是商品URL或标识符)
                A.ad_amount, -- 税前销售额 (扣除优惠券后的含税金额)
                A.adut_amount, -- 税后销售额 (扣除优惠券后的不含税金额)
                A.coupon, -- 优惠券金额
                A.order_count, -- 销售订单总数
                A.jan_count, -- 销售商品总数 (以数量计算)
                A.rpp_count, -- RPP (按单品推广) 的订单数
                A.rpp_amount, -- RPP 总金额 (按单品推广的总金额，含税)
                A.rpp_percentage, -- RPP 占比 (RPP 订单数占总订单数的比例)
                A.afl_order_count, -- AF (Affiliate 联盟推广) 的订单数
                A.afl_percentage, -- AF 占比 (AF 订单数占总订单数的比例)
                A.ca_sales_count, -- CA (活动推广) 的订单数
                A.ca_percentage, -- CA 占比 (CA 订单数占总订单数的比例)
                A.ca_amount, -- CA 商品金额 (活动推广销售额，含税)
                A.afl_rewards, -- AF 联盟推广奖励 (含税)
                A.afl_commission, -- AF 联盟推广佣金 (含税)
                A.other_count, -- 其他来源的订单数 (非 RPP、AF 或 CA)
                A.other_percentage, -- 其他来源订单占比
                A.total_orginal_price, -- 商品原价 (总的原始价格)
                A.shipping_fee, -- 运输费用 (含税)
                A.commission, -- 平台手续费 (按销售额的 0.07 计算，并含税)
                -- A.pointsawarded, -- 发放的积分金额 (整个月份的总支出)（为整月的支出数据）
                -- A.advertisingfees, -- 广告费用 (CPA 数据，整月支出)（为整月的支出数据）
                -- A.deal_sales_value, -- DEAL 广告支出 (整月支出)（为整月的支出数据）
                -- A.rmail_chargefee, -- 邮件广告费用 (Rakuten 平台邮件推广的支出)（为整月的支出数据）

                -- 以下为按比例分摊到当前销售项的数据
                round((A.adut_amount * 1.1 / B.total_amount) * B.pointsawarded, 0) AS pointsawarded, -- 按比例分摊的积分支出
                round((A.adut_amount * 1.1 / B.total_amount) * A.advertisingfees, 0) AS advertisingfees, -- 按比例分摊的广告费用
                round((A.adut_amount * 1.1 / B.total_amount) * A.deal_sales_value, 0) AS deal_sales_value, -- 按比例分摊的 DEAL 广告费用
                round((A.adut_amount * 1.1 / B.total_amount) * A.rmail_chargefee, 0) AS rmail_chargefee, -- 按比例分摊的邮件广告费用
                round((A.rpp_amount * B.discount_rate) / 100.0, 0) AS rrp_discount, -- RPP 折扣金额 (根据折扣率计算)

                -- 以下为利益相关的字段计算
                round(C.total_benefit, 0) AS total_benefit, -- 总收益
                round(
                    benefit - ((A.adut_amount * 1.1 / B.total_amount) * (B.pointsawarded + A.advertisingfees + A.deal_sales_value + A.rmail_chargefee)), 
                    0
                ) AS benefit, -- 当前商品的最终收益 (扣除各种成本后的净收益)
                round(
                    (A.benefit - ((A.adut_amount * 1.1 / B.total_amount) * (B.pointsawarded + A.advertisingfees + A.deal_sales_value + A.rmail_chargefee))) * 100.0 / A.adut_amount, 
                    2
                ) AS benefit_percentage, -- 利益率 (净收益占销售额比例)
                round(
                    (benefit - ((A.adut_amount * 1.1 / B.total_amount) * (B.pointsawarded + A.advertisingfees + A.deal_sales_value + A.rmail_chargefee))) * 100.0 / C.total_benefit, 
                    2
                ) AS total_benefit_percentage, -- 总利益中的占比 (当前商品收益占总收益的比例)
                round(
                    (benefit - ((A.adut_amount * 1.1 / B.total_amount) * (B.pointsawarded + A.advertisingfees + A.deal_sales_value + A.rmail_chargefee))) / A.jan_count, 
                    0
                ) AS avg_benefit -- 每件商品的平均收益 (净收益除以销售件数)

            FROM calculated_data AS A
            LEFT JOIN summary_data AS B
                ON A.shop_code = B.shop_code AND A.effect_month = B.effect_month 
            LEFT JOIN total_datas AS C
                ON A.shop_code = C.shop_code AND A.effect_month = C.effect_month
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


# ================================== shop_daily_sales_tagets ============================================
