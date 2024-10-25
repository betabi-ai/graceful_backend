from datetime import datetime
from ninja import Schema


class UserSchema(Schema):
    username: str
    is_authenticated: bool
    email: str = None
    date_joined: datetime = None


class CpcProductsSchema(Schema):
    itemid: int
    itemmngid: str
    itemname: str
    itemprice: int
    itemurl: str
    itemimageurl: str


class CpcGoodKeywordsSchema(Schema):
    id: int
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
    term_start_date: datetime | None = None
    term_end_date: datetime | None = None
    created_at: datetime | None = None
