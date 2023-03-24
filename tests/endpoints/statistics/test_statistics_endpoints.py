import pytest
from tests.endpoints.utils import client_login


@pytest.mark.parametrize(
    "user_type, stat_type, valid_response",
    [
        ('correct', 'profile', 200),
        ('unauthorized', 'profile', 401),
        ('correct', 'dealer', 200),
        ('unauthorized', 'dealer', 401),
        ('correct', 'saloon', 200),
        ('unauthorized', 'saloon', 401),
    ])
def test_stat_endpoints(client, setup_stat_endpoints, user_type, stat_type, valid_response):
    admin = setup_stat_endpoints
    client_login(client, user_type, admin, admin)
    base_url = 'http://localhost:8000/statistics/'
    url = f'{base_url}{stat_type}/'
    response = client.get(url)

    assert response.status_code == valid_response
