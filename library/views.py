from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.views import generic
from .models import Book,Subject
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import View
from .forms import *
from django.contrib import messages
from .models import Book
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .libgen import searchbooks as searchebooks
from account.forms import JsonLoadForm
import json
import datetime
global query
# Create your views here.

"""class Subject(CreateView):
    model = Subject
    fields = ['title','code']

class BookCreate(CreateView):
    model = Book
    fields = ['author', 'title', 'subject', 'image']

class BookEdit(UpdateView):
    model = Book
    fields = ['author', 'title', 'subject', 'image']"""

class BookIndex(generic.ListView):
    template_name = 'library/index.html'
    context_object_list = 'object_list'

    def get_queryset(self):
        return Book.objects.all()

def BookDetail(request, id):
    reqbook = get_object_or_404(Book, id=id)
    if request.method == 'GET':
        form=BookRequest(None)
        return render(request, 'library/detail.html', {'form':form, 'reqbook':reqbook})
    if request.method == 'POST':
        form = BookRequest(request.POST)
        if form.is_valid():
            req = form.save(commit=False) 
            req.book = reqbook #adding current book to the request.
            req.save()
            if reqbook.issued==True:
                messages.warning(request, 'This book has already been issued out,')
            messages.success(request, 'Your request for ' + reqbook.title + ' has been registered.')
        return render(request, 'library/detail.html', {'form': form, 'reqbook': reqbook})

def NewForm(request):
    if request.method == 'POST':
        form=New(request.POST)
        if form.is_valid():
            form.save()
            message.success(request, 'Your request has been submitted.')
    else:
        form=New(None)
    return render(request, 'library/new.html', {'form': form})

#@login_required
class BookAdd(CreateView):
    template_name='library/add.html'
    form_class = BookAdd

#@login_required
class BookEdit(UpdateView):
    model = Book
    template_name = 'library/edit_book.html'
    fields = ['title','author','subject','publisher','image']

class Requests(generic.ListView):
    template_name = 'library/requests.html'
    context_object_list = 'object_list'

    def get_queryset(self):
        return Request.objects.all()

def IssueBook(request, id):
    req = get_object_or_404(Request, id=id)
    book = req.book
    if not book.issued :
        book.issued = True
        book.name=req.name
        book.save()
        req.status = True
        req.save()
        messages.success(request, 'You issued out this book to ' + req.name +'.')
        return redirect('library:req')
    else:
        messages.error(request, 'Oops! Something went wrong! Looks like this book was already issued.')
    return redirect('library:req')

def ReturnBook(request, id):
    req = get_object_or_404(Request, id=id)
    book = req.book
    if not book.issued:
        messages.warning(request, 'It doesn\'t look like this book had been issued out. Contact an admin.')
    req.retstatus = True
    req.save()
    messages.success(request, 'You asked for this book to be collected.')
    return redirect('library:req')

def CollectBook(request, id):
    req = get_object_or_404(Request, id=id)
    book = req.book
    if not book.issued:
        messages.warning(request, 'It doesn\'t look like this book had been issued out. Contact an admin.')
    else:
        book.issued = False
        book.save()
        req.status = False
        req.save()
        messages.success(request, 'You collected this book.')
    return redirect('library:req')

def UndoReturn(request, id):
    req = get_object_or_404(Request, id=id)
    req.retstatus = False
    req.save()
    messages.success(request,"This return was cancelled.")
    return redirect('library:req')

import re, operator

def Search(request):
    if request.GET.get('q'):
        global query
        message = "you submitted " + request.GET['q']
        query=request.GET['q']
        q = query.lower()
        q = re.split('\s|\,',q)
        q = [x for x in q if x]
        all_books = Book.objects.all()
        results = []
        for book in all_books:
            slug = book.author.lower() +'-'+ book.title.lower() +'-'+ book.subject.title.lower() +'-'+ book.publisher.lower()
            #results.append(slug)
            count = 0
            for tag in q:
                if tag in slug:
                    count += 1
            if count == len(q):
                thisresult = [book,count]
                results.append(thisresult)
        results.sort(key=operator.itemgetter(1), reverse=True)
        message+=str(q)
        message += str(results)
       
    else:
        message = "Nothing submitted!"
        results=[]
        eresults=[]
        query=''
    
    return render(request, 'library/search.html', {'message':message, 'query':query, 'results':results})

def libgen(request):
    global query
    try:
        eresults = searchebooks(str(query))
        query=''
    except:
        eresults = []
        query=''
    return render(request, 'library/search.html', {'eresults':eresults})



#def FindEbooks(string):
#   httpslibgen.io/search.php?req=bachelor of arts&lg_topic=libgen&open=0&view=simple&res=25&phrase=1&column=def

def LibHome(request):
    return render(request, 'library/library.html')

def dateFix(request):
    if request.method=='POST':
        loadform = JsonLoadForm(request.POST)
        file = request.POST['files']
        fields=json.loads(open(file).read())
        for field in fields:
            del field['fields']['book']
            issue_date = field['fields']['issue_date']
            del field['fields']['issue_date']
            req = Request.objects.filter(**field['fields'])
            if req:
                req[0].issue_date = datetime.date(
                    int(issue_date.split('-')[0]), int(issue_date.split('-')[1]), int(issue_date.split('-')[2]))
                req[0].save()
        return HttpResponse("Successfull")
    else:
        loadform = JsonLoadForm(None)
        return render(request, 'account/json.html', {'dumpform': None, 'loadform': loadform})