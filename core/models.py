from django.db import models
from django.utils.translation import gettext_lazy as _
from django_lifecycle import LifecycleModel

from ninja_jwt.tokens import RefreshToken as SimpleJWTRefreshToken



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


class RefreshToken(SimpleJWTRefreshToken):
    @classmethod
    def for_user(cls, user):
        token = super().for_user(user)
        # Add custom claims
        token["user_id"] = str(user.id) # type: ignore
        token["user_email"] = user.email # type: ignore
        token["user_username"] = user.username # type: ignore
        token["user_fullname"] = user.get_full_name() # type: ignore
        return token