from django import forms
from .static import Static
from account.models import Boarder

class CSSTextListWidget(forms.HiddenInput):
    def __init__(self, queryset,first=None, default=None, *args, **kwargs):
        super(CSSTextListWidget, self).__init__(*args, **kwargs)
        self.TextInput = forms.TextInput(*args, **kwargs)
        self._list = queryset
        self.inputId = kwargs.pop('attrs', None)['id']
        self.first=first
        if default is not None:
            self.default = 'select_%s=%s;\ninput_%s_hidden.value = a_%s[select_%s].getAttribute("value")\ninput_%s.value=a_%s[select_%s].innerHTML;\na_%s[select_%s].style.backgroundColor="#ddd";\n' % (self.inputId, default, self.inputId, self.inputId, self.inputId, self.inputId, self.inputId,self.inputId,self.inputId,self.inputId)
        else:
            self.default = ''
            
    def render(self, name, value, attrs=None):
        hidden_text = super(CSSTextListWidget, self).render(name, value, attrs={'id':'%s_hidden'%self.inputId})
        input_text = self.TextInput.render('%s_text' % name, self._list.get(pk=value) if value and value!='0' else 'All' if value == '0' else '', attrs=attrs)
        data_list = '<div id="%s_Dropdown" class="dropdown-content">\n' % self.inputId
        if self.first:
            data_list+='<a value="%s">%s</a>\n' % (self.first[0], self.first[1])
        for item in self._list:
            data_list += '<a value="%s">%s</a>\n' % (item.id, item)
        data_list += '</div>\n'
        return (Static.getStyle(Static,self.inputId)+input_text + hidden_text + '\n' + data_list+Static.getScript(Static,self.inputId,self.default))
