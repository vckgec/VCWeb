from django.contrib import admin
from .models import *

# Register your models here.


class BoarderAdmin(admin.ModelAdmin):
    list_filter = ('Year_Of_Passing', 'Eats_Fish', 'Eats_Chicken', 'Eats_Egg',
                   'Department', 'Current_Boarder')


admin.site.register(Boarder, BoarderAdmin)
