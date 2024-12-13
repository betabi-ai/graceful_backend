from ninja import ModelSchema, Schema


# Create your models here.
class ProductsSuppliersSchema(Schema):
    id: int
    supplier_name: str
