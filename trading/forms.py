from django import forms

from trading.models import AutoSaloon


class AutoSaloonForm(forms.ModelForm):
    class Meta:
        model = AutoSaloon
        fields = ['country', 'city', 'address', 'car_characteristics', 'balance', 'buyer_discounts']
