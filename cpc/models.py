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
