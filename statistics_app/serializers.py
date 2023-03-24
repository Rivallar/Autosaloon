from rest_framework import serializers


class ProfileStatisticsSerializer(serializers.Serializer):
    car_models_bought = serializers.ListField(allow_empty=True)
    cars_amount = serializers.IntegerField(min_value=0)
    money_spent = serializers.DecimalField(max_digits=15, decimal_places=2, allow_null=True)
    max_price = serializers.DecimalField(max_digits=15, decimal_places=2, allow_null=True)


class AutoSaloonStatisticsSerializer(serializers.Serializer):

    n_cars_sold = serializers.IntegerField()
    money_earned = serializers.DecimalField(max_digits=15, decimal_places=2, allow_null=True)
    money_spent = serializers.DecimalField(max_digits=15, decimal_places=2, allow_null=True)
    money_diff = serializers.DecimalField(max_digits=15, decimal_places=2, allow_null=True)
    max_deal = serializers.DecimalField(max_digits=10, decimal_places=2, allow_null=True)
    top_cars_sold = serializers.ListField(allow_empty=True)
    top_buyers = serializers.ListField(allow_empty=True)
    top_dealers = serializers.ListField(allow_empty=True)


class DealerStatisticsSerializer(serializers.Serializer):

    n_cars_sold = serializers.IntegerField()
    money_earned = serializers.DecimalField(max_digits=15, decimal_places=2, allow_null=True)
    max_deal = serializers.DecimalField(max_digits=10, decimal_places=2, allow_null=True)
    top_saloons = serializers.ListField(allow_empty=True)
    top_cars = serializers.ListField(allow_empty=True)
