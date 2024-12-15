from typing import Any, List
from django.db.models import Q
from django.conf import settings
from ninja import Router
from ninja_jwt.authentication import JWTAuth

from ninja.orm import create_schema
from ninja.pagination import paginate, PageNumberPagination

from data_management.schemas import (
    CreateNewGtinCodeSchema,
    GtinCodeInputSchema,
    GtinCodeSchema,
    ProductsSuppliersSchema,
    ProductsUpsertSchema,
)
from data_management.tools import generate_gs_one_jancodes
from shares.models import GsoneJancode, Products, ProductsSuppliers

router = Router(auth=JWTAuth())
_PAGE_SIZE = getattr(settings, "PAGE_SIZE", 30)

ProductsSchema = create_schema(Products, exclude=["updated_by", "created_at"])


# =========================== products =================================


@router.get("/products", response=List[ProductsSchema], tags=["datas_management"])
@paginate(PageNumberPagination, page_size=_PAGE_SIZE)
def get_products(
    request,
    q: str = "",
    sort: str = "status,created_at",
    status: int = -1,
    supplier: str = "all",
):
    query = Q()
    if q:
        query &= (
            Q(itemid__icontains=q)
            | Q(jan_code__icontains=q)
            | Q(product_name__icontains=q)
        )
    if status != -1:
        query &= Q(status=status)
    if supplier and supplier != "all":
        query &= Q(supplier_id=supplier)
    if sort:
        sorts = sort.split(",")
    else:
        sorts = ["status", "-created_at"]
    qs = Products.objects.filter(query).order_by(*sorts)

    return qs


@router.post("/products/upsert", response=ProductsSchema, tags=["datas_management"])
def upsert_product(request, data: ProductsUpsertSchema):

    product = data.dict()
    user = request.user
    if user:
        product["updated_by"] = user
    new_product, _ = Products.objects.update_or_create(id=data.id, defaults=product)

    return new_product


# =========================== suppliers =================================


@router.get(
    "/suppliers", response=List[ProductsSuppliersSchema], tags=["datas_management"]
)
def get_all_products_suppliers(request):
    return ProductsSuppliers.objects.all()


@router.post(
    "/suppliers/upsert", response=ProductsSuppliersSchema, tags=["datas_management"]
)
def upsert_product(request, data: ProductsSuppliersSchema):

    supplier = data.dict()
    user = request.user
    if user:
        supplier["updated_by"] = user
    new_supplier, _ = ProductsSuppliers.objects.update_or_create(
        id=data.id, defaults=supplier
    )

    return new_supplier


# =========================== gsone_jancode =================================


@router.get("/gtins", response=List[GtinCodeSchema], tags=["datas_management"])
@paginate(PageNumberPagination, page_size=_PAGE_SIZE)
def get_gsone_jancodes(
    request,
    sort: str = "gs_jancode",
    q: str = "",
):
    query = Q()
    if q:
        query &= Q(gs_jancode__icontains=q) | Q(product_jancode__icontains=q)
    qs = GsoneJancode.objects.filter(query).order_by(sort)

    return qs


@router.post(
    "/gtins/upsert",
    response=GtinCodeSchema,
    tags=["datas_management"],
)
def relate_product_jan_code(request, data: GtinCodeInputSchema):
    # print(data)
    gs = GsoneJancode.objects.filter(gs_jancode=data.gs_jancode).first()
    if gs:
        user = request.user
        if user:
            gs.updated_by = user
        gs.product_jancode = data.product_jancode
        gs.save()
    return gs


@router.post(
    "/gtins/calc",
    response={200: Any, 422: Any},
    tags=["datas_management"],
)
def calc_gtin_codes(request, data: CreateNewGtinCodeSchema):
    gs = GsoneJancode.objects.filter(gs_prefix=data.gs_prefix).first()
    if gs:
        return 422, {"message": f"【{data.gs_prefix}】9位数字已经计算生成过了！！！"}
    # 457363815

    user = request.user
    if user:
        datas = generate_gs_one_jancodes(
            data.gs_prefix, data.gs_start, data.gs_end, user
        )
    else:
        datas = generate_gs_one_jancodes(
            data.gs_prefix, data.gs_start, data.gs_end, None
        )

    GsoneJancode.objects.bulk_create(datas)

    return 200, {
        "message": "{data.gs_prefix}】9位数字的GTIN（JANコード）计算成功！！！"
    }
