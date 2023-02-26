import pytest
import datetime 

from cars.models import Dealer

def test_that_works():
	assert 1 == 1

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
	
