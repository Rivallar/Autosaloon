import pytest
import datetime

from cars.models import AutoSaloon, SaloonCars
from trading.models import SaloonDiscount

pytestmark = pytest.mark.django_db


def client_login(client, user_type, correct_user, wrong_user):

    """Authenticates correct or wrong users for tests"""

    if user_type == 'correct':
        client.force_authenticate(user=correct_user)
    elif user_type == 'wrong':
        client.force_authenticate(user=wrong_user)
    return client


def make_endpoint(base_url, endpoint_type, corr_value, wrong_value=None, wrong_id_value=None):

    """Adds correct/wrong/non-existent ids to the end of url"""

    url = base_url
    if endpoint_type == "correct":
        url += f'{corr_value}/'
    elif endpoint_type == "wrong":
        url += f'{wrong_value}/'
    elif endpoint_type == "wrong_id":
        url += f'{wrong_id_value}/'
    return url


@pytest.mark.parametrize(
    "user_type, endpoint_type, validity",
    [
        ('correct', 'list', 200),     # owner of saloon
        ('unauthenticated', 'list', 401),     # unauthenticated user
        ('wrong', 'list', 404),     # unauthenticated user
        ('correct', 'correct', 200),     # owner of saloon
        ('unauthenticated', 'correct', 401),     # unauthenticated user
        ('wrong', 'correct', 403),     # unauthenticated user
        ('correct', 'wrong', 404),  # wrong saloon_id
        ('unauthenticated', 'wrong', 401),  # wrong saloon_id
        ('wrong', 'wrong', 404),  # wrong saloon_id
        ('correct', 'wrong_id', 403),  # other saloon_id
        ('unauthenticated', 'wrong_id', 401),  # other saloon_id
        ('wrong', 'wrong_id', 403),  # other saloon_id
    ])
def test_cars_saloon_list_and_retrieve(client, setup_cars_saloon_list, user_type, endpoint_type, validity):
    saloon, wrong_user = setup_cars_saloon_list

    client = client_login(client, user_type, saloon.admin, wrong_user)

    base_url = 'http://localhost:8000/cars/autosaloon/'
    url = make_endpoint(base_url, endpoint_type, saloon.id, 999999999, saloon.id - 1)

    response = client.get(url)

    assert response.status_code == validity
    if validity == 200:
        response = response.json()
        assert response.get('count', 'No') == 'No'
        assert response['name'] == saloon.name
        assert response['admin']['id'] == saloon.admin.id


@pytest.mark.parametrize(
    "user_type, id_type, validity",
    [
        ('correct', 'correct', 200),  # admin of saloon
        ('correct', 'wrong', 404),  # admin, non-existent saloon
        ('correct', 'wrong_id', 403),  # admin, wrong saloon
        ('unauthenticated', 'correct', 401),
        ('unauthenticated', 'wrong', 401),
        ('unauthenticated', 'wrong_id', 401),
        ('wrong', 'correct', 403),  # wrong user
        ('wrong', 'wrong', 404),
        ('wrong', 'wrong_id', 403),
    ])
@pytest.mark.django_db
def test_cars_saloon_patch(client, setup_cars_saloon_patch, user_type, id_type, validity):
    saloon, wrong_user = setup_cars_saloon_patch
    admin = saloon.admin

    client_login(client, user_type, admin, wrong_user)

    base_url = f'http://localhost:8000/cars/autosaloon/'
    url = make_endpoint(base_url, id_type, saloon.id, 999999999, saloon.id + 1)

    data = {'name': 'new_name', 'is_active': False, 'country': 'AZ', "car_characteristics": {
        "origin": ["Europe"]}, "buyer_discounts": {"0": 1, "5": 1.1}, 'balance': 500, 'admin': 1}
    response = client.patch(url, data=data, format='json')

    assert response.status_code == validity
    if response.status_code == 200:
        saloon = AutoSaloon.objects.get(id=saloon.id)
        assert saloon.name == 'new_name'
        assert not saloon.is_active
        assert saloon.country == "AZ"
        assert saloon.car_characteristics == {"origin": ["Europe"]}
        assert saloon.buyer_discounts == {"0": 1, "5": 1.1}
        assert saloon.balance == 500000
        assert saloon.admin == admin


@pytest.mark.parametrize(
    "user_type, id_type, validity",
    [
        ('correct', 'correct', 204),  # admin of saloon
        ('correct', 'wrong', 404),  # admin, non-existent saloon
        ('unauthenticated', 'correct', 401),
        ('unauthenticated', 'wrong', 401),
        ('wrong', 'correct', 403),  # non-admin user
        ('wrong', 'wrong', 404),
    ])
@pytest.mark.django_db
def test_cars_saloon_delete(client, setup_cars_saloon_patch, user_type, id_type, validity):
    saloon, wrong_user = setup_cars_saloon_patch

    client_login(client, user_type, saloon.admin, wrong_user)

    base_url = f'http://localhost:8000/cars/autosaloon/'
    url = make_endpoint(base_url, id_type, saloon.id, 999999999, saloon.id + 1)

    response = client.delete(url)
    assert response.status_code == validity
    if response.status_code == 204:
        saloon = AutoSaloon.objects.get(id=saloon.id)
        assert not saloon.is_active


@pytest.mark.parametrize(
    "user_type, validity",
    [
        ('correct', 200),     # owner of saloon
        ('unauthenticated', 401),     # unauthenticated user
        ('wrong', 404),     # unauthenticated user
    ])
def test_cars_saloon_cars_list(client, setup_cars_saloon_cars_list, user_type, validity):
    saloon, wrong_user, saloon_car = setup_cars_saloon_cars_list

    client_login(client, user_type, saloon.admin, wrong_user)

    url = f'http://localhost:8000/cars/saloon_cars/'
    response = client.get(url)
    assert response.status_code == validity
    if response.status_code == 200:
        response = response.json()
        assert len(response) == 3
        assert response[0]['saloon']['name'] == 'C'


@pytest.mark.parametrize(
    "user_type, car_id, validity",
    [
        ('correct', 'correct', 200),     # owner of saloon
        ('unauthenticated', 'correct', 401),     # unauthenticated user
        ('wrong', 'correct', 403),     # wrong user
        ('correct', 'wrong', 404),  # owner of saloon, wrong car_id
        ('unauthenticated', 'wrong', 401),
        ('wrong', 'wrong', 404),
        ('correct', 'wrong_id', 403),  # owner of saloon, car_id of other saloon
        ('unauthenticated', 'wrong_id', 401),
        ('wrong', 'wrong_id', 403),
    ])
def test_cars_saloon_cars_retrieve(client, setup_cars_saloon_cars_list, user_type, car_id, validity):
    saloon, wrong_user, saloon_car = setup_cars_saloon_cars_list

    client_login(client, user_type, saloon.admin, wrong_user)

    base_url = f'http://localhost:8000/cars/saloon_cars/'
    url = make_endpoint(base_url, car_id, saloon_car.id, 999999999, saloon_car.id - 5)

    response = client.get(url)
    assert response.status_code == validity
    if response.status_code == 200:
        response = response.json()
        assert response['saloon']['name'] == 'C'
        assert response['car']['model_name'] == 'Z'


@pytest.mark.parametrize(
    "user_type, validity_response, validity_count",
    [
        ('correct', 204, 0),     # owner of saloon
        ('unauthenticated', 401, 1),     # unauthenticated user
        ('wrong', 403, 1)
    ])
def test_cars_saloon_cars_delete(client, setup_cars_saloon_cars_delete, user_type, validity_response, validity_count):
    admin_user, wrong_user, saloon_car = setup_cars_saloon_cars_delete

    client_login(client, user_type, admin_user, wrong_user)

    url = f'http://localhost:8000/cars/saloon_cars/{saloon_car.id}/'
    response = client.delete(url)
    assert response.status_code == validity_response
    assert SaloonCars.objects.filter(saloon=saloon_car.saloon).count() == validity_count


@pytest.mark.parametrize(
    "user_type, validity_response, validity_price, validity_quantity",
    [
        ('correct', 200, 10, 5),     # owner of saloon
        ('unauthenticated', 401, 15000, 1),     # unauthenticated user
        ('wrong', 403, 15000, 1)
    ])
@pytest.mark.django_db
def test_cars_saloon_cars_patch(client, setup_cars_saloon_cars_list, user_type, validity_response, validity_price, validity_quantity):
    saloon, wrong_user, saloon_car = setup_cars_saloon_cars_list

    client_login(client, user_type, saloon.admin, wrong_user)

    url = f'http://localhost:8000/cars/saloon_cars/{saloon_car.id}/'
    data = {'car_price': 10, 'quantity': 5}
    response = client.patch(url, data=data)
    assert response.status_code == validity_response

    saloon_car = SaloonCars.objects.get(id=saloon_car.id)
    assert saloon_car.car_price == validity_price
    assert saloon_car.quantity == validity_quantity


@pytest.mark.parametrize(
    "user_type, discount_type, valid_response",
    [
        ('correct', 'correct', 200),
        ('correct', 'wrong', 404),
        ('unauthorized', 'correct', 401),
        ('unauthorized', 'wrong', 401),
        ('wrong', 'correct', 403),
        ('wrong', 'wrong', 403),
    ])
@pytest.mark.django_db
def test_cars_saloon_cars_add_discount(client, setup_cars_saloon_cars_add_discount, user_type, discount_type, valid_response):
    admin_user, wrong_user, saloon_car, discount, wrong_discount = setup_cars_saloon_cars_add_discount

    client_login(client, user_type, admin_user, wrong_user)

    url = f'http://localhost:8000/cars/saloon_cars/{saloon_car.id}/add_discount/'
    if discount_type == 'correct':
        data = {'discounts': discount.id}
    else:
        data = {'discounts': wrong_discount.id}

    response = client.post(url, data=data)
    assert response.status_code == valid_response
    if response.status_code == 200:
        saloon_car = SaloonCars.objects.get(id=saloon_car.id)
        assert saloon_car.car_discount.first().id == discount.id


@pytest.mark.parametrize(
    "user_type, discount_type, valid_response, valid_count",
    [
        ('correct', 'correct', 200, 0),
        ('correct', 'wrong', 200, 1),
        ('unauthorized', 'correct', 401, 1),
        ('unauthorized', 'wrong', 401, 1),
        ('wrong', 'correct', 404, 1),
        ('wrong', 'wrong', 404, 1),
    ])
@pytest.mark.django_db
def test_cars_saloon_cars_remove_discount(client, setup_cars_saloon_cars_remove_discount, user_type, discount_type, valid_response, valid_count):
    admin_user, wrong_user, saloon_car, discount, wrong_discount = setup_cars_saloon_cars_remove_discount

    client_login(client, user_type, admin_user, wrong_user)

    base_url = f'http://localhost:8000/cars/saloon_cars/{saloon_car.id}/remove_discount/'
    url = make_endpoint(base_url, discount_type, discount.id, wrong_discount.id, wrong_discount.id)

    response = client.delete(url)
    assert response.status_code == valid_response
    saloon_car = SaloonCars.objects.get(id=saloon_car.id)
    assert saloon_car.car_discount.all().count() == valid_count


@pytest.mark.parametrize(
    "user_type, valid_response",
    [
        ('correct', 200),
        ('unauthorized', 401),
        ('wrong', 404),
    ])
def test_trading_saloon_discounts_list(client, setup_trading_saloon_discounts_list_retrieve, user_type, valid_response):
    admin, wrong_user, discount = setup_trading_saloon_discounts_list_retrieve
    client_login(client, user_type, admin, wrong_user)
    url = 'http://localhost:8000/trading/saloon_discounts/'
    response = client.get(url)
    assert response.status_code == valid_response
    if response.status_code == 200:
        response = response.json()
        assert len(response) == 1
        assert len(response[0]['discounted_offers']) == 1
        assert response[0]['seller']['name'] == discount.seller.name


@pytest.mark.parametrize(
    "user_type, id_type, valid_response",
    [
        ('correct', 'correct', 200),
        ('unauthorized', 'correct', 401),
        ('wrong', 'correct', 404),
        ('correct', 'wrong', 404),
        ('unauthorized', 'wrong', 401),
        ('wrong', 'wrong', 404),
        ('correct', 'wrong_id', 404),
        ('unauthorized', 'wrong_id', 401),
        ('wrong', 'wrong_id', 404),
    ])
def test_trading_saloon_discounts_retrieve(client, setup_trading_saloon_discounts_list_retrieve, user_type, id_type, valid_response):
    admin, wrong_user, discount = setup_trading_saloon_discounts_list_retrieve
    client_login(client, user_type, admin, wrong_user)
    base_url = 'http://localhost:8000/trading/saloon_discounts/'
    url = make_endpoint(base_url, id_type, discount.id, 999999, discount.id + 1)
    response = client.get(url)
    assert response.status_code == valid_response
    if response.status_code == 200:
        response = response.json()
        assert len(response['discounted_offers']) == 1
        assert response['seller']['name'] == discount.seller.name


@pytest.mark.parametrize(
    "user_type, data_type, valid_response",
    [
        ('correct', 'correct', 201),
        ('wrong', 'correct', 404),
        ('unauthorized', 'correct', 401),
        ('correct', 'wrong', 400),          # data won`t pass validation
    ])
@pytest.mark.django_db
def test_trading_saloon_discounts_post(client, setup_trading_saloon_discounts_post, user_type, data_type, valid_response):
    saloon, wrong_user, salooncar_rec = setup_trading_saloon_discounts_post
    client_login(client, user_type, saloon.admin, wrong_user)
    url = 'http://localhost:8000/trading/saloon_discounts/'
    start_time = datetime.datetime.now()
    if data_type == "correct":
        end_time = start_time + datetime.timedelta(days=5)
    else:
        end_time = start_time - datetime.timedelta(days=5)
    data = {'title': 'testtitle', 'description': 'testdescription', 'discount': 1.2,
            'start_time': start_time, 'end_time': end_time, 'discounted_offers': [salooncar_rec.id]
            }
    response = client.post(url, data=data)
    assert response.status_code == valid_response
    if response.status_code == 201:
        discount = SaloonDiscount.objects.last()
        assert discount.title == data['title']
        assert discount.description == data['description']
        assert list(discount.discounted_offers.all()) == [salooncar_rec]


@pytest.mark.parametrize(
    "user_type, valid_response, valid_status",
    [
        ('correct', 204, False),
        ('wrong', 403, True),
        ('unauthorized', 401, True),
    ])
def test_trading_saloon_discounts_delete(client, setup_trading_saloon_discounts_delete, user_type, valid_response, valid_status):
    admin, wrong_user, discount = setup_trading_saloon_discounts_delete
    client_login(client, user_type, admin, wrong_user)
    url = f'http://localhost:8000/trading/saloon_discounts/{discount.id}/'
    response = client.delete(url)
    print(response.status_code)
    assert response.status_code == valid_response
    assert SaloonDiscount.objects.get(id=discount.id).is_active == valid_status


@pytest.mark.parametrize(
    "user_type, valid_response, valid_status",
    [
        ('correct', 200, False),
        ('wrong', 403, True),
        ('unauthorized', 401, True),
    ])
def test_trading_saloon_discounts_patch(client, setup_trading_saloon_discounts_delete, user_type, valid_response, valid_status):
    admin, wrong_user, discount = setup_trading_saloon_discounts_delete
    url = f'http://localhost:8000/trading/saloon_discounts/{discount.id}/'
    client_login(client, user_type, admin, wrong_user)
    data = {'is_active': False, 'title': 'new_title', 'description': 'new_description', 'discount': 2}
    response = client.patch(url, data=data)
    assert response.status_code == valid_response
    if response.status_code == 200:
        discount = SaloonDiscount.objects.get(id=discount.id)
        assert discount.title == data['title']
        assert discount.description == data['description']
        assert discount.discount == data['discount']
        assert discount.is_active == valid_status
