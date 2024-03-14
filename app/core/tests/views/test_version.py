import pytest
from django.shortcuts import resolve_url
from rest_framework.status import HTTP_200_OK

URL = resolve_url("api_version")


@pytest.mark.integration()
def test_version(client_api):

    response = client_api.get(URL)

    assert response.status_code == HTTP_200_OK
