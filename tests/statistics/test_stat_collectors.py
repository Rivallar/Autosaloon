from decimal import Decimal
import pytest

from statistics_app.stat_collectors import get_aggregated_stat, get_profile_stat, get_dealer_stat, get_saloon_stat
from trading.models import SaloonToBuyerHistory


@pytest.mark.parametrize(
    "prof_type, validity",
    [
        ("with_hist", [6, Decimal(100000), Decimal(50000)]),    # profile with deals
        ("no_hist", [0, 0, 0]),                                 # profile with no deals
    ],)
def test_get_aggregated_stat(setup_get_aggregated_stat, prof_type, validity):
    prof, empty_prof = setup_get_aggregated_stat
    prof_id = prof.id if prof_type == 'with_hist' else empty_prof.id
    q = SaloonToBuyerHistory.objects.filter(profile=prof_id)
    count, total, maximum = get_aggregated_stat(q)
    assert count == validity[0]
    assert total == validity[1]
    assert maximum == validity[2]


@pytest.mark.parametrize(
    "prof_type, validity",
    [
        ("with_hist", ['A', 'B', 'C', 'D', 'E', 'expensive_car']),    # profile with deals
        ("no_hist", []),                                 # profile with no deals
    ],)
def test_get_profile_stat(setup_get_aggregated_stat, mocker, prof_type, validity):
    prof, empty_prof = setup_get_aggregated_stat
    mocker.patch("statistics_app.stat_collectors.get_aggregated_stat", return_value=[6, Decimal(100000), Decimal(50000)])
    expected_data = {'cars_amount': 6, 'money_spent': '100000.00', 'max_price': '50000.00',
                     'car_models_bought': validity}
    prof_id = prof.id if prof_type == 'with_hist' else empty_prof.id
    result = get_profile_stat(prof_id)
    assert result.data == expected_data


@pytest.mark.parametrize(
    "prof_type, validity_top_saloons, validity_top_cars",
    [
        ("with_hist",
         [{'saloon__name': 'A', 'amount': 4}, {'saloon__name': 'B', 'amount': 3}, {'saloon__name': 'C', 'amount': 3}],
         [{'car__model_name': 'Z', 'amount': 4}, {'car__model_name': 'C', 'amount': 3}, {'car__model_name': 'X', 'amount': 3}]),    # profile with deals
        ("no_hist", [], []),                                 # profile with no deals
    ],)
def test_get_dealer_stat(setup_get_dealer_stat, mocker, prof_type, validity_top_saloons, validity_top_cars):
    dealer, empty_dealer = setup_get_dealer_stat
    mocker.patch("statistics_app.stat_collectors.get_aggregated_stat",
                 return_value=[6, Decimal(100000), Decimal(50000)])
    dealer_id = dealer.id if prof_type == "with_hist" else empty_dealer.id
    result = get_dealer_stat(dealer_id)
    exp_top_saloons = validity_top_saloons
    exp_top_cars = validity_top_cars
    exp_result = {'n_cars_sold': 6, 'money_earned': '100000.00', 'max_deal': '50000.00',
                  'top_saloons': exp_top_saloons, 'top_cars': exp_top_cars}
    assert result.data == exp_result


@pytest.mark.parametrize(
    "prof_type, validity_money_diff, validity_top_cars, validity_top_buyers, validity_top_dealers",
    [
        ("with_hist", '0.00',
            [{'car__model_name': 'Z', 'amount': 4}, {'car__model_name': 'C', 'amount': 3}, {'car__model_name': 'X', 'amount': 3}],
            [{'profile__user__username': 'A', 'cars_bought': 4}, {'profile__user__username': 'D', 'cars_bought': 3}, {'profile__user__username': 'S', 'cars_bought': 3}],
            [{'dealer__name': 'Q', 'cars_bought': 4}, {'dealer__name': 'E', 'cars_bought': 3}, {'dealer__name': 'W', 'cars_bought': 3}]),
        ("no_hist", '100000.00', [], [], []),
    ],)
def test_get_saloon_stat(setup_get_saloon_stat, mocker, prof_type, validity_money_diff, validity_top_cars, validity_top_buyers, validity_top_dealers):
    saloon, no_hist_saloon = setup_get_saloon_stat
    mocker.patch("statistics_app.stat_collectors.get_aggregated_stat",
                 return_value=[6, Decimal(100000), Decimal(50000)])
    saloon_id = saloon.id if prof_type == "with_hist" else no_hist_saloon.id
    result = get_saloon_stat(saloon_id)

    assert result.data['money_diff'] == validity_money_diff
    assert result.data['top_cars_sold'] == validity_top_cars
    assert result.data['top_buyers'] == validity_top_buyers
    assert result.data['top_dealers'] == validity_top_dealers
