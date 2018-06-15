from django import forms
from .models import *
from account.models import Boarder
from datetime import date

class ChangeForm(forms.Form):
    HALF_CHOICES = (('MO', 'Morning'),('EV', 'Evening'),)
    STATUS_CHOICES = (('off', 'OFF'),('on', 'ON'),)
    presence_date=forms.DateField(widget=forms.DateTimeInput(attrs={'type':'date','class':'form-control','value':date.today()}))
    presence_half = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control','max_length': 16}),choices=HALF_CHOICES)
    presence_status = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control','max_length': 16}),choices=STATUS_CHOICES,initial='on')

class MealForm(forms.Form):
    HALF_CHOICES = (('MO', 'Morning'),('EV', 'Evening'),)
    meal_dishes = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Meal','max_length': 100,'class':'form-control','style':'height:50px'}))
    meal_half = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control','max_length': 16}),choices=HALF_CHOICES)
    meal_date=forms.DateField(widget=forms.DateTimeInput(attrs={'type':'date','class':'form-control','value':date.today()}))

class GuestForm(forms.ModelForm):
    HALF_CHOICES = (('MO', 'Morning'),('EV', 'Evening'),)
    STATUS_CHOICES = (('off', 'OFF'),('on', 'ON'),)
    Meal_Half = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control','max_length': 16}),choices=HALF_CHOICES)
    No_Of_Guest = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder':'No of guest','class':'form-control','max_length': 16,'value':0}))
    Meal_Date=forms.DateField(widget=forms.DateTimeInput(attrs={'type':'date','class':'form-control','value':date.today()}))
    class Meta:
        model=GuestMeal
        fields = ['Meal_Half','No_Of_Guest','Meal_Date']

class ExtraMealForm(forms.Form):
    HALF_CHOICES = (('MO', 'Morning'),('EV', 'Evening'),)
    STATUS_CHOICES = (('off', 'OFF'),('on', 'ON'),) 
    half = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control','max_length': 16,'style':'height:34px'}),choices=HALF_CHOICES)
    extra_meals = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder':'Extra Meal','class':'form-control','max_length': 16,'value':0}))
class AdjustCountForm(forms.Form):
    HALF_CHOICES = (('MO', 'Morning'),('EV', 'Evening'),)
    STATUS_CHOICES = (('off', 'OFF'),('on', 'ON'),) 
    half = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control','max_length': 16,'style':'height:34px'}),choices=HALF_CHOICES)
    adjust_count = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder':'Adjust Count','class':'form-control','max_length': 16,'value':0}))
class StoreKeeperForm(forms.Form):
    Store_Name = forms.ModelChoiceField(widget=forms.Select(attrs={'max_length': 16,'class':'form-control'}),queryset = Boarder.objects.filter(Year_Of_Passing=Boarder.objects.aggregate(Year_Of_Passing=Max('Year_Of_Passing'))['Year_Of_Passing'],Current_Boarder=True))