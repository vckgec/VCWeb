from django.shortcuts import render
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from datetime import date
from django.http import *
from django.shortcuts import render_to_response,redirect
from django.template import RequestContext
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from .JsonModels import JSON
import base64
import websocket
import json

# Create your views here.

def send(message):
    try:
        ws = websocket.create_connection("wss://socketvc.herokuapp.com/")
        ws.send(json.dumps({'type': 'account', 'message':message }))
        result=ws.recv()
        print(result)
        ws.close()
        if result == 'Head client not found':
            return False
        else:
            return True
    except:
        return False

#@csrf_exempt
def login_user(request):
    logout(request)
    username=password=''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponse("OK")
        else:
            return HttpResponse("User doesn't exist")
    else:
        loginform=Login()
        return render(request,'account/login.html',{'loginform':loginform})

@login_required
def logout_user(request):
    logout(request)
    return HttpResponse("Successfully Logout")


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        b_form = BoarderRegistrationForm(request.POST)
        if form.is_valid() and b_form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            new_b = b_form.save(commit=False)
            new_b.user = new_user
            new_b.Name = new_user.first_name+" "+new_user.last_name
            new_b.Presence_Date = date.today()
            new_b.save()
            if not request.user.is_authenticated:
                user = authenticate(username=new_user.username, password=form.cleaned_data['password'])
                if user is not None:
                    logout(request)
                    if user.is_active:
                        login(request, user)
                        return redirect('mess:home')
            else:
                messages.success(request, 'Account successfully created. Pleasse login to activate your account')
                return redirect('login')
    else:
        form = UserRegistrationForm()
        b_form = BoarderRegistrationForm()
    return render(request,'account/register.html',{'form': form, 'b_form':b_form})


@login_required
def profile(request):
    return render(request, 'account/home.html')

@login_required
def change_password(request):
    if request.method == 'POST':
        form = ChangePassword(request.POST)
        if form.is_valid():
            if check_password(form.cleaned_data['old_password'], request.user.password):
                request.user.set_password(form.cleaned_data['new_password'])
                request.user.save()
                user = authenticate(username=request.user.username, password=form.cleaned_data['new_password'])
                if user is not None:
                    logout(request)
                    if user.is_active:
                        login(request, user)
                messages.success(request, 'Successfully change password')
                return redirect('.')
            else:
                form = ChangePassword()
                return render(request,'account/changepassword.html',{'errors':"Old password don\'t match",'form':form})
    else:
        form = ChangePassword()
    return render(request,'account/changepassword.html',{'form':form})

def forgot_password(request):
    if request.method=='POST':
        form = ForgotPassword(request.POST)
        if form.is_valid():            
            try:
                user=User.objects.get(username=form.cleaned_data['username'])
                reset_password=user.password[-11:-1]
                #asyncio.get_event_loop().run_until_complete(hello(reset_password))                
                if send({'email': form.cleaned_data['email'], 'password': reset_password}):
                    user.set_password(reset_password)
                    user.save()
                    messages.success(request, 'Password is send to '+form.cleaned_data['email'])
                else:
                    messages.warning(request,'Head client not found')
            except Exception as e:
                messages.warning(request, e)

            return redirect('.')
    else:
        form = ForgotPassword(None)
    return render(request,'account/forgotpassword.html',{'form':form})
def edit_details(request):
    if request.method=='POST':
        form=Edit_Details(request.POST,request.FILES)
        if form.is_valid():
            request.user.boarder.dp = base64.encodestring(
                form.cleaned_data['dp'].read()).decode('utf-8')
            request.user.boarder.save()            
    else:
        form=Edit_Details(None)
    return render(request,'account/editdetails.html',{'form':form})


def Json_Working(request):
    data=None
    if request.method=='POST':        
        dumpform = JsonDumpForm(request.POST)
        loadform=JsonLoadForm(request.POST,request.FILES)
        if dumpform.is_valid():
            obj=JSON(request.POST['appname'])
            try:
                data=obj.JsonDump()
            except:
                messages.warning(request,"Failed to dump")

        else:
            try:
                obj=JSON('all',request.POST.getlist("files"))
                try:
                    obj.JsonLoad(request.POST['dbtype'])
                    messages.success(request,"Successfully load data")
                except Exception as e:
                    messages.warning(request,e)
            except:
                pass
    else:
        dumpform = JsonDumpForm(None)
        loadform=JsonLoadForm(None)
    return render(request,'account/json.html',{'dumpform':dumpform,'loadform':loadform,'data':data})
