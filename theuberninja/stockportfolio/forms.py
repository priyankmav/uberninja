from django import forms

from .models import Investment

class InvestmentForm(forms.ModelForm):
    class Meta:
        model = Investment
        fields = ['investment_name', 'investment_type', 'investment_ticker', 'investment_units', 'investment_price']