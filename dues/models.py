from django.db import models
from account.models import Boarder
# Create your models here.

class Dues(models.Model):
    name=models.OneToOneField(Boarder,on_delete=models.CASCADE)
    first_charge=models.FloatField(default=0.0)
    net = models.FloatField(default=0.0)
    print_scan = models.FloatField(default=0.0)
    canteen = models.FloatField(default=0.0)
    recreation = models.FloatField(default=0.0)
    mess = models.FloatField(default=0.0)
    mess_bill = models.FloatField(blank=True, default=0.0)
    library = models.FloatField(default=0.0)
    def __str__(self):
        return "%s's total due in hostel(₹%s)" %(self.name,self.first_charge+self.net+self.print_scan+self.canteen+self.recreation+self.mess+self.library)
