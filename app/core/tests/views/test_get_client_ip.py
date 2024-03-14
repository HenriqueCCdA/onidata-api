import pytest
from django.shortcuts import resolve_url
from rest_framework.status import HTTP_200_OK

from app.conftest import fake

URL = resolve_url("get_client_ip")


@pytest.mark.integration
def test_get_client_ip(client_api):

    ip = fake.ipv4()

    response = client_api.get(URL, REMOTE_ADDR=ip)

    assert response.status_code == HTTP_200_OK

    assert response.json() == {"client_ip": ip}
