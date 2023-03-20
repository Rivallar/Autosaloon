import datetime
from decimal import Decimal
import time

import pytest

from cars.models import Auto
from tests.test_saloon_endpoints import client_login, make_endpoint
from trading.models import Profile, Offer


def test_cars_autos_list(client, setup_cars_autos):
    response = client.get('http://localhost:8000/cars/autos/')
    assert response.status_code == 200
    response = response.json()
    assert response['count'] == Auto.objects.all().count()


@pytest.mark.parametrize(
    "car_exist, validity",
    [
        (True, 200),     # existing car
        (False, 404)     # car_id is wrong
    ])
@pytest.mark.django_db
def test_cars_autos_retrieve(client, setup_cars_autos, car_exist, validity):
    if car_exist:
        car_id = setup_cars_autos
        car = Auto.objects.get(id=car_id)
        url = f'http://localhost:8000/cars/autos/{car_id}/'
    else:
        url = f'http://localhost:8000/cars/autos/9999999999/'
    response = client.get(url, format='json')
    assert response.status_code == validity
    if car_exist:
        response = response.json()
        assert car.model_name == response['model_name']


@pytest.mark.parametrize(
    "user_type, id_type, validity",
    [
        ('correct', 'list', 200),
        ('wrong', 'list', 404),
        ('unauthorized', 'list', 401),
        ('correct', 'correct', 200),
        ('wrong', 'correct', 404),
        ('unauthorized', 'correct', 401),
        ('correct', 'wrong', 404),
        ('wrong', 'wrong', 404),
        ('unauthorized', 'wrong', 401),
        ('correct', 'wrong_id', 404),
        ('wrong', 'wrong_id', 404),
        ('unauthorized', 'wrong_id', 401),
    ])
def test_trading_profile_list_retieve(client, setup_trading_profile_list, user_type, id_type, validity):
    profile, wrong_profile, no_profile_user = setup_trading_profile_list
    client_login(client, user_type, profile.user, no_profile_user)
    url = 'http://localhost:8000/trading/my_profile/'
    url = make_endpoint(url, id_type, profile.id, wrong_profile.id, 99999)
    response = client.get(url)
    assert response.status_code == validity
    if response.status_code == 200:
        response = response.json()
        assert response['id'] == profile.id
        assert response['user'] == profile.user.id


@pytest.mark.parametrize(
    "user_type, data, validity",
    [
        ('correct', {'phone': 777, 'birth_date': datetime.date.today()}, 201),
        ('unauthorized', {'phone': 777, 'birth_date': datetime.date.today()}, 401),
        ('wrong', {'phone': 777, 'birth_date': datetime.date.today()}, 400),
        ('correct', {}, 201),
        ('correct', {'balance': 50000}, 201),
    ])
def test_trading_profile_post(client, setup_trading_profile_post, user_type, data, validity):
    no_profile_user, profile = setup_trading_profile_post
    client_login(client, user_type, no_profile_user, profile.user)
    url = 'http://localhost:8000/trading/my_profile/'
    data = data
    response = client.post(url, data=data)
    print(response.status_code)
    assert response.status_code == validity
    if response.status_code == 201:
        response = response.json()
        assert Profile.objects.first()
        assert response['phone'] == data.get('phone')
        assert response['balance'] == '0.00'


@pytest.mark.parametrize(
    "user_type, id_type, validity",
    [
        ('correct', 'correct', 200),
        ('correct', 'wrong', 404),
        ('correct', 'wrong_id', 404),
        ('unauthorized', 'correct', 401),
        ('unauthorized', 'wrong', 401),
        ('unauthorized', 'wrong_id', 401),
        ('wrong', 'correct', 404),
        ('wrong', 'wrong_id', 404),
    ])
def test_trading_profile_patch(client, setup_trading_profile_list, user_type, id_type, validity):
    profile, wrong_profile, no_profile_user = setup_trading_profile_list
    client_login(client, user_type, profile.user, wrong_profile.user)

    base_url = 'http://localhost:8000/trading/my_profile/'
    url = make_endpoint(base_url, id_type, profile.id, wrong_profile.id, 99999)

    data = {'phone': 777, 'birth_date': datetime.date.today()}
    response = client.patch(url, data=data)
    assert response.status_code == validity
    if response.status_code == 200:
        profile = Profile.objects.get(id=profile.id)
        assert profile.phone == data['phone']
        assert profile.birth_date == data['birth_date']
        assert profile.balance == Decimal(30000)


@pytest.mark.parametrize(
    "user_type, offer_price, car_type, validity",
    [
        ('correct', Decimal(20000), 'correct', 201),    # all is ok
        #('correct', Decimal(20000), 'wrong', 400),      # car does not exist
        #('correct', Decimal(40000), 'correct', 400),    # profile balance lower then offer price
        #('unauthorized', Decimal(20000), 'correct', 401),   # unauthorized user
        #('wrong', Decimal(20000), 'correct', 404),  # a user without a profile
    ])
def test_trading_make_offer(client, setup_trading_make_offer, user_type, offer_price, car_type, validity):
    profile, record, no_profile_user = setup_trading_make_offer
    client_login(client, user_type, profile.user, no_profile_user)
    url = 'http://localhost:8000/trading/make_offer/'
    data = {'max_price': offer_price, 'car_model': record.car.id}
    if car_type == "wrong":
        data['car_model'] += 1
    response = client.post(url, data=data)
    print(response.status_code)
    assert response.status_code == validity
    if response.status_code == 201:
        offer = Offer.objects.last()

        assert offer.is_active == False
