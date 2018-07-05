from django.db import models
from django.urls import reverse
from account.models import Boarder
# Create your models here.

class Dues(models.Model):
    NAME_CHOICES = (('printscan', 'Print & Scan'),
                    ('net', 'Net'),
                    ('library', 'Library'),
                    ('recreation', 'Recreation'),
                    ('canteen', 'Canteen'),
                    ('mess', 'Mess'),
                    ('messbill', 'Mess Bill'))
    name = models.CharField(max_length=20, choices=NAME_CHOICES)
    boarder = models.ForeignKey(Boarder, on_delete=models.CASCADE, related_name='boarder')
    action_time = models.DateTimeField(auto_now_add=True)
    changed_by = models.ForeignKey(Boarder, on_delete=models.CASCADE, limit_choices_to={'Current_Boarder': True}, related_name='changed_by')
    added = models.FloatField(default=0.0)
    paid = models.FloatField(default=0.0)
    remarks = models.TextField(blank=True)

    def __str__(self):
        if self.added-self.paid>0:
            return '%s\'s dues added rupees %s in %s (%s)'%(self.boarder,self.added,self.name,self.remarks)
        else:
            return '%s paid rupees %s in %s (%s)' % (self.boarder, self.paid, self.name,self.remarks)
