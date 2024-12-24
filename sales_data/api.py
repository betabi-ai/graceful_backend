from typing import Any, List
from ninja import Router, File
from ninja_jwt.authentication import JWTAuth
from django.db.models import Q, Sum, F
from django.db.models.functions import (
    TruncMonth,
    TruncYear,
    TruncDate,
    Extract,
    TruncDay,
)

import pandas as pd

from shares.models import OrderDetailsCalc

router = Router(auth=JWTAuth())


@router.get(
    "/jan_sales",
    response=List[Any],
    auth=None,
    tags=["sale_datas"],
)
def get_jancode_sales_amount_infos(
    request, start: str = None, end: str = None, group_by: str = "month"
):

    # # 验证日期范围
    # if not start or not end:
    #     raise ValueError("Start and end dates are required.")

    # # 构造查询
    # query = Q(order_day__range=[start, end])

    # qs = (
    #     OrderDetailsCalc.objects.filter(query)
    #     .annotate(day=TruncDay("order_day"))
    #     .values("jan_cd", "day")
    #     .annotate(total_count=Sum("amount"), total_amount=Sum("amount_price"))
    #     .order_by("jan_cd")
    # )
    # if group_by == "month":
    #     qs = (
    #         OrderDetailsCalc.objects.filter(query)
    #         .annotate(day=TruncMonth("order_day"))
    #         .values("jan_cd", "day")
    #         .annotate(total_count=Sum("amount"), total_amount=Sum("amount_price"))
    #         .order_by("jan_cd")
    #     )
    # elif group_by == "year":
    #     qs = (
    #         OrderDetailsCalc.objects.filter(query)
    #         .annotate(day=TruncYear("order_day"))
    #         .values("jan_cd", "day")
    #         .annotate(total_count=Sum("amount"), total_amount=Sum("amount_price"))
    #         .order_by("jan_cd")
    #     )

    # return qs

    pass
