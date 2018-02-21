from django import template
register = template.Library()


@register.filter
def get_path(name,path):
    return path+'/'+name
    