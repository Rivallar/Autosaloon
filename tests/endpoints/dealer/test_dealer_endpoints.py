import datetime

import pytest

from cars.models import Dealer, DealerCars
from tests.endpoints.utils import client_login, make_endpoint
from trading.models import DealerDiscount

pytestmark = pytest.mark.django_db


class TestDealer:

    base_url = 'http://localhost:8000/cars/dealer/'

    @pytest.mark.parametrize(
        "user_type, endpoint_type, validity",
        [
            ('correct', 'list', 200),  # owner of dealer
            ('unauthenticated', 'list', 401),  # unauthenticated user
            ('wrong', 'list', 404),  # wrong user
            ('correct', 'correct', 200),  # correct retrieve
            ('unauthenticated', 'correct', 401),
            ('wrong', 'correct', 403),
            ('correct', 'wrong', 404),  # wrong dealer_id
            ('unauthenticated', 'wrong', 401),
            ('wrong', 'wrong', 404),
            ('correct', 'wrong_id', 403),  # other dealer_id
            ('unauthenticated', 'wrong_id', 401),
            ('wrong', 'wrong_id', 403),
        ])
    def test_cars_dealer_list_retrieve(self, client, setup_dealer_list, user_type, endpoint_type, validity):
        dealer, wrong_user = setup_dealer_list
        client = client_login(client, user_type, dealer.admin, wrong_user)
        url = make_endpoint(self.base_url, endpoint_type, dealer.id, 999999999, dealer.id - 1)

        response = client.get(url)

        assert response.status_code == validity
        if validity == 200:
            response = response.json()
            assert response.get('count', 'No') == 'No'
            assert response['name'] == dealer.name
            assert response['admin']['id'] == dealer.admin.id

    @pytest.mark.parametrize(
        "user_type, id_type, validity",
        [
            ('correct', 'correct', 200),  # admin of dealer
            ('correct', 'wrong', 404),  # admin, non-existent dealer
            ('correct', 'wrong_id', 403),  # admin, wrong dealer
            ('unauthenticated', 'correct', 401),
            ('unauthenticated', 'wrong', 401),
            ('unauthenticated', 'wrong_id', 401),
            ('wrong', 'correct', 403),  # wrong user
            ('wrong', 'wrong', 404),
            ('wrong', 'wrong_id', 403),
        ])
    def test_cars_dealer_patch(self, client, setup_cars_dealer_patch, user_type, id_type, validity):
        dealer, wrong_user = setup_cars_dealer_patch
        admin = dealer.admin

        client_login(client, user_type, admin, wrong_user)

        url = make_endpoint(self.base_url, id_type, dealer.id, 999999999, dealer.id + 1)

        found_date = datetime.date.today()
        data = {'name': 'new_name', 'is_active': False, 'about': 'bla-bla', "buyer_discounts": {"0": 1, "5": 1.1},
                'foundation_date': found_date, 'admin': 1}
        response = client.patch(url, data=data, format='json')

        assert response.status_code == validity
        if response.status_code == 200:
            dealer = Dealer.objects.get(id=dealer.id)
            assert dealer.name == 'new_name'
            assert not dealer.is_active
            assert dealer.about == data['about']
            assert dealer.buyer_discounts == data['buyer_discounts']
            assert dealer.foundation_date == data['foundation_date']
            assert dealer.admin == admin

    @pytest.mark.parametrize(
        "user_type, id_type, validity",
        [
            ('correct', 'correct', 204),  # admin of dealer
            ('correct', 'wrong', 404),  # admin, non-existent dealer
            ('unauthenticated', 'correct', 401),
            ('unauthenticated', 'wrong', 401),
            ('wrong', 'correct', 403),  # non-admin user
            ('wrong', 'wrong', 404),
        ])
    def test_cars_dealer_delete(self, client, setup_cars_dealer_patch, user_type, id_type, validity):
        dealer, wrong_user = setup_cars_dealer_patch

        client_login(client, user_type, dealer.admin, wrong_user)
        url = make_endpoint(self.base_url, id_type, dealer.id, 999999999, dealer.id + 1)

        response = client.delete(url)
        assert response.status_code == validity
        if response.status_code == 204:
            saloon = Dealer.objects.get(id=dealer.id)
            assert not saloon.is_active


class TestDealerCars:

    base_url = f'http://localhost:8000/cars/dealer_cars/'

    @pytest.mark.parametrize(
        "user_type, validity",
        [
            ('correct', 200),  # admin of dealer
            ('unauthenticated', 401),  # unauthenticated user
            ('wrong', 404),  # wrong user
        ])
    def test_cars_dealer_cars_list(self, client, setup_cars_dealer_cars_list, user_type, validity):
        dealer, wrong_user, dealer_car = setup_cars_dealer_cars_list
        client_login(client, user_type, dealer.admin, wrong_user)

        response = client.get(self.base_url)
        assert response.status_code == validity
        if response.status_code == 200:
            response = response.json()
            assert len(response) == 3
            assert response[0]['dealer']['name'] == 'C'

    @pytest.mark.parametrize(
        "user_type, car_id, validity",
        [
            ('correct', 'correct', 200),  # admin of dealer
            ('unauthenticated', 'correct', 401),  # unauthenticated user
            ('wrong', 'correct', 403),  # wrong user
            ('correct', 'wrong', 404),  # admin of dealer, wrong car_id
            ('unauthenticated', 'wrong', 401),
            ('wrong', 'wrong', 404),
            ('correct', 'wrong_id', 403),  # admin of dealer, car_id of other dealer
            ('unauthenticated', 'wrong_id', 401),
            ('wrong', 'wrong_id', 403),
        ])
    def test_cars_dealer_cars_retrieve(self, client, setup_cars_dealer_cars_list, user_type, car_id, validity):
        dealer, wrong_user, dealer_car = setup_cars_dealer_cars_list

        client_login(client, user_type, dealer.admin, wrong_user)
        url = make_endpoint(self.base_url, car_id, dealer_car.id, 999999999, dealer_car.id - 5)

        response = client.get(url)
        assert response.status_code == validity
        if response.status_code == 200:
            response = response.json()
            assert response['dealer']['name'] == 'C'
            assert response['car']['model_name'] == 'Z'

    @pytest.mark.parametrize(
        "user_type, validity_response, validity_count",
        [
            ('correct', 204, 0),  # admin of dealer
            ('unauthenticated', 401, 1),  # unauthenticated user
            ('wrong', 403, 1)
        ])
    def test_cars_dealer_cars_delete(self, client, setup_cars_dealer_cars_delete, user_type, validity_response,
                                     validity_count):
        admin, wrong_user, dealer_car = setup_cars_dealer_cars_delete
        client_login(client, user_type, admin, wrong_user)
        url = self.base_url + f'{dealer_car.id}/'
        response = client.delete(url)
        assert response.status_code == validity_response
        assert DealerCars.objects.filter(dealer=dealer_car.dealer).count() == validity_count

    @pytest.mark.parametrize(
        "user_type, validity_response, validity_price",
        [
            ('correct', 200, 10),  # admin of dealer
            ('unauthenticated', 401, 12000),     # unauthenticated user
            ('wrong', 403, 12000)       # wrong user
        ])
    def test_cars_dealer_cars_patch(self, client, setup_cars_dealer_cars_list, user_type, validity_response, validity_price):
        dealer, wrong_user, dealer_car = setup_cars_dealer_cars_list
        client_login(client, user_type, dealer.admin, wrong_user)

        url = self.base_url + f'{dealer_car.id}/'
        data = {'car_price': 10}
        response = client.patch(url, data=data)
        assert response.status_code == validity_response

        dealer_car = DealerCars.objects.get(id=dealer_car.id)
        assert dealer_car.car_price == validity_price

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
    def test_cars_dealer_cars_add_discount(self, client, setup_cars_dealer_cars_add_discount, user_type, discount_type,
                                           valid_response):
        admin, wrong_user, dealer_car, discount, wrong_discount = setup_cars_dealer_cars_add_discount
        client_login(client, user_type, admin, wrong_user)

        url = f'{self.base_url}{dealer_car.id}/add_discount/'
        if discount_type == 'correct':
            data = {'discounts': discount.id}
        else:
            data = {'discounts': wrong_discount.id}

        response = client.post(url, data=data)
        assert response.status_code == valid_response
        if response.status_code == 200:
            dealer_car = DealerCars.objects.get(id=dealer_car.id)
            assert dealer_car.car_discount.first().id == discount.id

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
    def test_cars_dealer_cars_remove_discount(self, client, setup_cars_dealer_cars_remove_discount, user_type, discount_type,
                                              valid_response, valid_count):
        admin, wrong_user, dealer_car, discount, wrong_discount = setup_cars_dealer_cars_remove_discount
        client_login(client, user_type, admin, wrong_user)

        base_url = f'{self.base_url}{dealer_car.id}/remove_discount/'
        url = make_endpoint(base_url, discount_type, discount.id, 99999999, wrong_discount.id)

        response = client.delete(url)
        assert response.status_code == valid_response
        dealer_car = DealerCars.objects.get(id=dealer_car.id)
        assert dealer_car.car_discount.all().count() == valid_count


class TestDealerDiscounts:

    base_url = 'http://localhost:8000/trading/dealer_discounts/'

    @pytest.mark.parametrize(
        "user_type, valid_response",
        [
            ('correct', 200),
            ('unauthorized', 401),
            ('wrong', 404),
        ])
    def test_trading_dealer_discounts_list(self, client, setup_trading_dealer_discounts_list_retrieve, user_type,
                                           valid_response):
        admin, wrong_user, discount = setup_trading_dealer_discounts_list_retrieve
        client_login(client, user_type, admin, wrong_user)
        response = client.get(self.base_url)
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
    def test_trading_dealer_discounts_retrieve(self, client, setup_trading_dealer_discounts_list_retrieve, user_type, id_type,
                                               valid_response):
        admin, wrong_user, discount = setup_trading_dealer_discounts_list_retrieve
        client_login(client, user_type, admin, wrong_user)
        url = make_endpoint(self.base_url, id_type, discount.id, 999999, discount.id + 1)
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
            ('correct', 'wrong', 400),  # data won`t pass validation
        ])
    @pytest.mark.django_db
    def test_trading_dealer_discounts_post(self, client, setup_trading_dealer_discounts_post, user_type, data_type,
                                           valid_response):
        dealer, wrong_user, dealercar_rec = setup_trading_dealer_discounts_post
        client_login(client, user_type, dealer.admin, wrong_user)
        start_time = datetime.datetime.now()
        if data_type == "correct":
            end_time = start_time + datetime.timedelta(days=5)
        else:
            end_time = start_time - datetime.timedelta(days=5)
        data = {'title': 'testtitle', 'description': 'testdescription', 'discount': 1.2,
                'start_time': start_time, 'end_time': end_time, 'discounted_offers': [dealercar_rec.id]
                }
        response = client.post(self.base_url, data=data)
        assert response.status_code == valid_response
        if response.status_code == 201:
            discount = DealerDiscount.objects.last()
            assert discount.title == data['title']
            assert discount.description == data['description']
            assert list(discount.discounted_offers.all()) == [dealercar_rec]

    @pytest.mark.parametrize(
        "user_type, valid_response, valid_status",
        [
            ('correct', 204, False),
            ('wrong', 403, True),
            ('unauthorized', 401, True),
        ])
    def test_trading_saloon_discounts_delete(self, client, setup_trading_dealer_discounts_delete, user_type, valid_response,
                                             valid_status):
        admin, wrong_user, discount = setup_trading_dealer_discounts_delete
        client_login(client, user_type, admin, wrong_user)
        url = f'{self.base_url}{discount.id}/'
        response = client.delete(url)
        assert response.status_code == valid_response
        assert DealerDiscount.objects.get(id=discount.id).is_active == valid_status

    @pytest.mark.parametrize(
        "user_type, valid_response, valid_status",
        [
            ('correct', 200, False),
            ('wrong', 403, True),
            ('unauthorized', 401, True),
        ])
    def test_trading_saloon_discounts_patch(self, client, setup_trading_dealer_discounts_delete, user_type, valid_response,
                                            valid_status):
        admin, wrong_user, discount = setup_trading_dealer_discounts_delete
        url = f'{self.base_url}{discount.id}/'
        client_login(client, user_type, admin, wrong_user)
        data = {'is_active': False, 'title': 'new_title', 'description': 'new_description', 'discount': 2}
        response = client.patch(url, data=data)
        assert response.status_code == valid_response
        if response.status_code == 200:
            discount = DealerDiscount.objects.get(id=discount.id)
            assert discount.title == data['title']
            assert discount.description == data['description']
            assert discount.discount == data['discount']
            assert discount.is_active == valid_status