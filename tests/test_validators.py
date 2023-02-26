import pytest

from decimal import Decimal

from trading.forms import AutoSaloonForm


@pytest.mark.parametrize(
    "name, country, city, address, car_characteristics, balance, validity",
    [
        ("test_saloon", 'AF', 'Minsk', 'abc', {'origin': ["Europe"]}, Decimal(500), True),     # correct
        ("test_saloon", 'AF', 'Minsk', 'abc', {'origin': ["Europe"], 'wrong': 1}, Decimal(500), False),     # wrong key
        ("test_saloon",'AF', 'Minsk', 'abc', {'fuel': ["gas", "atomic"]}, Decimal(500), False),      # wrong value
        ("test_saloon", 'AF', 'Minsk', 'abc', {'origin': "Europe"}, Decimal(500), False),       # value not a list
        ("test_saloon", 'AF', 'Minsk', 'abc',
            {'origin': ["Europe", "Asia"], 'fuel': ["gas", "hybrid"], 'frame': ["sedan", "bus"], 'segment': ['A', 'B', 'C']},
            Decimal(500), True),       # correct test with every option
    ],
)
def test_car_characteristics_validator(name, country, city, address, car_characteristics, balance, validity):

    form = AutoSaloonForm(data={
        "name": name,
        "country": country,
        "city": city,
        "address": address,
        "car_characteristics": car_characteristics,
        "balance": balance})

    assert form.is_valid() is validity


@pytest.mark.parametrize(
    "name, country, city, address, car_characteristics, balance, buyer_discounts, validity",
    [
        ("saloon", 'AF', 'Minsk', 'abc', {'segment': ["A"]}, Decimal(500), '', True),     # blank
        ("saloon", 'AF', 'Minsk', 'abc', {'segment': ["A"]}, Decimal(500), 'x', False),     # not a dict
        ("saloon", 'AF', 'Minsk', 'abc', {'segment': ["A"]}, Decimal(500), {'3': 1, 'x': 1}, False),     # wrong key
        ("saloon", 'AF', 'Minsk', 'abc', {'segment': ["A"]}, Decimal(500), {'3': 1, '-3': 1}, False),     # wrong key
        ("saloon", 'AF', 'Minsk', 'abc', {'segment': ["A"]}, Decimal(500), {'3': 1, '3.5': 1}, False),  # wrong key
        ("saloon", 'AF', 'Minsk', 'abc', {'segment': ["A"]}, Decimal(500), {'3': 'x'}, False),  # wrong value
        ("saloon", 'AF', 'Minsk', 'abc', {'segment': ["A"]}, Decimal(500), {'3': 0}, False),  # wrong value
        ("saloon", 'AF', 'Minsk', 'abc', {'segment': ["A"]}, Decimal(500), {'0': 1, '5': 1.15}, True),  # all is ok
    ],
)
def test_discount_validator(name, country, city, address, car_characteristics, balance, buyer_discounts, validity):

    form = AutoSaloonForm(data={
        "name": name,
        "country": country,
        "city": city,
        "address": address,
        "car_characteristics": car_characteristics,
        'buyer_discounts': buyer_discounts,
        "balance": balance})

    assert form.is_valid() is validity
