from allauth.account.forms import SignupForm
from allauth.socialaccount.forms import SignupForm as SocialSignupForm

from django.contrib.auth import forms as admin_forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class UserAdminCreationForm(admin_forms.UserCreationForm):
    """Form for User Creation in the Admin Area."""

    class Meta(admin_forms.UserCreationForm.Meta):
        model = User

        error_messages = {
            "username": {"unique": _("This username has already been taken.")}
        }


class UserAdminChangeForm(admin_forms.UserChangeForm):
    """Form for User Change in the Admin Area."""

    class Meta(admin_forms.UserChangeForm.Meta):
        model = User


class UserSignupForm(SignupForm):
    """
    Form that will be rendered on a user sign up section/screen.
    Default fields will be added automatically.
    Check UserSocialSignupForm for accounts created from social.
    """

    class Meta:
        model = User


class UserSocialSignupForm(SocialSignupForm):
    """
    Renders the form when user has signed up using social accounts.
    Default fields will be added automatically.
    See UserSignupForm otherwise.
    """
