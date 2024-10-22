from datetime import datetime
from ninja import Schema


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
