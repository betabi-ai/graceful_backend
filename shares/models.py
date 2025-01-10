from django.db import models
from django.utils.translation import gettext as _, gettext_lazy as _l
from django.contrib.auth.models import User  # 导入 User 模型

DEFAULT_USER_ID = 1


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


class RakutenMonitorKeywordsRank(models.Model):
    id = models.BigAutoField(primary_key=True)
    shopid = models.CharField(max_length=20)
    itemid = models.CharField(max_length=20)
    keyword = models.CharField(max_length=50)
    rank = models.IntegerField()
    rank_type = models.CharField(max_length=20)
    order_no = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "rakuten_monitor_keywords_rank"


# 商品表model
class Products(models.Model):
    id = models.BigAutoField(primary_key=True)
    itemid = models.CharField(max_length=50)
    jan_code = models.CharField(max_length=20)
    product_price = models.IntegerField()
    product_name = models.CharField(max_length=100, blank=True, null=True)
    gtin_code = models.CharField(max_length=13, blank=True, null=True)
    bare_code = models.CharField(max_length=20, blank=True, null=True)
    item_count = models.IntegerField(blank=True, null=True)
    category = models.ForeignKey(
        "ProductCategories",
        on_delete=models.DO_NOTHING,  # 当 ProductCategories 被删除时不做任何修改
        blank=True,
        null=True,
        related_name="related_categories",
    )
    stock_quantity = models.IntegerField(blank=True, null=True)
    compatible_models = models.CharField(max_length=200, blank=True, null=True)
    attribute = models.CharField(max_length=200, blank=True, null=True)
    status = models.IntegerField()
    weight = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    adapter_desc = models.CharField(max_length=200, blank=True, null=True)
    box_properties_desc = models.CharField(max_length=200, blank=True, null=True)
    notices_desc = models.CharField(max_length=200, blank=True, null=True)
    packaging_desc = models.CharField(max_length=200, blank=True, null=True)
    alcohol_pack_desc = models.CharField(max_length=200, blank=True, null=True)
    supplier_id = models.IntegerField(blank=True, null=True)
    min_order_quantity = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_DEFAULT,
        default=DEFAULT_USER_ID,
        related_name="products_updated_by",
    )

    class Meta:
        managed = False
        db_table = "products"


# 供货商基本信息表 Model
class ProductsSuppliers(models.Model):
    """
    供货商基本信息表 Model
    """

    supplier_name = models.CharField(max_length=100)
    contact_details = models.CharField(max_length=100, blank=True, null=True)
    contact = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_DEFAULT,
        default=DEFAULT_USER_ID,
        related_name="supplier_updated_by",
    )

    class Meta:
        managed = False
        db_table = "products_suppliers"


class GsoneJancode(models.Model):
    gs_prefix = models.CharField(max_length=9)
    gs_jancode = models.CharField(unique=True, max_length=13)
    gs_index = models.IntegerField()
    product_jancode = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField()
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_DEFAULT,
        default=DEFAULT_USER_ID,
        related_name="gtin_updated_by",
    )

    class Meta:
        managed = False
        db_table = "gsone_jancode"


# 进货清单表
class PurchaseInfos(models.Model):
    batch_code = models.CharField(unique=True, max_length=50)
    status = models.IntegerField(blank=True, null=True)
    exchange_rate = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, blank=True, null=True)
    regist_date = models.DateField(blank=True, null=True)
    transport_type = models.IntegerField(blank=True, null=True)
    transport_company = models.CharField(max_length=100, blank=True, null=True)
    updated_at = models.DateTimeField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_DEFAULT,
        default=DEFAULT_USER_ID,
        related_name="purchase_updated_by",
    )

    class Meta:
        managed = False
        db_table = "purchase_infos"


# 进货详细表
class PurchaseDetails(models.Model):
    jan_code = models.CharField(max_length=20)
    product_id = models.IntegerField()
    purchase_id = models.IntegerField()
    batch_code = models.CharField(max_length=50)
    quantity = models.IntegerField()
    exchange_rate = models.DecimalField(max_digits=10, decimal_places=2)
    tax_form_code = models.CharField(max_length=30, blank=True, null=True)
    tariff_rate = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    supplier_id = models.IntegerField(blank=True, null=True)
    remaining_quantity = models.IntegerField(blank=True, null=True)

    # 价格对象
    price_datas = models.JSONField(blank=True, null=True)

    updated_at = models.DateTimeField(blank=True, null=True)
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_DEFAULT,
        default=DEFAULT_USER_ID,
        related_name="purchase_detail_updated_by",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = "purchase_details"


# 海关报关信息表 Model
class PurchaseCustomInfos(models.Model):
    purchase_id = models.IntegerField()
    batch_code = models.CharField(max_length=50)
    product_id = models.IntegerField()
    jan_code = models.CharField(max_length=20)
    chinese_name = models.CharField(max_length=50, blank=True, null=True)
    english_name = models.CharField(max_length=50, blank=True, null=True)
    material_chinese = models.CharField(max_length=20, blank=True, null=True)
    material_english = models.CharField(max_length=20, blank=True, null=True)
    product_usage = models.CharField(max_length=20, blank=True, null=True)
    carton_size = models.CharField(max_length=200, blank=True, null=True)
    glass_area = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    logo = models.CharField(max_length=50, blank=True, null=True)
    bare_log = models.CharField(max_length=50, blank=True, null=True)
    customs_remark = models.CharField(max_length=200, blank=True, null=True)

    boxes_count = models.IntegerField(blank=True, null=True)
    per_box_count = models.IntegerField(blank=True, null=True)
    per_box_netweight = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    per_box_grossweight = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    unit_price = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=200, blank=True, null=True)

    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_DEFAULT,
        default=DEFAULT_USER_ID,
        related_name="custom_updated_by",
    )
    updated_at = models.DateTimeField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = "purchase_custom_infos"


# Jan code 一对多的对应关系 model 如：1111 --> 1234X2223
class JancodeParentChildMapping(models.Model):
    parent_jancode = models.CharField(max_length=20)
    child_jancode = models.CharField(max_length=20)
    product_price = models.IntegerField()
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_DEFAULT,
        default=DEFAULT_USER_ID,
        related_name="jancode_mapping_updated_by",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = "jancode_parent_child_mapping"


class Orders(models.Model):
    order_number = models.CharField(primary_key=True, max_length=20)
    order_date = models.DateTimeField(blank=True, null=True)
    shop_code = models.CharField(max_length=10, blank=True, null=True)
    shop_name = models.CharField(max_length=100, blank=True, null=True)
    order_code = models.CharField(max_length=50, blank=True, null=True)
    client_section_name1 = models.CharField(max_length=100, blank=True, null=True)
    client_section_name2 = models.CharField(max_length=100, blank=True, null=True)
    client_name = models.CharField(max_length=100, blank=True, null=True)
    client_kana = models.CharField(max_length=100, blank=True, null=True)
    client_zip = models.CharField(max_length=10, blank=True, null=True)
    client_address1 = models.CharField(max_length=255, blank=True, null=True)
    client_address2 = models.CharField(max_length=255, blank=True, null=True)
    client_tel = models.CharField(max_length=20, blank=True, null=True)
    client_mail = models.CharField(max_length=255, blank=True, null=True)
    terminal_type = models.SmallIntegerField(blank=True, null=True)
    ship_section_name1 = models.CharField(max_length=100, blank=True, null=True)
    ship_section_name2 = models.CharField(max_length=100, blank=True, null=True)
    ship_name = models.CharField(max_length=100, blank=True, null=True)
    ship_kana = models.CharField(max_length=100, blank=True, null=True)
    ship_zip = models.CharField(max_length=10, blank=True, null=True)
    ship_address1 = models.CharField(max_length=255, blank=True, null=True)
    ship_address2 = models.CharField(max_length=255, blank=True, null=True)
    ship_tel = models.CharField(max_length=20, blank=True, null=True)
    delivery_number = models.CharField(max_length=50, blank=True, null=True)
    delivery_type_code = models.CharField(max_length=20, blank=True, null=True)
    delivery_type_name = models.CharField(max_length=100, blank=True, null=True)
    delivery_code = models.CharField(max_length=20, blank=True, null=True)
    delivery_name = models.CharField(max_length=100, blank=True, null=True)
    delivery_req_date = models.DateField(blank=True, null=True)
    delivery_time_code = models.CharField(max_length=20, blank=True, null=True)
    delivery_time_name = models.CharField(max_length=100, blank=True, null=True)
    delivery_date = models.DateField(blank=True, null=True)
    multiple_delivery_flag = models.SmallIntegerField(blank=True, null=True)
    payment_code = models.CharField(max_length=20, blank=True, null=True)
    payment_name = models.CharField(max_length=100, blank=True, null=True)
    order_option1 = models.CharField(max_length=100, blank=True, null=True)
    order_option2 = models.CharField(max_length=100, blank=True, null=True)
    order_option3 = models.CharField(max_length=100, blank=True, null=True)
    order_option4 = models.CharField(max_length=100, blank=True, null=True)
    order_option5 = models.CharField(max_length=100, blank=True, null=True)
    order_option6 = models.CharField(max_length=100, blank=True, null=True)
    order_option7 = models.CharField(max_length=100, blank=True, null=True)
    order_option8 = models.CharField(max_length=100, blank=True, null=True)
    order_option9 = models.CharField(max_length=100, blank=True, null=True)
    order_option10 = models.CharField(max_length=100, blank=True, null=True)
    order_memo = models.CharField(max_length=200, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    subtotal_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    tax_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    tax_base = models.SmallIntegerField(blank=True, null=True)
    tax_round = models.SmallIntegerField(blank=True, null=True)
    tax_system_type = models.SmallIntegerField(blank=True, null=True)
    carriage_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    cash_on_delivery = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    option1_fee = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    option2_fee = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    point = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    coupon = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    taxin_total_price_10 = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    taxin_total_price_8 = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    taxin_total_price_0 = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    tax_total_price_10 = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    tax_total_price_8 = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    phase_name = models.CharField(max_length=50, blank=True, null=True)
    check_mark1 = models.SmallIntegerField(blank=True, null=True)
    check_mark2 = models.SmallIntegerField(blank=True, null=True)
    check_mark3 = models.SmallIntegerField(blank=True, null=True)
    cancel_flag = models.SmallIntegerField(blank=True, null=True)
    bundle_flag = models.SmallIntegerField(blank=True, null=True)
    bundle_ahead_number = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    creating_source_type = models.CharField(max_length=10, blank=True, null=True)
    delivery_memo = models.CharField(max_length=200, blank=True, null=True)
    mail_type = models.SmallIntegerField(blank=True, null=True)
    mail_name = models.CharField(max_length=50, blank=True, null=True)
    reserve_type = models.SmallIntegerField(blank=True, null=True)
    reserve_name = models.CharField(max_length=100, blank=True, null=True)
    short_memo = models.CharField(max_length=200, blank=True, null=True)
    postit_color = models.CharField(max_length=20, blank=True, null=True)
    postit_memo = models.CharField(max_length=200, blank=True, null=True)
    createdat = models.DateTimeField(blank=True, null=True)
    detail_downloaded = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "orders"


# 已经拆分好jan code 的订单详情 model
class OrderDetailsCalc(models.Model):
    id = models.BigAutoField(primary_key=True)
    order_number = models.CharField(max_length=20)
    jan_cd = models.CharField(max_length=10, blank=True, null=True)
    original_jan_cd = models.CharField(max_length=50, blank=True, null=True)
    item_code = models.CharField(max_length=50, blank=True, null=True)
    attribute1_code = models.CharField(max_length=50, blank=True, null=True)
    attribute1_name = models.CharField(max_length=200, blank=True, null=True)
    attribute2_code = models.CharField(max_length=50, blank=True, null=True)
    attribute2_name = models.CharField(max_length=200, blank=True, null=True)
    amount = models.IntegerField(blank=True, null=True)
    amount_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    tax_type = models.SmallIntegerField(blank=True, null=True)
    reduced_tax_rate_type = models.SmallIntegerField(blank=True, null=True)
    freight_type = models.SmallIntegerField(blank=True, null=True)
    free_item_code = models.CharField(max_length=50, blank=True, null=True)
    component_flag = models.SmallIntegerField(blank=True, null=True)
    tax_rate = models.SmallIntegerField(blank=True, null=True)
    sender_type = models.SmallIntegerField(blank=True, null=True)
    target_stock_type = models.SmallIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    order_date = models.DateTimeField(blank=True, null=True)
    order_day = models.DateField(blank=True, null=True)
    order_month = models.DateField(blank=True, null=True)
    order_year = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "order_details_calc"


# 商品管理番号（商品URL）与 商品番号 的对应关系 model
class ItemcodeItemmanagecodeMapping(models.Model):
    id = models.BigAutoField(primary_key=True)
    item_code = models.CharField(max_length=50)
    manage_code = models.CharField(max_length=50)
    updated_at = models.DateTimeField()
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_DEFAULT,
        default=DEFAULT_USER_ID,
        related_name="itemcode_itemmanagecode_updated_by",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = "itemcode_itemmanagecode_mapping"


class RppDiscountInfos(models.Model):
    id = models.BigAutoField(primary_key=True)
    shopid = models.CharField(max_length=20)
    shop_name = models.CharField(max_length=50)
    effect_month = models.DateField()
    discount_rate = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    updated_at = models.DateTimeField()
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_DEFAULT,
        default=DEFAULT_USER_ID,
        related_name="rpp_discount_infos_updated_by",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = "rpp_discount_infos"


class GracefulShops(models.Model):
    shopid = models.CharField(max_length=20)
    shopname = models.CharField(max_length=50)
    shop_login_id1 = models.CharField(max_length=50, blank=True, null=True)
    shop_login_pw1 = models.CharField(max_length=50, blank=True, null=True)
    shop_login_id2 = models.CharField(max_length=50, blank=True, null=True)
    shop_login_pw2 = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    shop_code = models.CharField(max_length=10, blank=True, null=True)
    shop_platform = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "graceful_shops"


class ProductCategories(models.Model):
    category_name = models.CharField(max_length=50)
    # parent_id = models.IntegerField(blank=True, null=True)
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="subcategories",
    )
    category_level = models.IntegerField()
    price_template = models.JSONField(null=True, blank=True)
    updated_at = models.DateTimeField()
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_DEFAULT,
        default=DEFAULT_USER_ID,
        related_name="product_categories_updated_by",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = "product_categories"


# 销售月汇总
class SalesPageMonthsSummary(models.Model):
    """销售月汇总"""

    shopid = models.CharField(max_length=20)
    shop_code = models.CharField(max_length=20, blank=True, null=True)
    effect_month = models.DateField(blank=True, null=True)
    item_code = models.CharField(max_length=50, blank=True, null=True)
    manage_code = models.CharField(max_length=50, blank=True, null=True)
    amount_price = models.DecimalField(
        max_digits=16, decimal_places=2, blank=True, null=True
    )
    jan_count = models.IntegerField(blank=True, null=True)
    order_count = models.IntegerField(blank=True, null=True)
    tax_price = models.DecimalField(
        max_digits=16, decimal_places=2, blank=True, null=True
    )
    coupon = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    shipping_fee = models.DecimalField(
        max_digits=14, decimal_places=2, blank=True, null=True
    )
    total_orginal_price = models.DecimalField(
        max_digits=14, decimal_places=2, blank=True, null=True
    )
    afl_rewards = models.DecimalField(
        max_digits=14, decimal_places=2, blank=True, null=True
    )
    afl_order_count = models.IntegerField(blank=True, null=True)
    total720hgms = models.IntegerField(blank=True, null=True)
    total720hcv = models.IntegerField(blank=True, null=True)
    ca_actual_amount = models.IntegerField(blank=True, null=True)
    ca_sales_count = models.IntegerField(blank=True, null=True)
    advertisingfees = models.IntegerField(blank=True, null=True)
    deal_sales_value = models.IntegerField(blank=True, null=True)
    rmail_chargefee = models.IntegerField(blank=True, null=True)
    pointsawarded = models.IntegerField(blank=True, null=True)
    updated_at = models.DateTimeField()
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_DEFAULT,
        default=DEFAULT_USER_ID,
        related_name="sales_page_months_summary_updated_by",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = "sales_page_months_summary"
