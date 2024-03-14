import pytest
from django.test import RequestFactory

from app.conftest import fake
from app.core.services import extract_client_id


@pytest.mark.unity()
@pytest.mark.parametrize("ip", [fake.ipv4(), fake.ipv6()])
def test_positive_extract_client_id_without_x_forwared_for(ip):

    request = RequestFactory().get("/", REMOTE_ADDR=ip)

    assert extract_client_id(request.META) == ip


@pytest.mark.unity()
@pytest.mark.parametrize("ips", [f"{fake.ipv4(), fake.ipv4()}", f"{fake.ipv6(), fake.ipv6()}"], ids=["ipv4", "ipv6"])
def test_positive_extract_client_id_with_x_forwared_for(ips):

    request = RequestFactory().get("/", headers={"X_FORWARDED_FOR": ips})

    expected_client_ip = ips.split(",")[0]

    assert extract_client_id(request.META) == expected_client_ip
