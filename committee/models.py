from django.db import models
from account.models import Boarder

# Create your models here.

class Committee(models.Model):
    NAME_CHOICES = (('net', 'Net Committee'),
                    ('library', 'Library Committee'),
                    ('recreation', 'Recreation Committee'),
                    ('canteen', 'Canteen Committee'),
                    ('mess', 'Mess Committee'),
                    ('sport', 'Sport Committee'))
    name = models.CharField(max_length=20,choices=NAME_CHOICES,primary_key=True)
    members = models.ManyToManyField(Boarder, blank=True,limit_choices_to={'Current_Boarder': True})
    def __str__(self):
        return self.name.capitalize()

class Account(models.Model):
    action_time=models.DateTimeField(auto_now_add=True)
    changed_by=models.ForeignKey(Boarder,limit_choices_to={'Current_Boarder':True},blank=True)
    committee = models.ForeignKey(Committee, on_delete=models.CASCADE)
    credit=models.FloatField(default=0.0)
    debit=models.FloatField(default=0.0)
    remarks=models.TextField(blank=True)
    def __str__(self):
        if self.credit-self.debit>0:            
            return '%s credit rupees %s in %s committee (%s)'%(self.changed_by,self.credit,self.committee,self.remarks)
        else:
            return '%s debit rupees %s in %s committee (%s)' % (self.changed_by, self.debit, self.committee, self.remarks)