from django import forms
from .models import Dues
from account.models import Boarder
from .fields import CSSTextListWidget

class PrintScan(forms.Form):
    user = forms.CharField(label="Name",widget=CSSTextListWidget(queryset=Boarder.objects.all(),attrs={"autocomplete": "off", "placeholder": "Search..", "id": "myInput", "class": "form-control"}))
    a4_paper = forms.DecimalField(required=False, label="No of A4 Papers", widget=forms.TextInput(
        attrs={'placeholder': 'No of A4 Papers', 'class': 'form-control', 'max_length': 16}))
    bw_print_single = forms.FloatField(required=False, label="No of B/W Prints or Xerox(Single Side)", widget=forms.TextInput(
        attrs={'placeholder': 'No of B/W Prints or Xerox(Single Side)', 'class': 'form-control', 'max_length': 16}))
    bw_print_double = forms.DecimalField(required=False, label="No of B/W Prints or Xerox(Double Side)", widget=forms.TextInput(
        attrs={'placeholder': 'No of B/W Prints or Xerox(Double Side)', 'class': 'form-control', 'max_length': 16}))
    color_print = forms.DecimalField(required=False, label="No of Color Prints", widget=forms.TextInput(attrs={
                                     'placeholder': 'No of Color Prints', 'class': 'form-control', 'max_length': 16}))
    five_photo_strip = forms.DecimalField(required=False, label="No of Photo Strip(5 Pics) Prints", widget=forms.TextInput(attrs={
                                          'placeholder': 'No of Photo Strip(5 Pics) Prints', 'class': 'form-control', 'max_length': 16}))
    photo_paper = forms.DecimalField(required=False, label="No of Photo Paper Prints", widget=forms.TextInput(attrs={
                                     'placeholder': 'No of Photo Paper Prints', 'class': 'form-control', 'max_length': 16}))
    def is_valid(self):
        parent=super(PrintScan,self).is_valid()
        if not parent:
            self._errors['user'] = "Please selecet one from list"
        fill_field=0
        keys = list(self.cleaned_data.keys())
        for i in range(len(keys)):
            if self.cleaned_data[keys[i]] != None:
                fill_field+=1            
        if fill_field<2:
            for i in range(len(keys)):
                #self.add_error(keys[i],"Only one field have to field")
                if keys[i]=='user':
                    pass
                else:
                    self._errors[keys[i]] = "Only one field have to field"
        else:
            return parent and True

class AddForm(forms.Form):
    name='Add'
    boarder_id = forms.CharField(widget=CSSTextListWidget(queryset=Boarder.objects.all(),first=(0,'All'),default=0, attrs={
                           "autocomplete": "off", "placeholder": "Search..", "id": "addInput", "class": "form-control"}))
    added = forms.FloatField(widget=forms.TextInput(attrs={'placeholder': 'Added', 'class': 'form-control', 'max_length': 16}))
    remarks = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Cause', 'max_length': 100, 'class': 'form-control','style':'height:100px'}))

class PaidForm(forms.Form):
    name='Paid'
    boarder_id = forms.CharField(widget=CSSTextListWidget(queryset=Boarder.objects.all(), first=(0, 'All'), default=0, attrs={
        "autocomplete": "off", "placeholder": "Search..", "id": "paidInput", "class": "form-control"}))
    paid = forms.FloatField(widget=forms.TextInput(
        attrs={'placeholder': 'Paid', 'class': 'form-control', 'max_length': 16}))
    remarks = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': 'Cause', 'max_length': 100, 'class': 'form-control', 'style': 'height:100px'}))
