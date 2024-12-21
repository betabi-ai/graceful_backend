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
    JancodeParentChildMappingListSchema,
    ProductsSuppliersSchema,
    ProductsUpsertSchema,
    PurchaseCustomSchema,
    PurchaseDetailsUpsertInputSchema,
    PurchaseInfosSchema,
)
from data_management.tools import generate_gs_one_jancodes
from shares.models import (
    GsoneJancode,
    JancodeParentChildMapping,
    ProductCustomInfos,
    Products,
    ProductsSuppliers,
    PurchaseDetails,
    PurchaseInfos,
)

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


@router.get("/products/all", response=List[Any], tags=["datas_management"])
def get_all_products(request):
    return Products.objects.filter().values(
        "id", "jan_code", "itemid", "product_name", "supplier_id"
    )


@router.get("/products/info", response=ProductsSchema, tags=["datas_management"])
def get_product_with_jancode(request, jancode: str):
    return Products.objects.filter(jan_code=jancode).first()


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
    "/gtins/upsert", response={200: GtinCodeSchema, 422: Any}, tags=["datas_management"]
)
def relate_product_jan_code(request, data: GtinCodeInputSchema):

    gj = GsoneJancode.objects.filter(product_jancode=data.product_jancode).first()
    if gj:
        return 422, {
            "message": f"商品JANコード【{data.product_jancode}】，已与【{data.gs_jancode}】进行了绑定！！！"
        }

    # print(data)

    gs = GsoneJancode.objects.filter(gs_jancode=data.gs_jancode).first()
    if gs:
        user = request.user
        if user:
            gs.updated_by = user
        gs.product_jancode = data.product_jancode
        gs.save()

    product = Products.objects.filter(jan_code=data.product_jancode).first()

    if product:
        product.gtin_code = data.gs_jancode
        product.save()
    return 200, gs


@router.post("/gtins/calc", response={200: Any, 422: Any}, tags=["datas_management"])
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


# =========================== purchase_infos =================================


@router.get("/purchases", response=List[PurchaseInfosSchema], tags=["datas_management"])
@paginate(PageNumberPagination, page_size=_PAGE_SIZE)
def get_purchase_infos(
    request,
    sort: str = "-created_at",
    status: int = -1,
    q: str = "",
):
    query = Q()
    if q:
        query &= Q(batch_code__icontains=q)
    if status != -1:
        query &= Q(status=status)
    qs = PurchaseInfos.objects.filter(query).order_by(sort)

    return qs


@router.get(
    "/purchases/{int:purchase_id}",
    response=PurchaseInfosSchema,
    tags=["datas_management"],
)
def get_purchase_info_with_id(request, purchase_id: int):

    return PurchaseInfos.objects.filter(id=purchase_id).first()


@router.get(
    "/purchases/details",
    response=List[PurchaseDetailsUpsertInputSchema],
    tags=["datas_management"],
)
def get_purchase_details(request, pid: int):
    return PurchaseDetails.objects.filter(purchase_id=pid)


@router.get(
    "/purchases/detail/{int:id}",
    response=PurchaseDetailsUpsertInputSchema,
    tags=["datas_management"],
)
def get_purchase_detail_info(request, id: int):
    return PurchaseDetails.objects.filter(id=id).first()


@router.post(
    "/purchases/upsert",
    response={200: PurchaseInfosSchema, 422: Any},
    tags=["datas_management"],
)
def upsert_purchase_info(request, data: PurchaseInfosSchema):
    query = ~Q(id=data.id)
    query &= Q(batch_code=data.batch_code)
    purchase = PurchaseInfos.objects.filter(query).first()
    print(purchase)
    if purchase:
        return 422, {"message": "批次号不能重复！！！"}
    purchase = data.dict()
    user = request.user
    if user:
        purchase["updated_by"] = user
    new_purchase, _ = PurchaseInfos.objects.update_or_create(
        id=data.id, defaults=purchase
    )

    return 200, new_purchase


# =========================== purchase_details =================================


@router.post(
    "/purchases/product/upsert",
    response=PurchaseDetailsUpsertInputSchema,
    tags=["datas_management"],
)
def upsert_purchase_product(request, data: PurchaseDetailsUpsertInputSchema):
    info = data.dict()
    user = request.user
    if user:
        info["updated_by"] = user
    new_info, _ = PurchaseDetails.objects.update_or_create(id=data.id, defaults=info)
    # print(new_info)

    return new_info


# =========================== product_custom_infos =================================


@router.get(
    "/purchases/customs", response=List[PurchaseCustomSchema], tags=["datas_management"]
)
def get_purchase_custom_infos(request, pid: int):
    qs = ProductCustomInfos.objects.filter(purchase_id=pid)

    return qs


@router.post(
    "/purchases/custom/upsert",
    response={200: PurchaseCustomSchema, 422: Any},
    tags=["datas_management"],
)
def upsert_purchase_custom_info(request, data: PurchaseCustomSchema):
    info = data.dict()
    user = request.user
    if user:
        info["updated_by"] = user
    new_info, _ = ProductCustomInfos.objects.update_or_create(id=data.id, defaults=info)

    return 200, new_info


# =========================== jancode_parent_child_mapping =================================


@router.get(
    "/jancode/parent-child",
    response=List[JancodeParentChildMappingListSchema],
    tags=["datas_management"],
    auth=None,
)
def get_jancode_parent_child_mapping(request, q: str = ""):
    """
    获取 parent_code 的子 code 映射关系
    """
    query = Q()
    # 检查参数
    if q:
        # 查询条件：匹配 parent_jancode 或 child_jancode
        query = Q(parent_jancode__icontains=q) | Q(child_jancode__icontains=q)

    relationships = (
        JancodeParentChildMapping.objects.filter(query)
        .values("parent_jancode")
        .distinct()
    )

    if relationships.exists():
        parent_codes = [rel["parent_jancode"] for rel in relationships]
        result = []

        for parent_code in parent_codes:
            children = JancodeParentChildMapping.objects.filter(
                parent_jancode=parent_code
            ).values_list("child_jancode", flat=True)
            result.append(
                {
                    "parent_code": parent_code,
                    "child_codes": list(children),
                }
            )

        return result

    return []


@router.post(
    "/jancode/parent-child/upsert",
    response=Any,
    tags=["datas_management"],
)
def upsert_jancode_parent_child_mapping(
    request, data: JancodeParentChildMappingListSchema
):
    """
    新增或更新 parent_code 的子 code 映射关系
    """

    parent_code = data.parent_code
    JancodeParentChildMapping.objects.filter(parent_jancode=parent_code).delete()
    user = request.user

    for child_code in data.child_codes:
        if user:
            JancodeParentChildMapping.objects.create(
                parent_jancode=parent_code, child_jancode=child_code, updated_by=user
            )
        else:
            JancodeParentChildMapping.objects.create(
                parent_jancode=parent_code, child_jancode=child_code
            )

    return {"message": "操作成功！！！"}
