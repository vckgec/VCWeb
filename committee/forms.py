from django import forms
from .models import Account
from dues.fields import CSSTextListWidget


class CreditForm(forms.ModelForm):
    name='Credit'
    credit = forms.FloatField(widget=forms.TextInput(attrs={'placeholder': 'Credit', 'class': 'form-control', 'max_length': 16}))
    remarks = forms.CharField(required=False,widget=forms.Textarea(attrs={'placeholder': 'Remarks', 'max_length': 100, 'class': 'form-control', 'style': 'height:100px'}))
    class  Meta:
        model=Account
        fields=['credit','remarks']

class DebitForm(forms.ModelForm):
    name='Debit'
    debit = forms.FloatField(widget=forms.TextInput(attrs={'placeholder': 'Debit', 'class': 'form-control', 'max_length': 16}))
    remarks = forms.CharField(required=False,widget=forms.Textarea(attrs={'placeholder': 'Remarks', 'max_length': 100, 'class': 'form-control', 'style': 'height:100px'}))
    class  Meta:
        model=Account
        fields=['debit','remarks']
