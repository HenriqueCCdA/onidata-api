from datetime import datetime

import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.unity()
def test_positive_create_user(user):
    assert user.pk
    assert User.objects.exists()


@pytest.mark.unity()
def test_positive_create_superuser(superuser):
    assert superuser.is_staff
    assert superuser.is_superuser


@pytest.mark.unity()
def test_positive_default(user):
    assert not user.is_staff
    assert user.is_active
    assert not user.is_superuser


@pytest.mark.unity()
def test_str(user):
    assert str(user) == user.email


@pytest.mark.unity()
def test_normilized_email(db):
    user = User(email="lunadonald@EXAMPLE.oRg")
    user.clean()
    assert user.email == "lunadonald@example.org"


@pytest.mark.unity()
def test_create_at_and_modified_at(user):
    assert isinstance(user.created_at, datetime)
    assert isinstance(user.modified_at, datetime)
