from typing import List, Optional
from ninja import ModelSchema, FilterSchema, Field

from stores.models import Category, Product, ProductImage, SubCategory


class CategoryOutSchema(ModelSchema):
    class Meta:
        model = Category
        fields = "__all__"


class SubCategoryOutSchema(ModelSchema):
    category: CategoryOutSchema

    class Meta:
        model = SubCategory
        fields = ["category", "name"]


class ProductFilterSchema(FilterSchema):
    search: Optional[str] = Field(None, q=['name__icontains', 'category__name__icontains'])


class ProductOutSchema(ModelSchema):
    category: CategoryOutSchema
    class Meta:
        model = Product
        fields = [
            "id",
            "category",
            "name",
            "overview",
            "description",
            "warranty",
            "image",
            "amount",
            "is_available",
        ]


class ProductImageOutSchema(ModelSchema):
    class Meta:
        model = ProductImage
        fields = ["id","image"]
