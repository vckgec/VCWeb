from django import forms
from account.models import Boarder
from .fields import ListTextWidget,MyDataListWidget,TextDropdownWidget,CSSTextListWidget

class Print_Scan(forms.Form):
    user = forms.CharField(required=True)
    def __init__(self, *args, **kwargs):
        data_list = kwargs.pop('data_list', None)
        super(Print_Scan, self).__init__(*args, **kwargs)
        # the "name" parameter will allow you to use the same widget more than once in the same
        # form, not setting this parameter differently will cuse all inputs display the
        # same list.
        self.fields['user'].widget = ListTextWidget(data_list=data_list, name='user')

class Print__Scan(forms.Form):
    user = forms.CharField(widget=MyDataListWidget(queryset=Boarder.objects.all(),attrs={'list':'list__user','class':'form-control'}))
    
class PrintScan(forms.Form):
    user = forms.CharField(label="Name",widget=CSSTextListWidget(queryset=Boarder.objects.all(), dropdownId="myDropdown", attrs={"autocomplete": "off", "placeholder": "Search..", "id": "myInput", "class": "form-control"}))
    a4_paper = forms.DecimalField(required=False, label="No of A4 Papers", widget=forms.TextInput(
        attrs={'placeholder': 'No of A4 Papers', 'class': 'form-control', 'max_length': 16}))
    bw_print_single = forms.DecimalField(required=False, label="No of B/W Prints or Xerox(Single Side)", widget=forms.TextInput(
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




