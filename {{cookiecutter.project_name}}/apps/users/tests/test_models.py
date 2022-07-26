import pytest
from users.models import User
from users.tests.fixtures import *  # noqa: F401

from .factories import UserFactory


def test_user_factory(user_factory):
    assert user_factory is not None
    assert user_factory is UserFactory


def test_user_model(user: User):
    assert user is not None
    assert isinstance(user, User)


def test_user_str_is_not_blank(user: User):
    assert user.__str__() is not None


def test_user_has_parm(user: User):
    assert user.has_perm(perm="") is True


def test_user_has_module_perms(user: User):
    assert user.has_module_perms(app_label=".") is True


def test_user_parametrize(user: User):
    assert user is not None
    assert user.first_name is not None
    assert user.last_name is not None
    assert user.email is not None
    assert user.password is not None


def test_user_can_be_created(user: User):
    _user = User.objects._create_user("test@mail.com", user.password)
    assert _user.email == "test@mail.com"


def test_user_can_not_be_created_without_email(user: User):
    with pytest.raises(ValueError, match="The given email must be set"):
        User.objects._create_user(None, user.password)


def test_super_user_can_be_created(user: User):
    _suser = User.objects.create_superuser(
        email="suser@mail.com", password=user.password
    )
    assert _suser.email == "suser@mail.com"
    assert _suser.is_superuser is True
    assert _suser.is_staff is True


def test_superuser_must_be_staff(user: User):
    with pytest.raises(ValueError, match="Superuser must have is_staff=True."):
        User.objects.create_superuser(None, user.password, is_staff=False)


def test_superuser_must_be_is_superuser(user: User):
    with pytest.raises(ValueError, match="Superuser must have is_superuser=True."):
        User.objects.create_superuser(None, user.password, is_superuser=False)


def test_create_user(user: User):
    _user = User.objects.create_user("test_user@mail.com", user.password)
    assert _user.email == "test_user@mail.com"
    assert _user.is_superuser is False
    assert _user.is_staff is False
    assert _user.is_active is True
