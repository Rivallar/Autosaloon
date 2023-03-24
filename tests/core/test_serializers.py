from decimal import Decimal
import pytest

from statistics_app.serializers import ProfileStatisticsSerializer


@pytest.mark.parametrize(
    "input_data, if_valid, error_field",
    [
        ({'car_models_bought': [], 'cars_amount': 0, 'money_spent': Decimal(50000), 'max_price': Decimal(25000)}, True, ''),        # ok
        ({'car_models_bought': [], 'cars_amount': -1, 'money_spent': Decimal(50000), 'max_price': Decimal(25000)}, False, 'cars_amount'),   # < 0
        ({'car_models_bought': 'abc', 'cars_amount': 0, 'money_spent': Decimal(50000), 'max_price': Decimal(25000)}, False, 'car_models_bought'),   # not a list
        ({'car_models_bought': [], 'cars_amount': 0, 'money_spent': Decimal(500000000000000000), 'max_price': Decimal(25000)}, False, 'money_spent'),   # to many digits
    ])
def test_serializer(input_data, if_valid, error_field):
    data = input_data
    serializer = ProfileStatisticsSerializer(data=data)
    assert serializer.is_valid() == if_valid
    if not if_valid:
        assert serializer.errors[error_field]

