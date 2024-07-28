from django.utils.timezone import now
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import BaseModel


def get_default_pic():
    return "default.png"


def upload_to(instance, filename):
    """
    Generate the upload file path.

    Parameters:
    instance: The model instance.
    filename (str): The filename.

    Returns:
    str: The upload file path.
    """
    # The file will be uploaded to MEDIA_ROOT/<tag>/year/month/day/<id>/<filename>
    t = now()
    return f"{t.year}/{t.month}/{t.day}/{instance.pk}_{filename}"


class Category(BaseModel):
    name = models.CharField(
        verbose_name=_("Name Of Category"), max_length=100, db_index=True
    )

    def __str__(self) -> str:
        return self.name


class SubCategory(BaseModel):
    category = models.ForeignKey(
        Category,
        verbose_name=_("Category"),
        on_delete=models.CASCADE,
        related_name="category_sub_cats",
    )
    name = models.CharField(verbose_name=_("Name Of SubCategory"), max_length=100)

    def __str__(self) -> str:
        return f"{self.category.name} -- {self.name}"


class Product(BaseModel):
    category = models.ForeignKey(
        Category,
        verbose_name=_("Category"),
        on_delete=models.CASCADE,
        related_name="category_products",
    )

    name = models.CharField(verbose_name=_("Product Name"), max_length=100)

    overview = models.CharField(
        verbose_name=_("Product Overview Message"), max_length=500
    )

    description = models.TextField(verbose_name=_("Product Description"), blank=True)

    warranty = models.TextField(verbose_name=_("Product Warranty"), blank=True)

    image = models.ImageField(
        verbose_name=_("Product Image"), upload_to=upload_to, default=get_default_pic
    )
    
    amount = models.DecimalField(
        verbose_name=_("Product Amount"), max_digits=10, decimal_places=2
    )

    is_available = models.BooleanField(
        verbose_name=_("Product Available"), default=True
    )

    def __str__(self) -> str:
        return f"{self.category.name} -- {self.name}"


class ProductImage(BaseModel):
    product = models.ForeignKey(
        Product,
        verbose_name=_("Product"),
        on_delete=models.CASCADE,
        related_name="product_images",
    )

    image = models.ImageField(
        verbose_name=_("Product Image"), upload_to=upload_to, default=get_default_pic
    )

    def __str__(self) -> str:
        return f"{self.product.name} -- {self.pk}"
