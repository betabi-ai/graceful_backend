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
