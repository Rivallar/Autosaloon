import pytest


@pytest.fixture
def setup_stat_endpoints(db, user_factory, profile_factory, autosaloon_factory, dealer_factory):
    admin = user_factory()
    profile_factory(user=admin)
    autosaloon_factory(admin=admin)
    dealer_factory(admin=admin)
    return admin
