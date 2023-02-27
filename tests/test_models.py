import pytest
import datetime
from decimal import Decimal

from cars.models import Dealer
from trading.forms import OfferForm


@pytest.mark.django_db
def test_softdelete():
	dealer_count = Dealer.objects.all().count()
	dealer = Dealer.objects.create(name='name', foundation_date=datetime.datetime.today())
	dealer.delete()
	assert Dealer.objects.all().count() == dealer_count + 1
	

@pytest.mark.django_db
def test_harddelete():
	dealer_count = Dealer.objects.all().count()
	dealer = Dealer.objects.create(name='name', foundation_date=datetime.datetime.today())
	dealer.delete(is_soft=False)
	assert Dealer.objects.all().count() == dealer_count


@pytest.mark.parametrize(
	"max_price, validity",
	[
		(Decimal(25000), True),     # max_price lower than profile balance
		(Decimal(35000), False)     # max_price higher than profile balance
	])
@pytest.mark.django_db
def test_offer(profile_and_car_for_offer, max_price, validity):
	profile_id, car_id = profile_and_car_for_offer
	form = OfferForm(data={
		"profile": profile_id,
		"max_price": max_price,
		"car_model": car_id
	})
	assert form.is_valid() == validity
	
