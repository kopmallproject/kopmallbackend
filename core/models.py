from django.db import models
from django.utils.translation import gettext_lazy as _
from django_lifecycle import LifecycleModel



class _BaseModel(models.Manager):
    def get_queryset(self):
        return super().get_queryset()


class BaseModelQuerySet(models.QuerySet):
    pass


BaseModelManager = _BaseModel.from_queryset(BaseModelQuerySet)


class BaseModel(LifecycleModel):
    date_updated = models.DateTimeField(
        verbose_name=_("Date Updated"), auto_now=True
    )
    date_created = models.DateTimeField(
        verbose_name=_("Date Created"), auto_now_add=True
    )

    objects = BaseModelManager()
    super_objects = models.Manager()

    class Meta:
        abstract = True
        ordering = ["-date_created"]

