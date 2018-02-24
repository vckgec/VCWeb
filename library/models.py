from __future__ import unicode_literals
from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User as AuthUser

# Create your models here.

class Subject(models.Model):
    title = models.CharField(max_length=50)
    code = models.CharField(max_length=2)
    #branches = models.CharField(max_length=200)

    def __str__(self):
        return self.title + ' (' + self.code + ')'


class Book(models.Model):
    author = models.CharField(max_length=250)
    title = models.CharField(max_length=500, unique=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='library', blank=True)
    publisher = models.CharField(max_length=50, blank=True)
    issued = models.BooleanField(default=False)
    name = models.CharField(max_length=30, default='')

    def get_edit_url(self):
        return reverse('library:edit', kwargs={'pk':self.id})

    def get_absolute_url(self):
        return reverse('library:detail', kwargs={'id':self.id})

    class Meta:
        ordering = ('issued','subject','-title','-author',)

    def __str__(self):
        return self.author + '-' + self.title + ' ---- ' + (self.subject).code + str(self.pk)

class Request(models.Model):

    """
    An explaination regarding status and retstatus is in order, obviously. 

    To make things simple, let us consider all 
    the forms the combination of these two Booleans can take: 00, 01, 10, 11. 
    00: User makes a reequest, and both are inititalised as False.
    10: The book has been delivered, request has been marked to be completed.
    11: The issuer wants to return the book. He expresses this desire by marking retstatus as True.
    01: The book has been returned to its place of glory on the library shelf, and the given request has completed its cycle. 
    Now it only awaits the attention of a superuser who checks everything and allows it to dissolve into digital oblivion.
    """

    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    # user = models.ForeignKey(AuthUser, blank=True, null=True, default=None, related_name='requests')
    name = models.CharField(max_length=30)
    remarks = models.TextField(blank=True)
    status = models.BooleanField(default=False)
    retstatus = models.BooleanField(default=False)
    issue_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(blank=True, null=True, default=None) #Not sure anymore if I even want this so..
    issued_by = models.ForeignKey(AuthUser, blank=True, null=True, default=None, on_delete=models.CASCADE,related_name='requests_completed')
    returned_by = models.ForeignKey(AuthUser, blank=True, null=True, default=None,on_delete=models.CASCADE, related_name='returns_completed')


    def __str__(self):
        if self.status == True:
            return self.name + "'s request completed."
        return self.name + ' requested a Book'

    def get_absolute_url(self):
        return reverse('library:req')

    def get_issue_url(self):
        return reverse('library:issue', kwargs={'id':self.id})

    def get_return_url(self):
        return reverse('library:return', kwargs={'id':self.id})

    def get_collect_url(self):
        return reverse('library:collect', kwargs={'id':self.id})

    def get_undo_url(self):
        return reverse('library:undoreturn', kwargs={'id':self.id})

class New(models.Model):
    details = models.TextField()
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name + ' wants an unregistered book.'

