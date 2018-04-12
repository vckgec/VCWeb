from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Chat(models.Model):
    username=models.ForeignKey(User,on_delete=models.CASCADE)
    dp = models.TextField(blank=True)
    name=models.CharField(max_length=200)
    message=models.CharField(max_length=1000)
    chat_datetime=models.DateTimeField()
    def __str__(self):
        return str(self.username)+':-'+self.message
