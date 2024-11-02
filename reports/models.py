from django.db import models


class ReportCampagns(models.Model):
    id = models.BigAutoField(primary_key=True)
    shopid = models.CharField(max_length=20)
    effectdate = models.DateField(blank=True, null=True)
    rppcampaignid = models.IntegerField(blank=True, null=True)
    campaignname = models.CharField(max_length=20, blank=True, null=True)
    periodtype = models.IntegerField(blank=True, null=True)
    activebudget = models.IntegerField(blank=True, null=True)
    clickprice = models.IntegerField(blank=True, null=True)
    adsalesafterdiscount = models.IntegerField(blank=True, null=True)
    consumptionrate = models.DecimalField(
        max_digits=10, decimal_places=4, blank=True, null=True
    )
    ctr = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    startdate = models.DateField(blank=True, null=True)
    enddate = models.DateField(blank=True, null=True)
    totalclick = models.IntegerField(blank=True, null=True)
    totaladcost = models.IntegerField(blank=True, null=True)
    totalcpc = models.IntegerField(blank=True, null=True)
    total12hgms = models.IntegerField(blank=True, null=True)
    total12cv = models.IntegerField(blank=True, null=True)
    total12cvr = models.DecimalField(
        max_digits=10, decimal_places=4, blank=True, null=True
    )
    total12roas = models.DecimalField(
        max_digits=10, decimal_places=4, blank=True, null=True
    )
    total12cpa = models.IntegerField(blank=True, null=True)
    total720hgms = models.IntegerField(blank=True, null=True)
    total720cv = models.IntegerField(blank=True, null=True)
    total720cvr = models.DecimalField(
        max_digits=10, decimal_places=4, blank=True, null=True
    )
    total720roas = models.DecimalField(
        max_digits=10, decimal_places=4, blank=True, null=True
    )
    total720cpa = models.IntegerField(blank=True, null=True)
    newclick = models.IntegerField(blank=True, null=True)
    newadcost = models.IntegerField(blank=True, null=True)
    newcpc = models.IntegerField(blank=True, null=True)
    new12hgms = models.IntegerField(blank=True, null=True)
    new12cv = models.IntegerField(blank=True, null=True)
    new12cvr = models.DecimalField(
        max_digits=10, decimal_places=4, blank=True, null=True
    )
    new12roas = models.DecimalField(
        max_digits=10, decimal_places=4, blank=True, null=True
    )
    new12cpa = models.IntegerField(blank=True, null=True)
    new720hgms = models.IntegerField(blank=True, null=True)
    new720cv = models.IntegerField(blank=True, null=True)
    new720cvr = models.DecimalField(
        max_digits=10, decimal_places=4, blank=True, null=True
    )
    new720roas = models.DecimalField(
        max_digits=10, decimal_places=4, blank=True, null=True
    )
    new720cpa = models.IntegerField(blank=True, null=True)
    existclick = models.IntegerField(blank=True, null=True)
    existadcost = models.IntegerField(blank=True, null=True)
    existcpc = models.IntegerField(blank=True, null=True)
    exist12hgms = models.IntegerField(blank=True, null=True)
    exist12cv = models.IntegerField(blank=True, null=True)
    exist12cvr = models.DecimalField(
        max_digits=10, decimal_places=4, blank=True, null=True
    )
    exist12roas = models.DecimalField(
        max_digits=10, decimal_places=4, blank=True, null=True
    )
    exist12cpa = models.IntegerField(blank=True, null=True)
    exist720hgms = models.IntegerField(blank=True, null=True)
    exist720cv = models.IntegerField(blank=True, null=True)
    exist720cvr = models.DecimalField(
        max_digits=10, decimal_places=4, blank=True, null=True
    )
    exist720roas = models.DecimalField(
        max_digits=10, decimal_places=4, blank=True, null=True
    )
    exist720cpa = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "report_campagns"


class ReportKeywords(models.Model):
    """
    "download_id",  # 返回的数据字段
    """

    """
    "shopid",
    "effectdate",
    "periodtype",
    "itempageurl",
    "itemurl",
    "keywordstring",
    "ctr",
    "keywordrecommendedcpc",
    "keywordcpc",  # 以下字段3个类型报告字段顺序一致
    "totalclicksvalid",
    "totaladsalesbeforediscount",
    "totalcpc",
    "newclicksvalid",
    "newadsalesbeforediscount",
    "newcpc",
    "existclicksvalid",
    "existadsalesbeforediscount",
    "existcpc",
    "total12hgms",
    "total12hcv",
    "total12hcvr",
    "total12hroas",
    "total12hcpa",
    "total720hgms",
    "total720hcv",
    "total720hcvr",
    "total720hroas",
    "total720hcpa",
    "new12hgms",
    "new12hcv",
    "new12hcvr",
    "new12hroas",
    "new12hcpa",
    "new720hgms",
    "new720hcv",
    "new720hcvr",
    "new720hroas",
    "new720hcpa",
    "exist12hgms",
    "exist12hcv",
    "exist12hcvr",
    "exist12hroas",
    "exist12hcpa",
    "exist720hgms",
    "exist720hcv",
    "exist720hcvr",
    "exist720hroas",
    "exist720hcpa",
    """

    shopid = models.CharField(max_length=20)
    effectdate = models.DateField(blank=True, null=True)
    itemurl = models.CharField(max_length=30)
    periodtype = models.IntegerField(blank=True, null=True)
    keywordstring = models.CharField(max_length=50)
    ctr = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    totalclicksvalid = models.IntegerField(blank=True, null=True)
    totaladsalesbeforediscount = models.IntegerField(blank=True, null=True)
    totalcpc = models.IntegerField(blank=True, null=True)
    total12hgms = models.IntegerField(blank=True, null=True)
    total12hcv = models.IntegerField(blank=True, null=True)
    total12hcvr = models.DecimalField(
        max_digits=10, decimal_places=4, blank=True, null=True
    )
    total12hroas = models.DecimalField(
        max_digits=10, decimal_places=4, blank=True, null=True
    )
    total12hcpa = models.IntegerField(blank=True, null=True)
    total720hgms = models.IntegerField(blank=True, null=True)
    total720hcv = models.IntegerField(blank=True, null=True)
    total720hcvr = models.DecimalField(
        max_digits=10, decimal_places=4, blank=True, null=True
    )
    total720hroas = models.DecimalField(
        max_digits=10, decimal_places=4, blank=True, null=True
    )
    total720hcpa = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "report_keywords"


class ReportGoods(models.Model):
    id = models.BigAutoField(primary_key=True)
    shopid = models.CharField(max_length=20)
    effectdate = models.DateField(blank=True, null=True)
    itempageurl = models.CharField(max_length=255, blank=True, null=True)
    itemurl = models.CharField(max_length=30, blank=True, null=True)
    periodtype = models.IntegerField(blank=True, null=True)
    clickprice = models.IntegerField(blank=True, null=True)
    ctr = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    cpc = models.IntegerField(blank=True, null=True)
    totalclicksvalid = models.IntegerField(blank=True, null=True)
    totaladsalesbeforediscount = models.IntegerField(blank=True, null=True)
    totalcpc = models.IntegerField(blank=True, null=True)
    newclicksvalid = models.IntegerField(blank=True, null=True)
    newadsalesbeforediscount = models.IntegerField(blank=True, null=True)
    newcpc = models.IntegerField(blank=True, null=True)
    existclicksvalid = models.IntegerField(blank=True, null=True)
    existadsalesbeforediscount = models.IntegerField(blank=True, null=True)
    existcpc = models.IntegerField(blank=True, null=True)
    total12hgms = models.IntegerField(blank=True, null=True)
    total12hcv = models.IntegerField(blank=True, null=True)
    total12hcvr = models.DecimalField(
        max_digits=10, decimal_places=4, blank=True, null=True
    )
    total12hroas = models.DecimalField(
        max_digits=10, decimal_places=4, blank=True, null=True
    )
    total12hcpa = models.IntegerField(blank=True, null=True)
    total720hgms = models.IntegerField(blank=True, null=True)
    total720hcv = models.IntegerField(blank=True, null=True)
    total720hcvr = models.DecimalField(
        max_digits=10, decimal_places=4, blank=True, null=True
    )
    total720hroas = models.DecimalField(
        max_digits=10, decimal_places=4, blank=True, null=True
    )
    total720hcpa = models.IntegerField(blank=True, null=True)
    new12hgms = models.IntegerField(blank=True, null=True)
    new12hcv = models.IntegerField(blank=True, null=True)
    new12hcvr = models.DecimalField(
        max_digits=10, decimal_places=4, blank=True, null=True
    )
    new12hroas = models.DecimalField(
        max_digits=10, decimal_places=4, blank=True, null=True
    )
    new12hcpa = models.IntegerField(blank=True, null=True)
    new720hgms = models.IntegerField(blank=True, null=True)
    new720hcv = models.IntegerField(blank=True, null=True)
    new720hcvr = models.DecimalField(
        max_digits=10, decimal_places=4, blank=True, null=True
    )
    new720hroas = models.DecimalField(
        max_digits=10, decimal_places=4, blank=True, null=True
    )
    new720hcpa = models.IntegerField(blank=True, null=True)
    exist12hgms = models.IntegerField(blank=True, null=True)
    exist12hcv = models.IntegerField(blank=True, null=True)
    exist12hcvr = models.DecimalField(
        max_digits=10, decimal_places=4, blank=True, null=True
    )
    exist12hroas = models.DecimalField(
        max_digits=10, decimal_places=4, blank=True, null=True
    )
    exist12hcpa = models.IntegerField(blank=True, null=True)
    exist720hgms = models.IntegerField(blank=True, null=True)
    exist720hcv = models.IntegerField(blank=True, null=True)
    exist720hcvr = models.DecimalField(
        max_digits=10, decimal_places=4, blank=True, null=True
    )
    exist720hroas = models.DecimalField(
        max_digits=10, decimal_places=4, blank=True, null=True
    )
    exist720hcpa = models.IntegerField(blank=True, null=True)
    download_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "report_goods"
