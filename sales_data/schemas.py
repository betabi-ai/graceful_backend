from datetime import date
from typing import Optional, List, Dict
from ninja import ModelSchema, Schema
from pydantic import field_validator


class SalesPageMonthsSummarySchema(Schema):
    """销售月汇总"""

    shopid: str
    shop_code: str
    effect_month: date
    item_code: str
    manage_code: str
    amount_price: Optional[float] = None
    jan_count: Optional[int] = None
    order_count: Optional[int] = None
    tax_price: Optional[float] = None
    coupon: Optional[float] = None
    shipping_fee: Optional[float] = None
    total_orginal_price: Optional[float] = None
    afl_rewards: Optional[float] = None
    afl_order_count: Optional[int] = None
    total720hgms: Optional[int] = None
    total720hcv: Optional[int] = None
    ca_actual_amount: Optional[int] = None
    ca_sales_count: Optional[int] = None
    advertisingfees: Optional[int] = None
    deal_sales_value: Optional[int] = None
    rmail_chargefee: Optional[int] = None
    pointsawarded: Optional[int] = None


# 店铺每月固定费
class ShopFixedFeesSchema(Schema):
    """店铺每月固定费"""

    id: Optional[int] = None
    shopid: str
    shop_code: str
    shop_name: str
    effect_month: date
    fee_name: str
    fee_amount: int
