from django import forms
from .static import Static
from account.models import Boarder
class ListTextWidget(forms.TextInput):
    def __init__(self, data_list, name, *args, **kwargs):
        super(ListTextWidget, self).__init__(*args, **kwargs)
        self._name = name
        self._list = data_list
        self.attrs.update({'list': 'list__%s' % self._name}) #<input list = "list__user">

    def render(self, name, value, attrs=None):
        input_text = super(ListTextWidget, self).render(
            name, value, attrs=attrs)
        # <datalist id = "list__%s" >
        data_list = '<datalist id="list__%s">' % self._name
        for item in self._list:
            data_list += '<option value="%s">%s</option>' % (item.id, str(item)) #< option value = "%s" > %s < /option >
        data_list += '</datalist>'                                            #</datalist>
        return (input_text + data_list)


class MyDataListWidget(forms.TextInput):
    def __init__(self,queryset,*args, **kwargs):
        super(MyDataListWidget,self).__init__(*args, **kwargs)
        self._name=kwargs.pop('attrs',None)['list']
        self._list = queryset

    def render(self, name, value, attrs=None):
        input_text = super(MyDataListWidget, self).render(name, value, attrs=attrs)
        data_list = '<datalist id="%s">' % self._name
        for item in self._list:
            data_list += '<option value="[%s]%s">%s</option>' % (item.id, item, item)
        data_list += '</datalist>'
        return (input_text + data_list)

class TextDropdownWidget(forms.TextInput):
    def __init__(self, queryset, *args, **kwargs):
        super(TextDropdownWidget, self).__init__(*args, **kwargs)
        self._list = queryset

    def render(self, name, value, attrs=None):
        input_text = super(TextDropdownWidget, self).render(name, value, attrs=attrs)
        hidden_text='<input type="hidden" id="%s_hidden">'%name
        data_list = '<ul id="myDropdown" class="dropdown-menu">\n'
        for item in self._list:
            data_list += '<li> <a value=%s onclick="selectFunction(this)">%s</a></li>\n' % (item.id,item)
        data_list += '</ul>\n'+\
        '</div>\n'+\
        '<script>\n'+\
        'function myFunction() {\n'+\
            'document.getElementById("myDropdown").classList.toggle("show");\n'+\
        '}'+\
        'function selectFunction(obj){\n'+\
            'document.getElementById("myInput").value = obj.innerHTML\n'+\
            'myFunction();\n'+\
        '}\n'+\
        'function filterFunction() {\n'+\
            'myFunction();\n'+\
            'var input, filter, ul, li, a, i;\n'+\
            'input = document.getElementById("myInput");\n'+\
            'filter = input.value.toUpperCase();\n'+\
            'div = document.getElementById("myDropdown");\n'+\
            'a = div.getElementsByTagName("a");\n'+\
            'for (i=0; i < a.length; i++) {\n'+\
                'if (a[i].innerHTML.toUpperCase().indexOf(filter) > -1) {\n'+\
                    'a[i].style.display = "";} else {\n'+\
                    'a[i].style.display = "none";\n'+\
                '}\n'+\
            '}\n'+\
        '}\n'+\
        '</script>'
        return ('<div class = "dropdown">\n'+input_text+hidden_text +'\n'+ data_list)


class CSSTextListWidget(forms.HiddenInput):
    def __init__(self, queryset,dropdownId,*args, **kwargs):
        super(CSSTextListWidget, self).__init__(*args, **kwargs)
        self.TextInput = forms.TextInput(*args, **kwargs)
        self._list = queryset
        self.inputId = kwargs.pop('attrs', None)['id']
        self.dropdownId=dropdownId
    def render(self, name, value, attrs=None):
        hidden_text = super(CSSTextListWidget, self).render(name, value, attrs={'id':'%s_hidden'%self.inputId})
        input_text=self.TextInput.render('%s_text' % name, self._list.get(pk=value) if value else '', attrs=attrs)
        data_list = '<div id="%s" class="dropdown-content">\n' % self.dropdownId
        for item in self._list:
            data_list += '<a value="%s">%s</a>\n' % (item.id, item)
        data_list += '</div>\n'
        return (Static.getStyle(Static,self.inputId)+input_text + hidden_text + '\n' + data_list+Static.getScript(Static,self.inputId,self.dropdownId))

