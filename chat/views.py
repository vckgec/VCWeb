from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import *

# Create your views here.

@login_required
def Index(request):
    chats=Chat.objects.all()
    return render(request,'chat/chat.html',{'chats':chats})