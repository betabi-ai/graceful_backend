from ninja import ModelSchema, Schema


from reports.models import ReportCampagns, ReportGoods, ReportKeywords


class ReportCampagnsSchema(ModelSchema):
    class Meta:
        model = ReportCampagns
        fields = "__all__"
        exclude = ["created_at", "adsalesafterdiscount", "periodtype"]


class ReportKeywordsSchema(ModelSchema):

    class Meta:
        model = ReportKeywords
        fields = "__all__"
        exclude = ["periodtype"]


class ReportGoodsSchema(ModelSchema):
    class Meta:
        model = ReportGoods
        fields = "__all__"
        exclude = ["created_at", "periodtype", "download_id"]
