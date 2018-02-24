from django.contrib.auth.models import User
from django.conf import settings
from django.db import models
from django.utils import timezone
from datetime import date
from datetime import datetime

# Create your models here.

class Boarder(models.Model):
    DEPT_CHOICES = (('ME', 'Mechanical Engineering'),
        ('CSE', 'Computer Science and Engineering'),
        ('EE', 'Electrical Engineering'),
        ('IT', 'Information Technology'),
        ('ECE', 'Electronics and Communications'),
        ('MCA', 'Master of Computer Application'),
        ('MME', 'MTech: Mechanical'),
        ('MCSE', 'MTech: Computer Science'),
        ('MIT', 'MTech: Information Technology'),
        ('MEE', 'MTech: Electrical Engineering'),
        ('MECE', 'MTech: Electronics and Communication'),
        )

    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    dp = models.URLField(default='/media/account/default.png',blank=True)
    Name = models.CharField(max_length = 50)
    Year_Of_Passing = models.DecimalField(max_digits = 4, decimal_places = 0)
    Eats_Fish = models.BooleanField(default = True) #True if boarder eats fish
    Eats_Chicken = models.BooleanField(default = True)
    Eats_Mutton = models.BooleanField(default = True)
    Eats_Egg = models.BooleanField(default = True)
    Room_Number = models.CharField(max_length = 4)
    Morning_Presence = models.BooleanField(default = False) #True if the person is a current boarder
    Evening_Presence = models.BooleanField(default = False)
    Presence_Date=models.DateField(null=True)
    Department = models.CharField(choices = DEPT_CHOICES, max_length=40)
    def __str__(self):
        return self.Name
