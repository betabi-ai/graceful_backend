from typing import Optional
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
