from ninja import ModelSchema


from reports.models import ReportCampagns


class ReportCampagnsSchema(ModelSchema):
    class Meta:
        model = ReportCampagns
        fields = "__all__"
        exclude = ["created_at", "adsalesafterdiscount", "periodtype"]
