from datetime import date
from typing import Optional

from ninja import Schema


# 供 ProductsSchema 使用
class ProductCategoriesSimpleSchema(Schema):
    id: Optional[int] = None
    category_name: str


class ShopDailySalesTagetsSchema(Schema):
    id: Optional[int] = None
    taget_amount: float
    effect_date: date
    shop_code: str
