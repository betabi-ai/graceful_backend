import csv
from datetime import date
from shares.enums import DeviceType
from shares.models import RakutenSalesIndicators

skip_lines = 3

_HEADER_COLUMNS = [
    "日付",
    "曜日",
    "デバイス",
    "売上金額",
    "売上件数",
    "アクセス人数",
    "転換率",
    "客単価",
    "ユニークユーザー数",
    "購入者数（会員）",
    "購入者数（非会員）",
    "新規購入者数",
    "リピート購入者数",
    "税額（外税額）",
    "送料額",
    "クーポン値引額（店舗）",
    "クーポン値引額（楽天）",
    "送料無料クーポン",
    "のし・ラッピング代金",
    "決済手数料",
    "サブジャンルTOP10平均 売上金額",
    "月商別平均値（月商1億以上） 売上金額",
    "月商別平均値（月商3,000万～9,999万） 売上金額",
    "月商別平均値（月商1,000万～2,999万） 売上金額",
    "月商別平均値（月商100万～999万） 売上金額",
    "月商別平均値（月商50万～99万） 売上金額",
    "月商別平均値（月商50万未満） 売上金額",
    "サブジャンルTOP10平均 売上件数",
    "月商別平均値（月商1億以上） 売上件数",
    "月商別平均値（月商3,000万～9,999万） 売上件数",
    "月商別平均値（月商1,000万～2,999万） 売上件数",
    "月商別平均値（月商100万～999万） 売上件数",
    "月商別平均値（月商50万～99万） 売上件数",
    "月商別平均値（月商50万未満） 売上件数",
    "サブジャンルTOP10平均 アクセス人数",
    "月商別平均値（月商1億以上） アクセス人数",
    "月商別平均値（月商3,000万～9,999万） アクセス人数",
    "月商別平均値（月商1,000万～2,999万） アクセス人数",
    "月商別平均値（月商100万～999万） アクセス人数",
    "月商別平均値（月商50万～99万） アクセス人数",
    "月商別平均値（月商50万未満） アクセス人数",
    "サブジャンルTOP10平均 転換率",
    "月商別平均値（月商1億以上） 転換率",
    "月商別平均値（月商3,000万～9,999万） 転換率",
    "月商別平均値（月商1,000万～2,999万） 転換率",
    "月商別平均値（月商100万～999万） 転換率",
    "月商別平均値（月商50万～99万） 転換率",
    "月商別平均値（月商50万未満） 転換率",
    "サブジャンルTOP10平均 客単価",
    "月商別平均値（月商1億以上） 客単価",
    "月商別平均値（月商3,000万～9,999万） 客単価",
    "月商別平均値（月商1,000万～2,999万） 客単価",
    "月商別平均値（月商100万～999万） 客単価",
    "月商別平均値（月商50万～99万） 客単価",
    "月商別平均値（月商50万未満） 客単価",
    "楽天スーパーDEAL 売上金額",
    "楽天スーパーDEAL 売上件数",
    "楽天スーパーDEAL アクセス人数",
    "楽天スーパーDEAL 転換率",
    "楽天スーパーDEAL 客単価",
    "楽天スーパーDEAL ユニークユーザー数",
    "楽天スーパーDEAL 購入者数（会員）",
    "楽天スーパーDEAL 購入者数（非会員）",
    "楽天スーパーDEAL 新規購入者数",
    "楽天スーパーDEAL リピート購入者数",
    "運用型ポイント変倍経由売上金額",
    "運用型ポイント変倍経由売上件数",
    "運用型ポイント変倍経由ポイント付与料",
]


_COLUMNS_DICT = {
    "日付": "effectdate",
    "デバイス": "devicetype",
    "売上金額": "hgms",
    "売上件数": "hcv",
    "アクセス人数": "visit_count",
    "転換率": "ctr",
    "客単価": "avg_customer_price",
    "ユニークユーザー数": "unique_user_count",
    "購入者数（会員）": "members",
    "購入者数（非会員）": "not_members",
    "新規購入者数": "news",
    "リピート購入者数": "repeats",
    "税額（外税額）": "exclude_tax_amount",
    "送料額": "shipping_cost",
    "クーポン値引額（店舗）": "shop_coupon_discount",
    "クーポン値引額（楽天）": "rakuten_coupon_discount",
    "送料無料クーポン": "free_shipping_coupon",
    "のし・ラッピング代金": "gift_wrapping_fee",
    "決済手数料": "payment_fee",
    "サブジャンルTOP10平均 売上金額": "top10_avg_sales_amount",
    "月商別平均値（月商1億以上） 売上金額": "month_100_million_avg_amount",
    "月商別平均値（月商3,000万～9,999万） 売上金額": "month_30_million_avg_amount",
    "月商別平均値（月商1,000万～2,999万） 売上金額": "month_10_million_avg_amount",
    "月商別平均値（月商100万～999万） 売上金額": "month_million_avg_amount",
    "月商別平均値（月商50万～99万） 売上金額": "month_half_million_avg_amount",
    "月商別平均値（月商50万未満） 売上金額": "month_less_avg_amount",
    "サブジャンルTOP10平均 売上件数": "top10_avg_sales_count",
    "月商別平均値（月商1億以上） 売上件数": "month_100_million_avg_count",
    "月商別平均値（月商3,000万～9,999万） 売上件数": "month_30_million_avg_count",
    "月商別平均値（月商1,000万～2,999万） 売上件数": "month_10_million_avg_count",
    "月商別平均値（月商100万～999万） 売上件数": "month_million_avg_count",
    "月商別平均値（月商50万～99万） 売上件数": "month_half_million_avg_count",
    "月商別平均値（月商50万未満） 売上件数": "month_less_avg_count",
    "サブジャンルTOP10平均 アクセス人数": "top10_avg_visits",
    "月商別平均値（月商1億以上） アクセス人数": "month_100_million_avg_visits",
    "月商別平均値（月商3,000万～9,999万） アクセス人数": "month_30_million_avg_visits",
    "月商別平均値（月商1,000万～2,999万） アクセス人数": "month_10_million_avg_visits",
    "月商別平均値（月商100万～999万） アクセス人数": "month_million_avg_visits",
    "月商別平均値（月商50万～99万） アクセス人数": "month_half_million_avg_visits",
    "月商別平均値（月商50万未満） アクセス人数": "month_less_avg_visits",
    "サブジャンルTOP10平均 転換率": "top10_avg_ctr",
    "月商別平均値（月商1億以上） 転換率": "month_100_million_avg_ctr",
    "月商別平均値（月商3,000万～9,999万） 転換率": "month_30_million_avg_ctr",
    "月商別平均値（月商1,000万～2,999万） 転換率": "month_10_million_avg_ctr",
    "月商別平均値（月商100万～999万） 転換率": "month_million_avg_ctr",
    "月商別平均値（月商50万～99万） 転換率": "month_half_million_avg_ctr",
    "月商別平均値（月商50万未満） 転換率": "month_less_avg_ctr",
    "サブジャンルTOP10平均 客単価": "top10_avg_price",
    "月商別平均値（月商1億以上） 客単価": "month_100_million_avg_price",
    "月商別平均値（月商3,000万～9,999万） 客単価": "month_30_million_avg_price",
    "月商別平均値（月商1,000万～2,999万） 客単価": "month_10_million_avg_price",
    "月商別平均値（月商100万～999万） 客単価": "month_million_avg_price",
    "月商別平均値（月商50万～99万） 客単価": "month_half_million_avg_price",
    "月商別平均値（月商50万未満） 客単価": "month_less_avg_price",
    "楽天スーパーDEAL 売上金額": "super_deal_amount",
    "楽天スーパーDEAL 売上件数": "super_deal_count",
    "楽天スーパーDEAL アクセス人数": "super_deal_visits",
    "楽天スーパーDEAL 転換率": "super_deal_ctr",
    "楽天スーパーDEAL 客単価": "super_deal_price",
    "楽天スーパーDEAL ユニークユーザー数": "super_deal_unique_visits",
    "楽天スーパーDEAL 購入者数（会員）": "super_deal_members",
    "楽天スーパーDEAL 購入者数（非会員）": "super_deal_not_members",
    "楽天スーパーDEAL 新規購入者数": "super_deal_news",
    "楽天スーパーDEAL リピート購入者数": "super_deal_repeats",
    "運用型ポイント変倍経由売上金額": "invest_point_amount",
    "運用型ポイント変倍経由売上件数": "invest_point_count",
    "運用型ポイント変倍経由ポイント付与料": "invest_point_fee",
}


def read_rakuten_sales_indicators():
    # TODO 数据还有写死的
    with open(
        "/Users/kevincoder/Desktop/20241101_20241130_日次_店舗データ.csv", "r"
    ) as f:

        for _ in range(skip_lines):
            next(f)

        reader = csv.DictReader(f)

        # header_row = next(reader)
        header_row = reader.fieldnames

        if header_row == _HEADER_COLUMNS:
            # 如果相等，表示数据格式没问题
            datas = []
            dates = []
            for row in reader:
                mapped_row = {
                    _COLUMNS_DICT[key]: value
                    for key, value in row.items()
                    if key in _COLUMNS_DICT and value != ""
                }
                effectdate = mapped_row["effectdate"].replace("/", "-")
                today = date.today().strftime("%Y-%m-%d")
                print(effectdate, today)
                if today == effectdate:
                    break
                mapped_row["effectdate"] = effectdate
                mapped_row["shopid"] = "319134"
                dates.append(effectdate)
                mapped_row["devicetype"] = DeviceType[mapped_row["devicetype"]].value

                datas.append(RakutenSalesIndicators(**mapped_row))

            RakutenSalesIndicators.objects.filter(
                shopid="319134", effectdate__in=dates
            ).delete()

            RakutenSalesIndicators.objects.bulk_create(datas)


if __name__ == "__main__":
    read_rakuten_sales_indicators()
