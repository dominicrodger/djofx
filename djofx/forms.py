from django import forms
from djofx import models


class OFXForm(forms.Form):
    file = forms.FileField()


class CategoriseTransactionForm(forms.Form):
    next_url = forms.CharField(required=False, widget=forms.HiddenInput)
    transaction_id = forms.IntegerField(widget=forms.HiddenInput)
    category = forms.ModelChoiceField(queryset=models.TransactionCategory.objects.all(), required=True)
