from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import User as UserType
from django.db import models
from django.db.models.fields import BooleanField, CharField, DateTimeField, EmailField
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields) -> UserType:
        """Create and save a user with the given email, and
        password.
        """
        if not email:
            raise ValueError("The given email must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields) -> UserType:
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields) -> UserType:
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email: EmailField = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    first_name: CharField = models.CharField(
        _("first name"),
        max_length=30,
        blank=True,
    )
    last_name: CharField = models.CharField(
        _("last name"),
        max_length=150,
        blank=True,
    )
    is_staff: BooleanField = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into " "this admin site."),
    )
    is_active: BooleanField = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be "
            "treated as active. Unselect this instead "
            "of deleting accounts."
        ),
    )
    is_admin: BooleanField = models.BooleanField(
        default=False,
        help_text=_("Designates whether the user is admin or not."),
    )

    date_joined: DateTimeField = models.DateTimeField(
        _("date joined"),
        auto_now_add=True,
    )
    objects = UserManager()

    USERNAME_FIELD = "email"

    def __str__(self) -> str:
        return self.email

    def has_perm(self, perm, obj=None) -> bool:
        return True

    def has_module_perms(self, app_label) -> bool:
        return True
