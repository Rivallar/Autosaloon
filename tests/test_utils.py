from decimal import Decimal
import pytest

from cars.models import DealerCars
from cars.utils import apply_discount, find_best_dealer, find_cars_and_dealers
from trading.models import DealerToSaloonHistory

@pytest.mark.parametrize(
	"n_trades, validity",
	[
		(0, Decimal('10000')),
		(1, Decimal('10000')),
		(3, Decimal('9090.91')),
		(4, Decimal('9090.91')),
		(5, Decimal('8333.33')),		
	],)
@pytest.mark.django_db
def test_const_discount(const_discount_setup, dealertosaloonhistory_factory, n_trades, validity):
	
	car, saloon, dealer = const_discount_setup
	for _ in range(n_trades):
		history_rec = dealertosaloonhistory_factory(
			dealer = dealer,
			saloon = saloon,
			car = car)
	final_price = apply_discount(dealer, saloon, Decimal(10000))

	assert final_price == validity


@pytest.mark.parametrize(
	"n_records, validity",
	[
		(0, [Decimal(999999999999), '']),		# no dealer found
		(1, [Decimal('8000'), '']),				# dealer made discount
	],)
@pytest.mark.django_db
def test_find_best_dealer(best_dealer_setup, n_records, validity, dealercars_factory, dealer_factory, mocker):
	car, saloon = best_dealer_setup
	dealer_rec = ''
	for i in range(n_records):
		dealer_rec = dealercars_factory(
			dealer = dealer_factory(name=str(i)),
			car = car,
			car_price = Decimal(10000))
	if dealer_rec:
		validity[1] = dealer_rec.dealer
	mocker.patch("cars.utils.apply_discount", return_value=Decimal(8000))
	assert find_best_dealer(car, saloon) == validity


@pytest.mark.parametrize(
	"mock_value",
	[
		([Decimal(999999999999), '']),		# no dealer found
		([Decimal(999999999999), 'dealer']),		# dealer found
	],)
@pytest.mark.django_db
def test_find_cars_and_dealers(find_cars_and_dealers_setup, dealer_factory, mocker, mock_value):
	saloon, cars = find_cars_and_dealers_setup
	dealer_id, dealer_name = '', ''
	if mock_value[1]:
		mock_value[1] = dealer_factory()
		dealer_id = mock_value[1].id
		dealer_name = mock_value[1].name
	mocker.patch("cars.utils.find_best_dealer", return_value=mock_value)
	expected_result = {}
	for car in cars:
		expected_result[car.id] = {"car_model": car.model_name, "dealer_id": dealer_id, "dealer_name": dealer_name}
	assert find_cars_and_dealers(saloon) == expected_result
