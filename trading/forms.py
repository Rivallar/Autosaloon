from django import forms

from trading.models import AutoSaloon, Offer


class AutoSaloonForm(forms.ModelForm):
    class Meta:
        model = AutoSaloon
        fields = ['country', 'city', 'address', 'car_characteristics', 'balance', 'buyer_discounts']


class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ['profile', 'max_price', 'car_model']
