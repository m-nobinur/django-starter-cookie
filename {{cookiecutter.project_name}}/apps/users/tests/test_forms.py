import pytest
from django.http import request
from users.forms import UserLoginForm, UserSignupForm
from users.models import User
from users.tests.fixtures import *  # noqa: F401


@pytest.mark.parametrize(
    "first_name,last_name, email, password1, password2, expected_is_valid",
    [
        (
            "John",
            "Doe",
            "john@mail.com",
            "XYZ12345",
            "XYZ12345",
            True,
        ),
        (
            "John",
            "Doe",
            "",
            "XYZ12345",
            "XYZ12345",
            False,
        ),
        (
            "John",
            "Doe",
            "john@mail.com",
            "XYZ12345",
            "XYZ12",
            False,
        ),
        (
            "John",
            "",
            "john@mail.com",
            "XYZ12345",
            "XYZ12",
            False,
        ),
    ],
)
def test_signup_form_is_valid(
    first_name, last_name, email, password1, password2, expected_is_valid, db
):
    form = UserSignupForm(
        data={
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password1": password1,
            "password2": password2,
        }
    )
    assert form.is_valid() == expected_is_valid


@pytest.mark.parametrize(
    "email, password, expected_is_valid",
    [
        (
            "john@mail.com",
            "XYZ12345",
            False,
        ),
    ],
)
def test_login_form_is_valid(email, password, expected_is_valid, db):
    form = UserLoginForm(
        data={
            "email": email,
            "password": password,
        }
    )
    assert form.is_valid() == expected_is_valid


def test_signup_form_save_method(db, user: User, client):

    form = UserSignupForm(
        data={
            "first_name": "first_name",
            "last_name": "last_name",
            "email": "email@mail.com",
            "password1": "password1234",
            "password2": "password1234",
        }
    )

    assert form.is_valid()
    assert callable(form.save)
    assert form.cleaned_data["first_name"] == "first_name"
    assert form.cleaned_data["last_name"] == "last_name"
    assert form.cleaned_data["email"] == "email@mail.com"
    assert form.cleaned_data["password1"] == "password1234"
    assert form.cleaned_data["password2"] == "password1234"

    assert isinstance(form.save(client), User)


#     assert not form.is_valid()
#     assert len(form.errors) == 1
#     assert "username" in form.errors
#     assert form.errors["username"][0] == _("This username has already been taken.")
