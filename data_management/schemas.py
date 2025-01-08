from datetime import date
from typing import Optional, List
from ninja import ModelSchema, Schema
from pydantic import field_validator


# Create your models here.
class ProductsSuppliersSchema(Schema):
    id: Optional[int] = None
    supplier_name: str
    contact: Optional[str] = None
    contact_details: Optional[str] = None


class ProductsUpsertSchema(Schema):
    id: Optional[int] = None
    itemid: str
    jan_code: Optional[str] = None
    product_name: Optional[str] = None
    product_price: Optional[float] = None
    bare_code: Optional[str] = None
    item_count: int = 1
    compatible_models: Optional[str] = None
    attribute: Optional[str] = None
    status: int = -1
    weight: Optional[float] = 0.0  # 修改为 float 类型
    adapter_desc: Optional[str] = None
    box_properties_desc: Optional[str] = None
    notices_desc: Optional[str] = None
    packaging_desc: Optional[str] = None
    alcohol_pack_desc: Optional[str] = None
    supplier_id: int = -1
    min_order_quantity: Optional[int] = 0
    stock_quantity: Optional[int] = None  # 添加 stock_quantity 字段

    # 使用 Pydantic V2 的 field_validator 处理空字符串
    @field_validator("weight", mode="before")
    def convert_empty_string_to_none(cls, value):
        if value == "":
            return 0.0  # 或者返回 0.0
        return value


class GtinCodeSchema(Schema):
    gs_prefix: str
    gs_jancode: str
    gs_index: int
    product_jancode: Optional[str]


class CreateNewGtinCodeSchema(Schema):
    gs_prefix: str
    gs_start: int
    gs_end: int


class GtinCodeInputSchema(Schema):
    gs_jancode: str
    product_jancode: str


class PurchaseInfosSchema(Schema):
    id: Optional[int] = None
    batch_code: str
    status: int
    exchange_rate: Optional[float] = None
    currency: Optional[str] = None
    regist_date: Optional[date] = None
    transport_type: Optional[int] = None
    transport_company: Optional[str] = None


class PurchaseDetailsUpsertInputSchema(Schema):
    id: Optional[int] = None
    product_id: int
    purchase_id: int
    jan_code: str
    batch_code: str
    quantity: int
    exchange_rate: float
    tax_form_code: Optional[str] = None
    tariff_rate: Optional[float] = None
    supplier_id: Optional[int] = None
    bare_price: Optional[float] = None
    alcohol_bag_price: Optional[float] = None
    envelope: Optional[float] = None
    instruction_manual_price: Optional[float] = None
    adapter_price: Optional[float] = None
    packaging_box_price: Optional[float] = None
    plastic_packaging_price: Optional[float] = None
    scratch_card_price: Optional[float] = None
    wax_pager_price: Optional[float] = None
    lamination_price: Optional[float] = None
    labor_cost: Optional[float] = None
    packaging_bag_price: Optional[float] = None
    other_price: Optional[float] = None


class PurchaseCustomSchema(Schema):
    id: Optional[int] = None
    product_id: int
    purchase_id: int
    jan_code: str
    batch_code: str
    chinese_name: Optional[str] = None
    english_name: Optional[str] = None
    material_chinese: Optional[str] = None
    material_english: Optional[str] = None
    product_usage: Optional[str] = None
    carton_size: Optional[str] = None
    glass_area: Optional[float] = None
    logo: Optional[str] = None
    bare_log: Optional[str] = None
    customs_remark: Optional[str] = None
    description: Optional[str] = None
    unit_price: Optional[int] = None
    per_box_grossweight: Optional[float] = None
    per_box_netweight: Optional[float] = None
    per_box_count: Optional[int] = None
    boxes_count: Optional[int] = None


class JancodeParentChildMappingListSchema(Schema):
    parent_jancode: str
    child_jancode: str
    product_price: float


class ItemcodeItemmanagecodeMappingSchema(Schema):
    id: Optional[int] = None
    item_code: str
    manage_code: str


class RPPDiscountInfosInputSchema(Schema):
    id: Optional[int] = None
    shopid: str
    shop_name: str
    effect_month: date
    discount_rate: float


class GracefulShopsSchema(Schema):
    id: Optional[int] = None
    shopid: str
    shop_code: str
    shopname: str
    shop_platform: int
