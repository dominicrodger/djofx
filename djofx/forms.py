from django import forms
from djofx import models


class OFXForm(forms.Form):
    file = forms.FileField()


class CategoriseTransactionForm(forms.Form):
    next_url = forms.CharField(required=False, widget=forms.HiddenInput)
    category = forms.ModelChoiceField(
        queryset=models.TransactionCategory.objects.all(),
        required=True
    )


class CategoryForm(forms.ModelForm):
    class Meta:
        model = models.TransactionCategory
        fields = ('name', 'is_void', )
