import secrets
import time

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_lifecycle import AFTER_CREATE, BEFORE_SAVE, LifecycleModel, hook

from accounts.manager import UserManager
from core.models import BaseModel


class User(AbstractUser, LifecycleModel):
    class AuthenticationProvider(models.TextChoices):
        GOOGLE = "GOOGLE", _("Google")
        APPLE = "APPLE", _("Apple")
        EMAIL = "EMAIL", _("Email")

    email = models.EmailField(verbose_name=_("Email"), unique=True)

    username = models.CharField(
        max_length=100, verbose_name=_("Username"), unique=True, blank=True
    )

    first_name = models.CharField(verbose_name=_("First Name"), max_length=100)

    last_name = models.CharField(verbose_name=_("Last Name"), max_length=100)

    mobile = models.CharField(verbose_name=_("Phone Number"), max_length=100)

    auth_provider = models.CharField(
        verbose_name=_("Authentication Provider"),
        max_length=15,
        choices=AuthenticationProvider.choices,
        default=AuthenticationProvider.EMAIL,
    )

    email_verified = models.BooleanField(
        verbose_name=_("Email Verified"), default=False
    )

    USERNAME_FIELD: str = "email"

    REQUIRED_FIELDS: list[str] = ["first_name", "last_name"]

    class Meta:
        ordering = ("-date_joined",)
        indexes = [
            models.Index(fields=["email"]),
            models.Index(fields=["username"]),
        ]

    objects = UserManager()

    def __str__(self) -> str:
        return str(self.email)

    def get_full_name(self) -> str:
        """
        Returns the first_name and last_name, with a space in between.
        """
        full_name: str = f"{self.first_name} {self.last_name}".strip().title()

        return full_name

    @hook(BEFORE_SAVE, when="email", is_not=None)
    def _update_username(self):
        self.username = self.email.lower()


class OTP(BaseModel):
    user = models.ForeignKey(
        User,
        verbose_name=_("User"),
        on_delete=models.CASCADE,
        related_name="otp_user",
    )

    otp_code = models.CharField(
        verbose_name=_("Otp Code"), max_length=4, db_index=True
    )

    def __str__(self) -> str:
        return f"{self.user.email} with code {self.otp_code}"

    @staticmethod
    def _time_exceeds_10mins(otp) -> bool:
        # checking whether OTP as exceed 10mins
        timer = 600

        start_time = otp.date_created.timestamp()

        elapsed_time = time.time() - start_time

        otp_exceeded_10_minutes = (
            True if elapsed_time > timer else False
        )  # 10 minutes in seconds

        return otp_exceeded_10_minutes

    @staticmethod
    def _generate_otp() -> str:
        return "".join([str(secrets.randbelow(10)) for _ in range(4)])

    @staticmethod
    def otp_session(user: User):
        # generating otp_code
        otp_code: str = OTP._generate_otp()

        OTP.objects.create(user=user, otp_code=otp_code)

        return True

    @staticmethod
    def check_otp(user: object, otp: str | None = None) -> bool:
        otp_ = OTP.objects.filter(user=user, otp_code=otp)

        # check if OTP has exceeded 10mins

        expired: bool = (
            OTP._time_exceeds_10mins(otp_.first()) if otp_.exists() else True
        )

        check: bool = otp_.exists() and not expired

        return check

    @hook(AFTER_CREATE)
    def _send_email(self):
        pass
