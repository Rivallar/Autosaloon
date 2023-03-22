from django.db.models import Count

from trading.models import SaloonToBuyerHistory, DealerToSaloonHistory
from statistics_app.serializers import AutoSaloonStatisticsSerializer, DealerStatisticsSerializer, ProfileStatisticsSerializer


def get_profile_stat(profile_id):

    db_data = SaloonToBuyerHistory.objects.filter(profile=profile_id).prefetch_related('car').\
        values_list('car__model_name', 'deal_price')

    # Aggregation sum deal_price
    # max price
    # count
    car_models_bought = set()
    cars_amount = 0
    money_spent = 0
    max_price = 0
    for item in db_data:
        cars_amount += 1
        car_models_bought.add(item[0])
        price = item[1]
        money_spent += price
        if price > max_price:
            max_price = price

    data = {'car_models_bought': car_models_bought, 'cars_amount': cars_amount, 'money_spent': money_spent,
            'max_price': max_price}

    serializer = ProfileStatisticsSerializer(data=data)
    if serializer.is_valid():
        return serializer


def get_dealer_stat(dealer_id):
    base_query = DealerToSaloonHistory.objects.filter(dealer=dealer_id)

    deals = base_query.values_list('deal_price', flat=True)
    n_cars_sold = len(deals) # count
    money_earned = sum(deals)
    max_deal = max(deals)

    top_saloons = base_query.prefetch_related('saloon').values('saloon__name').annotate(
        amount=Count('saloon')).order_by('-amount')[:10]
    top_cars = base_query.prefetch_related('car').values('car__model_name').annotate(amount=Count('car')).order_by('-amount')[:10]

    data = {'n_cars_sold': n_cars_sold, 'money_earned': money_earned, 'max_deal': max_deal, 'top_saloons': list(top_saloons),
            'top_cars': list(top_cars)}
    serializer = DealerStatisticsSerializer(data=data)

    if serializer.is_valid():
        return serializer


def get_saloon_stat(saloon_id):
    base_buyer_query = SaloonToBuyerHistory.objects.filter(saloon=saloon_id)
    buyer_query = base_buyer_query.values_list('deal_price', flat=True)

    n_cars_sold = len(buyer_query)
    money_earned = sum(buyer_query)
    max_deal = max(buyer_query)

    top_cars_sold = base_buyer_query.prefetch_related('car').values('car__model_name').annotate(
        amount=Count('car')).order_by('-amount')[:10]
    top_buyers = base_buyer_query.prefetch_related('profile__user').values('profile__user__username').annotate(
        cars_bought=Count('profile')).order_by('-cars_bought')[:10]

    base_dealer_query = DealerToSaloonHistory.objects.filter(saloon=saloon_id)
    dealer_query = base_dealer_query.values_list('deal_price', flat=True)
    money_spent = sum(dealer_query)
    money_diff = money_earned - money_spent

    top_dealers = base_dealer_query.prefetch_related('dealer').values('dealer__name').annotate(
        cars_bought=Count('dealer')).order_by('-cars_bought')[:10]

    data = {'n_cars_sold': n_cars_sold, 'money_earned': money_earned, 'money_spent': money_spent, 'money_diff': money_diff,
            'max_deal': max_deal, 'top_cars_sold': list(top_cars_sold), 'top_buyers': list(top_buyers), 'top_dealers': list(top_dealers)}

    serializer = AutoSaloonStatisticsSerializer(data=data)
    if serializer.is_valid():
        return serializer
    else:
        print("Something wrong with serializer")
