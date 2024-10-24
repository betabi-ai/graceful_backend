from django.contrib import admin

from cpc.models import CpcGoodKeywords


class CpcGoodKeywordsAdmin(admin.ModelAdmin):
    list_display = (
        # "itemid",
        "keyword",
        "itemmngid",
        "cpc",
        "maxcpc",
        "recommendationcpc",
        "weightvalue",
        "cpc_rank",
        "cpc_rank_updatedat",
        "natural_rank",
        "natural_rank_updatedat",
    )
    search_fields = ("keyword",)


admin.site.register(CpcGoodKeywords, CpcGoodKeywordsAdmin)
