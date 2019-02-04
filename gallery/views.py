import mimetypes
import os
import posixpath
import re
import stat
from django.utils._os import safe_join
from django.utils.http import http_date, parse_http_date
from django.utils.six.moves.urllib.parse import unquote
from django.http import (
    FileResponse, Http404, HttpResponse, HttpResponseNotModified,
)
from django.shortcuts import render
from django.views.static import serve


# Create your views here.

def ftp(request,path):
    document_root = os.path.dirname(path)
    path = posixpath.normpath(unquote(os.path.basename(path))).lstrip('/')
    fullpath = safe_join(document_root, path)
    if os.path.isdir(fullpath):
        files = []
        for f in os.listdir(fullpath):
            if not f.startswith('.'):
                if os.path.isdir(os.path.join(fullpath, f)):
                    f += '/'
                files.append(f)
        return render(request,'gallery/gallery.html',{'directory': fullpath + '/','file_list': files})
    if not os.path.exists(fullpath):
        raise Http404(('"%(path)s" does not exist') % {'path': fullpath})
    # print(mimetypes.guess_type(fullpath))
    return serve(request,path,document_root)

def play(request,path):
    return render(request,'gallery/play.html',{'src':path})

def Youtube(request):
    try:
        import requests
        import bs4
        res = requests.get("https://www.youtube.com/channel/UCn-UsYWkx-2-bCCau0bjhRQ")
        res.raise_for_status()
        soups = bs4.BeautifulSoup(res.text, "lxml")
        results=[]
        for soup in soups.select('a[class="yt-uix-sessionlink"]'):
            try:
                result = {'link':soup.attrs['href'],\
                'text':soups.select('a[href='+soup.attrs['href']+']')[1].getText(),\
                'iframesrc':soup.attrs['href'].split("=")[1],\
                'imgsrc':soup.select('img')[0].attrs['data-thumb']}
                results.append(result)
                #print(soups.select('a[href='+soup.attrs['href']+']')[1].getText())
                #print(soup.select('img')[0].attrs['data-thumb'])
                #print(soups.select('a[href='+soup.attrs['href']+']')[1].getText())
            except:
                pass
    except:
        results=[]
    return render(request,'gallery/youtube.html',{'results':results})
