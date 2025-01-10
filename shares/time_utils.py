from datetime import datetime
from dateutil.relativedelta import relativedelta


def get_previous_months_first_day(current_date: datetime, months: int):
    # 存储结果
    first_days = []
    for i in range(months):
        # 计算前 i+1 月的第一天
        first_day = (current_date.replace(day=1) - relativedelta(months=i)).replace(
            day=1
        )
        first_days.append(first_day.strftime("%Y-%m-%d"))
    return first_days


def get_date_first_month_day(current_date: datetime):
    return (current_date.replace(day=1)).strftime("%Y-%m-%d")
