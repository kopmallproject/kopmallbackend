from typing import List

from django.shortcuts import get_object_or_404

from ninja import Query, Router

from core.schema import NOTFOUND_404OUTSCHEMA
from stores.models import Category, Product, ProductImage
from stores.schema import (
    CategoryOutSchema,
    ProductFilterSchema,
    ProductImageOutSchema,
    ProductOutSchema,
)

router = Router()


@router.get(
    "/categories",
    description="The endpoint to list all categories",
    response={200: List[CategoryOutSchema]},
)
def list_categories(request):
    return Category.objects.all()


@router.get(
    "/{category_id}/categories",
    description="The endpoint to get a category by ID",
    response={200: CategoryOutSchema},
)
def get_category(request, category_id: int):
    return get_object_or_404(Category, pk=category_id)


@router.get(
    "/products",
    description="The endpoint to get all products",
    response={200: List[ProductOutSchema]},
)
def list_products(request, filters: ProductFilterSchema = Query(...)):
    products = filters.filter(Product.objects.select_related("category").all())
    return products


@router.get(
    "/{category_id}/products/category",
    description="The endpoint that queries all product under a category",
    response={200: List[ProductOutSchema]},
)
def list_products_by_category(request, category_id: int):
    products = Product.objects.select_related("category").filter(category_id=category_id)
    return products


@router.get(
    "/{product_id}/products",
    description="The endpoint to get a product by ID",
    response={200: ProductOutSchema, 404: NOTFOUND_404OUTSCHEMA},
)
def get_product(request, product_id: int):
    product = Product.objects.select_related("category").filter(pk=product_id).first()
    
    if not product:
        return 404, {'message': "Product is not available"}

    return product


@router.get(
    "/{product_id}/products-image",
    description="The endpoint queries out a single product images",
    response={200: List[ProductImageOutSchema]},
)
def get_product_images(request, product_id: int):
    product_images = ProductImage.objects.select_related("product__category").filter(
        product_id=product_id
    )
    return product_images