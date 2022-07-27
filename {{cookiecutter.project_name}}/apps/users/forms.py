from allauth.account import app_settings
from allauth.account.forms import LoginForm, SignupForm
from allauth.utils import get_username_max_length, set_form_field_order
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.forms.fields import EmailField
from django.utils.translation import gettext as _
from django.utils.translation import pgettext
from users.models import User

from .utils import (
    login_field_css_classes,
    login_password_css_classes,
    name_field_css_classes,
    password_field_css_classes,
    remember_me_css_classes,
)


class UserLoginForm(LoginForm):
    def __init__(self, *args, **kwargs) -> None:
        self.request = kwargs.pop("request", None)
        super(LoginForm, self).__init__(*args, **kwargs)
        if (
            app_settings.AUTHENTICATION_METHOD
            == app_settings.AuthenticationMethod.EMAIL
        ):  # pragma: no cover
            login_widget = forms.TextInput(
                attrs={
                    "type": "email",
                    "placeholder": _("E-mail address"),
                    "autocomplete": "email",
                    "autofocus": "autofocus",
                    "class": login_field_css_classes,
                }
            )
            login_field = forms.EmailField(label=_("E-mail"), widget=login_widget)
        elif (
            app_settings.AUTHENTICATION_METHOD
            == app_settings.AuthenticationMethod.USERNAME
        ):  # pragma: no cover
            login_widget = forms.TextInput(
                attrs={
                    "placeholder": _("Username"),
                    "autocomplete": "username",
                    "autofocus": "autofocus",
                    "class": login_field_css_classes,
                }
            )
            login_field = forms.CharField(  # type: ignore
                label=_("Username"),
                widget=login_widget,
                max_length=get_username_max_length(),
            )
        else:  # pragma: no cover
            assert (
                app_settings.AUTHENTICATION_METHOD
                == app_settings.AuthenticationMethod.USERNAME_EMAIL
            )
            login_widget = forms.TextInput(
                attrs={
                    "placeholder": _("Username or e-mail"),
                    "autocomplete": "email",
                    "class": login_field_css_classes,
                }
            )
            login_field: EmailField = forms.CharField(  # type: ignore
                label=pgettext("field label", "Login"), widget=login_widget
            )

        remeber_widget = forms.CheckboxInput(attrs={"class": remember_me_css_classes})
        password_widget = forms.PasswordInput(
            attrs={
                "placeholder": _("Password"),
                "class": login_password_css_classes,
            }
        )
        remeber_field = forms.CharField(
            widget=remeber_widget,
            required=False,
        )
        password_field = forms.CharField(
            widget=password_widget,
            required=True,
        )

        self.fields["remember"] = remeber_field
        self.fields["login"] = login_field
        self.fields["password"] = password_field
        set_form_field_order(self, ["login", "password", "remember"])
        if app_settings.SESSION_REMEMBER is not None:  # pragma: no cover
            del self.fields["remember"]


class UserSignupForm(SignupForm):
    first_name = forms.CharField(
        max_length=30,
        label="First Name",
        widget=forms.TextInput(
            attrs={"placeholder": _("First Name"), "class": name_field_css_classes}
        ),
    )
    last_name = forms.CharField(
        max_length=30,
        label="Last Name",
        widget=forms.TextInput(
            attrs={"placeholder": _("Last Name"), "class": name_field_css_classes}
        ),
    )

    def __init__(self, *args, **kwargs) -> None:
        super(SignupForm, self).__init__(*args, **kwargs)

        email_field = forms.EmailField(
            label=_("Email Address"),
            widget=forms.TextInput(
                attrs={
                    "type": "email",
                    "placeholder": _("E-mail address"),
                    "class": name_field_css_classes,
                }
            ),
        )

        self.fields["email"] = email_field
        self.fields["password1"] = PasswordField(
            label=_("Password"),
            autocomplete="new-password",
        )
        if app_settings.SIGNUP_PASSWORD_ENTER_TWICE:  # pragma: no cover
            self.fields["password2"] = PasswordField(
                label=_("Password (again)"),
                autocomplete="new-password",
            )

        self.fields["password2"].help_text = "Enter your password again."

        if hasattr(self, "field_order"):  # pragma: no cover
            set_form_field_order(self, self.field_order)

    def save(self, request) -> User:
        user = super().save(request)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.save()
        return user


class PasswordField(forms.CharField):
    def __init__(self, *args, **kwargs) -> None:
        render_value = kwargs.pop(
            "render_value", app_settings.PASSWORD_INPUT_RENDER_VALUE
        )
        kwargs["widget"] = forms.PasswordInput(
            render_value=render_value,
            attrs={
                "placeholder": kwargs.get("label"),
                "class": password_field_css_classes,
            },
        )
        autocomplete = kwargs.pop("autocomplete", None)
        if autocomplete is not None:  # pragma: no cover
            kwargs["widget"].attrs["autocomplete"] = autocomplete
        super().__init__(*args, **kwargs)


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name")

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True) -> User:
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:  # pragma: no cover
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ("email", "password", "is_active", "is_admin", "is_staff")
