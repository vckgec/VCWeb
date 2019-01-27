from django.contrib import admin
from .models import *

# Register your models here.


class BoarderAdmin(admin.ModelAdmin):
<<<<<<< HEAD
    list_filter = ('Year_Of_Passing', 'Eats_Mutton', 'Eats_Chicken', 'Eats_Fish','Eats_Egg',
=======
    list_filter = ('Year_Of_Passing', 'Eats_Fish', 'Eats_Chicken', 'Eats_Egg',
>>>>>>> b256745d13b64abf5513683ecb34a82b6d39f01d
                   'Department', 'Current_Boarder')


admin.site.register(Boarder, BoarderAdmin)
