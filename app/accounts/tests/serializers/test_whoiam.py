import pytest

from app.accounts.serializers import WhoamiSerializer


@pytest.mark.unity
def test_positive(user):

    serializer = WhoamiSerializer(instance=user)

    assert serializer.data == {
        "id": user.pk,
        "email": user.email,
        "created_at": user.created_at.astimezone().isoformat(),
        "modified_at": user.modified_at.astimezone().isoformat(),
    }
