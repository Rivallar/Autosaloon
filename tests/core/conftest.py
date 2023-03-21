import pytest


@pytest.fixture
def profile_and_car_for_offer(db, profile_factory, auto_factory):
	profile = profile_factory.create()
	car = auto_factory.create()
	return profile.id, car.id
