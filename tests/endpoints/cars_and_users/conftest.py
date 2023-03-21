import pytest

from autosaloon.celery import app


@pytest.fixture
def setup_cars_autos(db, auto_factory):
    for i in 'ABC':
        car = auto_factory(model_name=i)
    return car.id


@pytest.fixture
def setup_trading_profile_list(db, user_factory, profile_factory):
    no_profile_user = user_factory(username="no_profile")
    profile = profile_factory()
    wrong_profile = profile_factory(user__username='wrong_user')
    return profile, wrong_profile, no_profile_user


@pytest.fixture
def setup_trading_profile_post(db, user_factory, profile_factory):
    no_profile_user = user_factory(username="no_profile")
    profile = profile_factory()
    return no_profile_user, profile


@pytest.fixture(scope='module')
def celery_app(request):
    app.conf.update(CELERY_ALWAYS_EAGER=True)
    return app


@pytest.fixture
def setup_trading_make_offer(db, profile_factory, salooncars_factory, user_factory):
    profile = profile_factory()
    no_profile_user = user_factory(username="no_profile")
    record = salooncars_factory()
    return profile, record, no_profile_user

