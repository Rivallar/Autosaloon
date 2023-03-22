from rest_framework import serializers


class ProfileStatisticsSerializer(serializers.Serializer):
    car_models_bought = serializers.ListField()
    cars_amount = serializers.IntegerField()
    money_spent = serializers.DecimalField(max_digits=15, decimal_places=2)
    max_price = serializers.DecimalField(max_digits=15, decimal_places=2)


class AutoSaloonStatisticsSerializer(serializers.Serializer):

    n_cars_sold = serializers.IntegerField()
    money_earned = serializers.DecimalField(max_digits=15, decimal_places=2)
    money_spent = serializers.DecimalField(max_digits=15, decimal_places=2)
    money_diff = serializers.DecimalField(max_digits=15, decimal_places=2)
    max_deal = serializers.DecimalField(max_digits=10, decimal_places=2)
    top_cars_sold = serializers.ListField()
    top_buyers = serializers.ListField()
    top_dealers = serializers.ListField()


class DealerStatisticsSerializer(serializers.Serializer):

    n_cars_sold = serializers.IntegerField()
    money_earned = serializers.DecimalField(max_digits=15, decimal_places=2)
    max_deal = serializers.DecimalField(max_digits=10, decimal_places=2)
    top_saloons = serializers.ListField()
    top_cars = serializers.ListField()
