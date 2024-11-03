from datetime import datetime, date
from typing import Optional
from ninja import Schema
from pydantic import Field

from shares.models import ShopCampagnsBudget


# 主要用于错误信息的返回
class Message(Schema):
    message: str


# User Schema
class UserSchema(Schema):
    username: str
    is_authenticated: bool
    email: str = None
    date_joined: datetime = None


# 用于返回CPC商品列表
class CpcProductsSchema(Schema):
    itemid: int
    itemmngid: str
    # itemname: str
    keywordcounts: int | None = None
    cpc: int | None = None
    itemprice: int
    itemurl: str
    itemimageurl: str


# 用于返回CPC关键词列表
class CpcGoodKeywordsSchema(Schema):
    id: int
    shopid: str
    keyword: str
    itemmngid: str
    cpc: int
    maxcpc: int
    recommendationcpc: int
    weightvalue: int
    cpc_rank: int
    cpc_rank_updatedat: datetime | None = None
    natural_rank: int
    natural_rank_updatedat: datetime | None = None
    updatedat: datetime = None
    cpc_asc: int  # CPC竞价价格每次递增的值
    cpc_desc: int  # CPC竞价价格每次递减的值
    enabled_cpc: bool  # 是否启用CPC竞价


# 用于返回top关键词列表
class TopKeywordsSchema(Schema):
    shopid: int
    itemid: int
    search_word: str
    itemmngid: str
    ldate: datetime | None = None
    item_rank: int | None = None
    item_visit: int | None = None
    item_visit_all: int | None = None
    item_order_count_all: int | None = None
    search_word_order_count: int | None = None
    item_cvr_all: float | None = None
    search_word_cvr: float | None = None
    search_word_rank: int | None = None
    search_word_ichiba_rank: int | None = None
    search_word_visit: int | None = None
    search_word_ichiba_visit: int | None = None
    reg_date: datetime | None = None
    term_start_date: date | None = None
    term_end_date: date | None = None
    created_at: datetime | None = None

    class Config:
        json_encoders = {
            date: lambda v: v.strftime("%Y-%m-%d"),
        }


# 用于处理更新CPC关键词功能的输入
class CpcKeywordEnableChangeINSchema(Schema):
    """
    用于更新CPC关键词的 enabled_cpc 字段
    """

    id: int  # CPC关键词ID
    keyword: str
    shopid: str
    enabled_cpc: Optional[bool] = None  # 是否启用CPC竞价
    cpc_asc: Optional[int] = None  # CPC竞价价格每次递增的值
    cpc_desc: Optional[int] = None  # CPC竞价价格每次递减的值
    weightvalue: Optional[int] = None  # 权重值
    maxcpc: Optional[int] = None  # 最大CPC值


# 用于返回活动报表中的月份列表
class CampaignsMonthSchema(Schema):
    formatted_date: str  # 输出的日期字段，格式为 YYYY-MM


# 用于返回TopKeywords中的关键词和展示次数
class KeyValueTopKeywordsSchema(Schema):
    name: str = Field(alias="search_word")
    value: int = Field(alias="show_count")


# 用于返回店铺活动预算信息
class ShopCampagnsBudgetSchema(Schema):
    class Meta:
        model = ShopCampagnsBudget
        fields = "__all__"
        # exclude = ["created_at", "periodtype", "download_id"]
