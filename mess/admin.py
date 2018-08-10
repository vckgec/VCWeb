from django.contrib import admin
from .models import *

# Register your models here.
class PresenceAdmin(admin.ModelAdmin):
    list_filter = ('boarder__Year_Of_Passing','half','status','boarder__Current_Boarder')

admin.site.register(Store)
admin.site.register(Presence,PresenceAdmin)
admin.site.register(MessManager)
admin.site.register(MealDish)
admin.site.register(GuestMeal)
admin.site.register(StoreKeeper)
