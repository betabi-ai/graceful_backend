from django.db import models
from django.utils.translation import gettext as _, gettext_lazy as _l


# CPC（点击付费）广告的优质关键词模型
class CpcGoodKeywords(models.Model):
    shopid = models.CharField(_l("店铺ID"), max_length=20)  # 店铺ID
    itemid = models.CharField(_l("商品ID"), max_length=20)  # 商品ID
    keyword = models.CharField(_l("关键词"), max_length=50)  # 关键词
    itemmngid = models.CharField(_l("商品管理ID"), max_length=32)  # 商品管理ID
    cpc = models.IntegerField(
        _l("CPC"),
    )  # 当前CPC值
    maxcpc = models.IntegerField(
        _l("最大CPC"),
    )  # 最大CPC值
    recommendationcpc = models.IntegerField(
        _l("目安CPC"),
    )  # 推荐CPC值
    weightvalue = models.IntegerField(
        _l("权重值"),
    )  # 权重值
    cpc_rank = models.IntegerField(
        _l("CPC排名"),
    )  # CPC排名
    cpc_rank_updatedat = models.DateTimeField(
        _l("CPC排名更新时间"), blank=True, null=True
    )  # CPC排名更新时间
    natural_rank = models.IntegerField(
        _l("自然排名"),
    )  # 自然排名
    natural_rank_updatedat = models.DateTimeField(
        _l("自然排名更新时间"), blank=True, null=True
    )  # 自然排名更新时间
    cpc_asc = models.IntegerField(
        _l("CPC递增值"),
    )  # CPC竞价价格每次递增的值
    cpc_desc = models.IntegerField(
        _l("CPC递减值"),
    )  # CPC竞价价格每次递减的值
    enabled_cpc = models.BooleanField(
        _l("是否启用CPC竞价"),
    )  # 是否启用CPC竞价计算逻辑功能
    cpc_calc_method = models.IntegerField(_l("cpc计算的方法"), blank=True, null=True)
    is_deleted = models.BooleanField(
        _l("是否删除"),
    )  # 是否删除
    updatedat = models.DateTimeField(
        _l("乐天更新时间"), blank=True, null=True
    )  # 更新时间
    created_at = models.DateTimeField(_l("创建时间"), blank=True, null=True)  # 创建时间
    updated_at = models.DateTimeField(_l("更新时间"), blank=True, null=True)  # 更新时间

    def __str__(self):
        return self.keyword

    class Meta:
        managed = False  # 指示Django不管理该表的生命周期
        db_table = "cpc_good_keywords"  # 数据库表名

        verbose_name = _("CPC关键词")
        verbose_name_plural = _("CPC关键词")


# CPC广告的关键词排名日志模型
class CpcGoodKeywordsRankLog(models.Model):
    shopid = models.CharField(max_length=20)  # 店铺ID
    itemid = models.CharField(max_length=20)  # 商品ID
    keyword = models.CharField(max_length=50)  # 关键词
    cpc = models.IntegerField(blank=True, null=True)  # 当前CPC值（可选）
    recommendationcpc = models.IntegerField(blank=True, null=True)  # 推荐CPC值（可选）
    rank = models.IntegerField()  # 关键词排名
    rank_type = models.CharField(max_length=20)  # 排名类型（例如：CPC排名，自然排名）
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "cpc_good_keywords_rank_log"


# 有cpc广告的商品模型
class CpcKeywordsGoods(models.Model):
    shopid = models.CharField(_l("店铺ID"), max_length=20)  # 店铺ID
    itemid = models.CharField(_l("商品ID"), max_length=20)  # 商品ID
    itemmngid = models.CharField(_l("商品管理ID"), max_length=32)  # 商品管理ID
    itemname = models.CharField(_l("商品名称"), max_length=255)  # 商品名称
    itemprice = models.IntegerField(
        _l("商品价格"),
    )  # 商品价格
    itemurl = models.CharField(_l("商品链接"), max_length=255)  # 商品链接
    itemimageurl = models.CharField(_l("主图"), max_length=255)  # 商品主图片链接
    keywordcounts = models.IntegerField(
        _l("关键词数量"), blank=True, null=True
    )  # 关键词数量
    cpc = models.IntegerField(_l("CPC"), blank=True, null=True)  # CPC值
    is_deleted = models.BooleanField(
        _l("是否删除"),
    )  # 是否删除
    created_at = models.DateTimeField(_l("创建时间"), blank=True, null=True)  # 创建时间
    updated_at = models.DateTimeField(_l("更新时间"), blank=True, null=True)  # 更新时间

    class Meta:
        managed = False  # 指示Django不管理该表的生命周期
        db_table = "cpc_keywords_goods"  # 数据库表名
        unique_together = (("shopid", "itemid"),)  # shopid和itemid的唯一约束
        verbose_name_plural = verbose_name = _("CPC关键词商品列表")


# 店铺商品模型
class ShopGood(models.Model):
    """
    店铺商品模型
    """

    shopid = models.CharField(max_length=20)  # 店铺ID
    itemid = models.CharField(max_length=20)  # 商品ID
    itemtype = models.CharField(max_length=20)  # 商品类型
    managenumber = models.CharField(max_length=30)  # 商品管理编号
    itemnumber = models.CharField(max_length=30)  # 商品编号
    title = models.CharField(max_length=255)  # 商品标题
    tagline = models.CharField(max_length=255)  # 商品副标题
    standardprice = models.IntegerField(blank=True, null=True)  # 标准价格
    showitem = models.BooleanField(blank=True, null=True)  # 是否展示商品
    showsku = models.BooleanField(blank=True, null=True)  # 是否展示SKU
    searchvisibility = models.BooleanField(blank=True, null=True)  # 是否搜索可见
    unlimitedinventoryflag = models.BooleanField(blank=True, null=True)  # 无限库存标志
    isdeleted = models.BooleanField(blank=True, null=True)  # 是否删除
    isdraftitem = models.BooleanField(blank=True, null=True)  # 是否草稿商品
    issinglesku = models.BooleanField(blank=True, null=True)  # 是否单SKU
    isinconsistentitem = models.BooleanField(blank=True, null=True)  # 是否不一致商品
    created_at = models.DateTimeField(blank=True, null=True)  # 创建时间
    updated_at = models.DateTimeField(blank=True, null=True)  # 更新时间

    class Meta:
        managed = False  # 指示Django不管理该表的生命周期
        db_table = "shop_good"  # 数据库表名
        unique_together = (("shopid", "itemid"),)  # shopid和itemid的唯一约束


# Top关键词模型
class TopKeywords(models.Model):
    shopid = models.CharField(max_length=20)
    itemid = models.CharField(max_length=20)
    search_word = models.CharField(max_length=200)
    itemmngid = models.CharField(max_length=32)
    ldate = models.DateField(blank=True, null=True)
    item_rank = models.IntegerField()
    item_visit = models.IntegerField()
    date_type = models.IntegerField()
    item_visit_all = models.IntegerField()
    item_order_count_all = models.IntegerField()
    search_word_order_count = models.IntegerField()
    item_cvr_all = models.DecimalField(max_digits=10, decimal_places=2)
    search_word_cvr = models.DecimalField(max_digits=10, decimal_places=2)
    search_word_rank = models.IntegerField()
    search_word_ichiba_rank = models.IntegerField()
    search_word_visit = models.IntegerField()
    search_word_ichiba_visit = models.IntegerField()
    reg_date = models.DateTimeField(blank=True, null=True)
    term_start_date = models.DateField(blank=True, null=True)
    term_end_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "top_keywords_datas"


# 店铺广告预算模型
class ShopCampagnsBudget(models.Model):
    shopid = models.CharField(max_length=20)
    campaigntype = models.CharField(max_length=20, blank=True, null=True)
    campaignid = models.IntegerField(unique=True)
    campaignname = models.CharField(max_length=20)
    clickprice = models.IntegerField()
    budget = models.BigIntegerField()
    maxbudget = models.BigIntegerField()
    bugdgetasc = models.IntegerField()
    budgetoverdatetime = models.DateTimeField(blank=True, null=True)
    inactiveflag = models.BooleanField(blank=True, null=True)
    isuserrankenabled = models.BooleanField(blank=True, null=True)
    createdat = models.DateTimeField(blank=True, null=True)
    updatedat = models.DateTimeField(blank=True, null=True)
    itemcount = models.IntegerField(blank=True, null=True)
    monclicks = models.IntegerField(blank=True, null=True)
    dayclicks = models.IntegerField(blank=True, null=True)
    totalclicks = models.IntegerField(blank=True, null=True)
    monadsales = models.BigIntegerField(blank=True, null=True)
    dayadsales = models.BigIntegerField(blank=True, null=True)
    totaladsales = models.BigIntegerField(blank=True, null=True)
    budgetconsumptionrate = models.DecimalField(
        max_digits=10, decimal_places=4, blank=True, null=True
    )
    created_at = models.DateTimeField(blank=True, null=True)
    is_auto_calc = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "shop_campagns_budget"


# 店铺广告预算日志模型
class ShopCampagnsBudgetLog(models.Model):
    shopid = models.CharField(max_length=20)
    campaigntype = models.CharField(max_length=20, blank=True, null=True)
    campaignid = models.IntegerField()
    campaignname = models.CharField(max_length=20)
    clickprice = models.IntegerField()
    budget = models.BigIntegerField()
    inactiveflag = models.BooleanField(blank=True, null=True)
    isuserrankenabled = models.BooleanField(blank=True, null=True)
    updatedat = models.DateTimeField(blank=True, null=True)
    monclicks = models.IntegerField(blank=True, null=True)
    dayclicks = models.IntegerField(blank=True, null=True)
    totalclicks = models.IntegerField(blank=True, null=True)
    monadsales = models.BigIntegerField(blank=True, null=True)
    dayadsales = models.BigIntegerField(blank=True, null=True)
    totaladsales = models.BigIntegerField(blank=True, null=True)
    budgetconsumptionrate = models.DecimalField(
        max_digits=10, decimal_places=4, blank=True, null=True
    )
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "shop_campagns_budget_log"


class RakutenSalesIndicators(models.Model):
    shopid = models.CharField(max_length=20)
    effectdate = models.DateField()
    devicetype = models.IntegerField()
    hgms = models.IntegerField(blank=True, null=True)
    hcv = models.IntegerField(blank=True, null=True)
    visit_count = models.IntegerField(blank=True, null=True)
    ctr = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    avg_customer_price = models.IntegerField(blank=True, null=True)
    unique_user_count = models.IntegerField(blank=True, null=True)
    members = models.IntegerField(blank=True, null=True)
    not_members = models.IntegerField(blank=True, null=True)
    news = models.IntegerField(blank=True, null=True)
    repeats = models.IntegerField(blank=True, null=True)
    exclude_tax_amount = models.IntegerField(blank=True, null=True)
    shipping_cost = models.IntegerField(blank=True, null=True)
    shop_coupon_discount = models.IntegerField(blank=True, null=True)
    rakuten_coupon_discount = models.IntegerField(blank=True, null=True)
    free_shipping_coupon = models.IntegerField(blank=True, null=True)
    gift_wrapping_fee = models.IntegerField(blank=True, null=True)
    payment_fee = models.IntegerField(blank=True, null=True)
    top10_avg_sales_amount = models.IntegerField(blank=True, null=True)
    top10_avg_sales_count = models.IntegerField(blank=True, null=True)
    top10_avg_visits = models.IntegerField(blank=True, null=True)
    top10_avg_ctr = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    top10_avg_price = models.IntegerField(blank=True, null=True)
    month_100_million_avg_amount = models.IntegerField(blank=True, null=True)
    month_100_million_avg_count = models.IntegerField(blank=True, null=True)
    month_100_million_avg_visits = models.IntegerField(blank=True, null=True)
    month_100_million_avg_ctr = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    month_100_million_avg_price = models.IntegerField(blank=True, null=True)
    month_30_million_avg_amount = models.IntegerField(blank=True, null=True)
    month_30_million_avg_count = models.IntegerField(blank=True, null=True)
    month_30_million_avg_visits = models.IntegerField(blank=True, null=True)
    month_30_million_avg_ctr = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    month_30_million_avg_price = models.IntegerField(blank=True, null=True)
    month_10_million_avg_amount = models.IntegerField(blank=True, null=True)
    month_10_million_avg_count = models.IntegerField(blank=True, null=True)
    month_10_million_avg_visits = models.IntegerField(blank=True, null=True)
    month_10_million_avg_ctr = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    month_10_million_avg_price = models.IntegerField(blank=True, null=True)
    month_million_avg_amount = models.IntegerField(blank=True, null=True)
    month_million_avg_count = models.IntegerField(blank=True, null=True)
    month_million_avg_visits = models.IntegerField(blank=True, null=True)
    month_million_avg_ctr = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    month_million_avg_price = models.IntegerField(blank=True, null=True)
    month_half_million_avg_amount = models.IntegerField(blank=True, null=True)
    month_half_million_avg_count = models.IntegerField(blank=True, null=True)
    month_half_million_avg_visits = models.IntegerField(blank=True, null=True)
    month_half_million_avg_ctr = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    month_half_million_avg_price = models.IntegerField(blank=True, null=True)
    month_less_avg_amount = models.IntegerField(blank=True, null=True)
    month_less_avg_count = models.IntegerField(blank=True, null=True)
    month_less_avg_visits = models.IntegerField(blank=True, null=True)
    month_less_avg_ctr = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    month_less_avg_price = models.IntegerField(blank=True, null=True)
    super_deal_amount = models.IntegerField(blank=True, null=True)
    super_deal_count = models.IntegerField(blank=True, null=True)
    super_deal_visits = models.IntegerField(blank=True, null=True)
    super_deal_ctr = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    super_deal_price = models.IntegerField(blank=True, null=True)
    super_deal_unique_visits = models.IntegerField(blank=True, null=True)
    super_deal_members = models.IntegerField(blank=True, null=True)
    super_deal_not_members = models.IntegerField(blank=True, null=True)
    super_deal_news = models.IntegerField(blank=True, null=True)
    super_deal_repeats = models.IntegerField(blank=True, null=True)
    invest_point_amount = models.IntegerField(blank=True, null=True)
    invest_point_count = models.IntegerField(blank=True, null=True)
    invest_point_fee = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "rakuten_sales_indicators"


class PointsAwarded(models.Model):
    shopid = models.CharField(max_length=20)
    pointsawarded = models.IntegerField()
    effectdate = models.DateField()
    numbers = models.IntegerField()

    class Meta:
        managed = False
        db_table = "points_awarded"


class RakutenMonitorProducts(models.Model):
    shop_id = models.CharField(max_length=20, blank=True, null=True)
    item_id = models.CharField(max_length=20, blank=True, null=True)
    item_url = models.CharField(unique=True, max_length=255)
    item_img_url = models.CharField(max_length=255, blank=True, null=True)
    item_name = models.CharField(max_length=400, blank=True, null=True)
    shop_name = models.CharField(max_length=100, blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    item_number = models.CharField(max_length=100, blank=True, null=True)
    keywords = models.CharField(unique=True, max_length=100, blank=True, null=True)
    is_monitor = models.BooleanField(blank=True, null=True, default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = "rakuten_monitor_shops"
