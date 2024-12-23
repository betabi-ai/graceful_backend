# Generated by Django 5.1.2 on 2024-10-23 00:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CpcGoodKeywords",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("shopid", models.CharField(max_length=20, verbose_name="店铺ID")),
                ("itemid", models.CharField(max_length=20, verbose_name="商品ID")),
                ("keyword", models.CharField(max_length=50, verbose_name="关键词")),
                (
                    "itemmngid",
                    models.CharField(max_length=32, verbose_name="商品管理ID"),
                ),
                ("cpc", models.IntegerField(verbose_name="CPC")),
                ("maxcpc", models.IntegerField(verbose_name="最大CPC")),
                ("recommendationcpc", models.IntegerField(verbose_name="目安CPC")),
                ("weightvalue", models.IntegerField(verbose_name="权重值")),
                ("cpc_rank", models.IntegerField(verbose_name="CPC排名")),
                (
                    "cpc_rank_updatedat",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="CPC排名更新时间"
                    ),
                ),
                ("natural_rank", models.IntegerField(verbose_name="自然排名")),
                (
                    "natural_rank_updatedat",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="自然排名更新时间"
                    ),
                ),
                ("cpc_asc", models.IntegerField(verbose_name="CPC递增值")),
                ("cpc_desc", models.IntegerField(verbose_name="CPC递减值")),
                ("enabled_cpc", models.BooleanField(verbose_name="是否启用CPC竞价")),
                ("is_deleted", models.BooleanField(verbose_name="是否删除")),
                (
                    "updatedat",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="乐天更新时间"
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="创建时间"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="更新时间"
                    ),
                ),
            ],
            options={
                "verbose_name": "CPC关键词",
                "verbose_name_plural": "CPC关键词",
                "db_table": "cpc_good_keywords",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="CpcGoodKeywordsRankLog",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("shopid", models.CharField(max_length=20)),
                ("itemid", models.CharField(max_length=20)),
                ("keyword", models.CharField(max_length=50)),
                ("cpc", models.IntegerField(blank=True, null=True)),
                ("recommendationcpc", models.IntegerField(blank=True, null=True)),
                ("rank", models.IntegerField()),
                ("rank_type", models.CharField(max_length=20)),
                ("created_at", models.DateTimeField(blank=True, null=True)),
            ],
            options={
                "db_table": "cpc_good_keywords_rank_log",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="CpcKeywordsGoods",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("shopid", models.CharField(max_length=20, verbose_name="店铺ID")),
                ("itemid", models.CharField(max_length=20, verbose_name="商品ID")),
                (
                    "itemmngid",
                    models.CharField(max_length=32, verbose_name="商品管理ID"),
                ),
                ("itemname", models.CharField(max_length=255, verbose_name="商品名称")),
                ("itemprice", models.IntegerField(verbose_name="商品价格")),
                ("itemurl", models.CharField(max_length=255, verbose_name="商品链接")),
                ("itemimageurl", models.CharField(max_length=255, verbose_name="主图")),
                (
                    "keywordcounts",
                    models.IntegerField(
                        blank=True, null=True, verbose_name="关键词数量"
                    ),
                ),
                ("cpc", models.IntegerField(blank=True, null=True, verbose_name="CPC")),
                ("is_deleted", models.BooleanField(verbose_name="是否删除")),
                (
                    "created_at",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="创建时间"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="更新时间"
                    ),
                ),
            ],
            options={
                "verbose_name": "CPC关键词商品列表",
                "verbose_name_plural": "CPC关键词商品列表",
                "db_table": "cpc_keywords_goods",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ShopGood",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("shopid", models.CharField(max_length=20)),
                ("itemid", models.CharField(max_length=20)),
                ("itemtype", models.CharField(max_length=20)),
                ("managenumber", models.CharField(max_length=30)),
                ("itemnumber", models.CharField(max_length=30)),
                ("title", models.CharField(max_length=255)),
                ("tagline", models.CharField(max_length=255)),
                ("standardprice", models.IntegerField(blank=True, null=True)),
                ("showitem", models.BooleanField(blank=True, null=True)),
                ("showsku", models.BooleanField(blank=True, null=True)),
                ("searchvisibility", models.BooleanField(blank=True, null=True)),
                ("unlimitedinventoryflag", models.BooleanField(blank=True, null=True)),
                ("isdeleted", models.BooleanField(blank=True, null=True)),
                ("isdraftitem", models.BooleanField(blank=True, null=True)),
                ("issinglesku", models.BooleanField(blank=True, null=True)),
                ("isinconsistentitem", models.BooleanField(blank=True, null=True)),
                ("created_at", models.DateTimeField(blank=True, null=True)),
                ("updated_at", models.DateTimeField(blank=True, null=True)),
            ],
            options={
                "db_table": "shop_good",
                "managed": False,
            },
        ),
    ]
