# 商品数据模板title与数据库字段的对应
PRODUCT_UPLOAD_FIELDNAME_MAPPING = {
    "商品コード": "itemid",
    "JANコード": "jan_code",
    "中文商品名": "product_name",
    "商品价格(JPY)": "product_price",
    "商品类目": "category_name",
    "属性1名": "attribute",
    "属性2名": "compatible_models",
    "GTIN（JANコード）": "gtin_code",
    "数量": "item_count",
    "裸片JAN": "bare_code",
    "取扱状況": "status",
    "供货商": "supplier_id",
    "一套重量(g)": "weight",
    "适配神器说明": "adapter_desc",
    "箱属性说明": "box_properties_desc",
    "注意事项": "notices_desc",
    "包装盒说明": "packaging_desc",
    "酒精包种类": "alcohol_pack_desc",
    "起訂量": "min_order_quantity",
}

# products插入值时，处理默认值
PRODUCT_DEFAULT_VALUES = {
    "itemid": "",
    "jan_code": "",
    "product_name": "",
    "product_price": 0,
    "attribute": "",
    "compatible_models": "",
    "gtin_code": "",
    "item_count": 0,
    "bare_code": "",
    "status": 1,
    "supplier_id": None,
    "weight": 0,
    "adapter_desc": "",
    "box_properties_desc": "",
    "notices_desc": "",
    "packaging_desc": "",
    "alcohol_pack_desc": "",
    "min_order_quantity": 0,
}

# 批次下的进货信息导入时的字段与数据库字段对应关系
PURCHASE_PRODUCT_UPLOAD_FIELDNAME_MAPPING = {
    "JANコード": "jan_code",
    "进货数量": "quantity",
    "裸片仕入単価(CNY)": "bare_price",
    "酒精包(CNY)": "alcohol_bag_price",
    "信封(CNY)": "envelope",
    "说明书(CNY)": "instruction_manual_price",
    "贴膜神器(CNY)": "adapter_price",
    "包装盒(CNY)": "packaging_box_price",
    "吸塑(CNY)": "plastic_packaging_price",
    "刮卡(CNY)": "scratch_card_price",
    "蜡纸(CNY)": "wax_pager_price",
    "过塑(CNY)": "lamination_price",
    "人工(CNY)": "labor_cost",
    "包装袋(CNY)": "packaging_bag_price",
    "其他(CNY)": "other_price",
    "税表番号": "tax_form_code",
    "関税率": "tariff_rate",
}

# 批次下的进货信息导入时的字段默认值对应
PURCHASE_PRODUCT_UPLOAD_DEFAULT_VALUE = {
    "jan_code": "",
    "quantity": 0,
    "bare_price": 0.0,
    "alcohol_bag_price": 0.0,
    "envelope": 0.0,
    "instruction_manual_price": 0.0,
    "adapter_price": 0.0,
    "packaging_box_price": 0.0,
    "plastic_packaging_price": 0.0,
    "scratch_card_price": 0.0,
    "wax_pager_price": 0.0,
    "lamination_price": 0.0,
    "labor_cost": 0.0,
    "packaging_bag_price": 0.0,
    "other_price": 0.0,
    "tax_form_code": "",
    "tariff_rate": 0.0,
}

# 报关信息导入时的字段与数据库字段对应关系
PURCHASE_CUSTOM_UPLOAD_FIELDNAME_MAPPING = {
    "JANコード": "jan_code",
    "商品中文名": "chinese_name",
    "商品英文名": "english_name",
    "成品材质中文名": "material_chinese",
    "成品材质英文名": "material_english",
    "用途": "product_usage",
    "描述": "description",
    "单价(JPY)": "unit_price",
    "箱数": "boxes_count",
    "每箱数量": "per_box_count",
    "每箱净重(KG)": "per_box_netweight",
    "每箱毛重(KG)": "per_box_grossweight",
    "包装尺寸(CM)": "carton_size",
    "玻璃面積(㎡)": "glass_area",
    "海关备注": "customs_remark",
    "裸件LOGO": "bare_log",
    "成品LOGO": "logo",
}

# 报关信息导入时的字段默认值对应
PURCHASE_CUSTOM_UPLOAD_DEFAULT_VALUE = {
    "jan_code": "",
    "chinese_name": "",
    "english_name": "",
    "material_chinese": "",
    "material_english": "",
    "product_usage": "",
    "description": "",
    "unit_price": 0.0,
    "boxes_count": 0,
    "per_box_count": 0,
    "per_box_netweight": 0.0,
    "per_box_grossweight": 0.0,
    "carton_size": "",
    "glass_area": 0.0,
    "customs_remark": "",
    "bare_log": "",
    "logo": "",
}


# 商品番号和管理番号对应关系
ITEMCODE_ITEMMANAGECOD_EMAPPING = {
    "商品管理番号（商品URL）": "manage_code",
    "商品番号": "item_code",
}
