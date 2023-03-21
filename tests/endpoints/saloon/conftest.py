import pytest


@pytest.fixture
def setup_cars_saloon_list(db, user_factory, autosaloon_factory):
	user = user_factory()
	wrong_user = user_factory(username="wrong")
	for i in 'ABC':
		saloon = autosaloon_factory(name=i)
	saloon.admin = user
	saloon.save()
	return saloon, wrong_user

@pytest.fixture
def setup_cars_saloon_patch(db, user_factory, autosaloon_factory):
	user = user_factory()
	wrong_user = user_factory(username="wrong")
	saloon = autosaloon_factory()
	autosaloon_factory(name="wrong_saloon")
	saloon.admin = user
	saloon.save()
	return saloon, wrong_user


@pytest.fixture
def setup_cars_saloon_cars_list(db, user_factory, auto_factory, autosaloon_factory, salooncars_factory):
	admin_user = user_factory()
	wrong_user = user_factory(username="wrong")
	cars = [auto_factory(model_name=model) for model in 'XYZ']
	for name in 'ABC':
		saloon = autosaloon_factory(name=name)
		for car in cars:
			saloon_car = salooncars_factory(saloon=saloon, car=car)
	saloon.admin = admin_user
	saloon.save()
	return saloon, wrong_user, saloon_car


@pytest.fixture
def setup_cars_saloon_cars_delete(db, user_factory, salooncars_factory):
	admin_user = user_factory()
	wrong_user = user_factory(username="wrong")
	saloon_car = salooncars_factory()
	saloon = saloon_car.saloon
	saloon.admin = admin_user
	saloon.save()
	return admin_user, wrong_user, saloon_car


@pytest.fixture
def setup_cars_saloon_cars_add_discount(db, user_factory, salooncars_factory, saloondiscount_factory, autosaloon_factory):
	admin_user = user_factory()
	wrong_user = user_factory(username="wrong")
	saloon_car = salooncars_factory()
	saloon = saloon_car.saloon
	saloon.admin = admin_user
	saloon.save()
	discount = saloondiscount_factory(seller=saloon)
	wrong_saloon = autosaloon_factory(name="wrong")
	wrong_discount = saloondiscount_factory(seller=wrong_saloon)
	return admin_user, wrong_user, saloon_car, discount, wrong_discount


@pytest.fixture
def setup_cars_saloon_cars_remove_discount(db, user_factory, saloondiscount_factory, salooncars_factory):
	admin_user = user_factory()
	wrong_user = user_factory(username="wrong_user")
	discount = saloondiscount_factory()
	wrong_discount = saloondiscount_factory(seller__name="wrong_saloon")
	saloon = discount.seller
	saloon.admin = admin_user
	saloon.save()
	saloon_car = salooncars_factory(saloon=saloon)
	saloon_car.car_discount.add(discount.id)
	return admin_user, wrong_user, saloon_car, discount, wrong_discount


@pytest.fixture
def setup_trading_saloon_discounts_list_retrieve(db, autosaloon_factory, salooncars_factory, user_factory, saloondiscount_factory):
	saloon = autosaloon_factory(name='testsaloon')
	salooncar_rec = salooncars_factory(saloon=saloon)

	admin = user_factory()
	wrong_user = user_factory(username="wrong_user")
	saloon.admin = admin
	saloon.save()

	discount = saloondiscount_factory(seller=saloon)
	salooncar_rec.car_discount.add(discount.id)

	saloondiscount_factory()

	return admin, wrong_user, discount


@pytest.fixture
def setup_trading_saloon_discounts_post(db, user_factory, salooncars_factory):
	admin = user_factory(username='saloon_admin')
	wrong_user = user_factory()
	salooncar_rec = salooncars_factory()
	saloon = salooncar_rec.saloon
	saloon.admin = admin
	saloon.save()
	return saloon, wrong_user, salooncar_rec


@pytest.fixture
def setup_trading_saloon_discounts_delete(db, user_factory, saloondiscount_factory):
	discount = saloondiscount_factory()
	saloon = discount.seller
	admin = user_factory(username='saloon_admin')
	wrong_user = user_factory()
	saloon.admin = admin
	saloon.save()
	return admin, wrong_user, discount