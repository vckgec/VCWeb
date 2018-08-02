from django import forms
from .models import *
from account.models import Boarder
from datetime import date
from django.db import connection

class ChangeForm(forms.Form):
    HALF_CHOICES = (('1MO', 'Morning'),('2EV', 'Evening'),)
    STATUS_CHOICES = (('off', 'OFF'),('on', 'ON'),)
    date=forms.DateField(widget=forms.DateTimeInput(attrs={'type':'date','class':'form-control','value':date.today()}))
    half = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control','max_length': 16}),choices=HALF_CHOICES)
    status = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control','max_length': 16}),choices=STATUS_CHOICES,initial='on')

class MealForm(forms.Form):
    HALF_CHOICES = (('1MO', 'Morning'),('2EV', 'Evening'),)
    dish = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Meal','max_length': 100,'class':'form-control','style':'height:50px'}))
    half = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control','max_length': 16}),choices=HALF_CHOICES)
    date=forms.DateField(widget=forms.DateTimeInput(attrs={'type':'date','class':'form-control','value':date.today()}))

class GuestForm(forms.ModelForm):
    HALF_CHOICES = (('1MO', 'Morning'),('2EV', 'Evening'),)
    STATUS_CHOICES = (('off', 'OFF'),('on', 'ON'),)
    half = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control','max_length': 16}),choices=HALF_CHOICES)
    number = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder':'No of guest','class':'form-control','max_length': 16,'value':0}))
    date=forms.DateField(widget=forms.DateTimeInput(attrs={'type':'date','class':'form-control','value':date.today()}))
    class Meta:
        model=GuestMeal
        fields = ['half','number','date']

class ExtraMealForm(forms.Form):
    name='Extra Meal'
    HALF_CHOICES = (('1MO', 'Morning'),('2EV', 'Evening'),)
    STATUS_CHOICES = (('off', 'OFF'),('on', 'ON'),) 
    half = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control','max_length': 16,'style':'height:34px'}),choices=HALF_CHOICES)
    extra_meals = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder':'Extra Meal','class':'form-control','max_length': 16,'value':0}))
class AdjustCountForm(forms.Form):
    name='Adjust Count'
    HALF_CHOICES = (('1MO', 'Morning'),('2EV', 'Evening'),)
    STATUS_CHOICES = (('off', 'OFF'),('on', 'ON'),) 
    half = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control','max_length': 16,'style':'height:34px'}),choices=HALF_CHOICES)
    adjust_count = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder':'Adjust Count','class':'form-control','max_length': 16,'value':0}))
class StoreKeeperForm(forms.Form):
    name = forms.ModelChoiceField(required=False,widget=forms.Select(attrs={'max_length': 16,'class':'form-control'}),queryset = Boarder.objects.filter(Year_Of_Passing=Boarder.objects.aggregate(Year_Of_Passing=Max('Year_Of_Passing'))['Year_Of_Passing'],Current_Boarder=True) if 'mess_storekeeper' in connection.introspection.table_names() else None)