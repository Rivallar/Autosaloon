import pytest

from tests.endpoints.utils import set_admin


@pytest.fixture
def make_two_users(db, user_factory):
	admin = user_factory()
	wrong_user = user_factory(username="wrong")
	return admin, wrong_user


@pytest.fixture
def setup_dealer_list(db, make_two_users, dealer_factory):
	admin, wrong_user = make_two_users
	for i in 'ABC':
		dealer = dealer_factory(name=i)
	set_admin(admin, dealer)
	return dealer, wrong_user


@pytest.fixture
def setup_cars_dealer_patch(db, make_two_users, dealer_factory):
	admin, wrong_user = make_two_users
	dealer = dealer_factory()
	dealer_factory(name="wrong_dealer")
	set_admin(admin, dealer)
	return dealer, wrong_user


@pytest.fixture
def setup_cars_dealer_cars_list(db, make_two_users, auto_factory, dealer_factory, dealercars_factory):
	admin, wrong_user = make_two_users
	cars = [auto_factory(model_name=model) for model in 'XYZ']
	for name in 'ABC':
		dealer = dealer_factory(name=name)
		for car in cars:
			dealer_car = dealercars_factory(dealer=dealer, car=car)
	set_admin(admin, dealer)
	return dealer, wrong_user, dealer_car


@pytest.fixture
def setup_cars_dealer_cars_delete(db, make_two_users, dealercars_factory):
	admin, wrong_user = make_two_users
	dealer_car = dealercars_factory()
	dealer = dealer_car.dealer
	set_admin(admin, dealer)
	return admin, wrong_user, dealer_car


@pytest.fixture
def setup_cars_dealer_cars_add_discount(db, make_two_users, dealercars_factory, dealerdiscount_factory, dealer_factory):
	admin, wrong_user = make_two_users
	dealer_car = dealercars_factory()
	dealer = dealer_car.dealer
	set_admin(admin, dealer)
	discount = dealerdiscount_factory(seller=dealer)
	wrong_dealer = dealer_factory(name="wrong")
	wrong_discount = dealerdiscount_factory(seller=wrong_dealer)
	return admin, wrong_user, dealer_car, discount, wrong_discount


@pytest.fixture
def setup_cars_dealer_cars_remove_discount(db, make_two_users, dealerdiscount_factory, dealercars_factory):
	admin, wrong_user = make_two_users
	discount = dealerdiscount_factory()
	wrong_discount = dealerdiscount_factory(seller__name="wrong_saloon")
	dealer = discount.seller
	set_admin(admin, dealer)
	dealer_car = dealercars_factory(dealer=dealer)
	dealer_car.car_discount.add(discount.id)
	return admin, wrong_user, dealer_car, discount, wrong_discount


@pytest.fixture
def setup_trading_dealer_discounts_list_retrieve(db, dealer_factory, dealercars_factory, make_two_users, dealerdiscount_factory):
	dealer = dealer_factory(name='testdealer')
	dealercar_rec = dealercars_factory(dealer=dealer)

	admin, wrong_user = make_two_users
	set_admin(admin, dealer)

	discount = dealerdiscount_factory(seller=dealer)
	dealercar_rec.car_discount.add(discount.id)

	dealerdiscount_factory()

	return admin, wrong_user, discount


@pytest.fixture
def setup_trading_dealer_discounts_post(db, make_two_users, dealercars_factory):
	admin, wrong_user = make_two_users
	dealercar_rec = dealercars_factory()
	dealer = dealercar_rec.dealer
	set_admin(admin, dealer)
	return dealer, wrong_user, dealercar_rec


@pytest.fixture
def setup_trading_dealer_discounts_delete(db, make_two_users, dealerdiscount_factory):
	discount = dealerdiscount_factory()
	dealer = discount.seller
	admin, wrong_user = make_two_users
	set_admin(admin, dealer)
	return admin, wrong_user, discount
