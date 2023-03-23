from django.db.models import Count, Sum, Max

from trading.models import SaloonToBuyerHistory, DealerToSaloonHistory
from statistics_app.serializers import AutoSaloonStatisticsSerializer, DealerStatisticsSerializer, ProfileStatisticsSerializer


def get_profile_stat(profile_id):

    base_query = SaloonToBuyerHistory.objects.filter(profile=profile_id)

    car_models_bought = base_query.prefetch_related('car').values_list('car__model_name', flat=True).distinct()
    cars_amount = base_query.count()
    money_spent = base_query.values('deal_price').aggregate(total=Sum('deal_price'))
    max_price = base_query.values('deal_price').aggregate(max_deal=Max('deal_price'))

    data = {'car_models_bought': list(car_models_bought), 'cars_amount': cars_amount, 'money_spent': money_spent['total'],
            'max_price': max_price['max_deal']}

    serializer = ProfileStatisticsSerializer(data=data)
    if serializer.is_valid():
        return serializer


def get_dealer_stat(dealer_id):
    base_query = DealerToSaloonHistory.objects.filter(dealer=dealer_id)

    n_cars_sold = base_query.count()
    money_earned = base_query.aggregate(total=Sum('deal_price'))['total']
    max_deal = base_query.aggregate(max_deal=Max('deal_price'))['max_deal']

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

    n_cars_sold = base_buyer_query.count()
    money_earned = base_buyer_query.aggregate(total=Sum('deal_price'))['total']
    max_deal = base_buyer_query.aggregate(max_deal=Max('deal_price'))['max_deal']

    top_cars_sold = base_buyer_query.prefetch_related('car').values('car__model_name').annotate(
        amount=Count('car')).order_by('-amount')[:10]
    top_buyers = base_buyer_query.prefetch_related('profile__user').values('profile__user__username').annotate(
        cars_bought=Count('profile')).order_by('-cars_bought')[:10]

    base_dealer_query = DealerToSaloonHistory.objects.filter(saloon=saloon_id)

    money_spent = base_dealer_query.aggregate(total=Sum('deal_price'))['total']
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
