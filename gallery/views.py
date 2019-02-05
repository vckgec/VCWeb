import os
import mimetypes
import posixpath
import re
from django.utils._os import safe_join
from django.utils.six.moves.urllib.parse import unquote
from django.http import FileResponse, Http404, HttpResponse, HttpResponseNotModified,StreamingHttpResponse
from django.shortcuts import render
from django.views.static import serve
from time import ctime
from wsgiref.util import FileWrapper

# Create your views here.

range_re = re.compile(r'bytes\s*=\s*(\d+)\s*-\s*(\d*)', re.I)

class RangeFileWrapper(object):
    def __init__(self, filelike, blksize=8192, offset=0, length=None):
        self.filelike = filelike
        self.filelike.seek(offset, os.SEEK_SET)
        self.remaining = length
        self.blksize = blksize

    def close(self):
        if hasattr(self.filelike, 'close'):
            self.filelike.close()

    def __iter__(self):
        return self

    def __next__(self):
        if self.remaining is None:
            # If remaining is None, we're reading the entire file.
            data = self.filelike.read(self.blksize)
            if data:
                return data
            raise StopIteration()
        else:
            if self.remaining <= 0:
                raise StopIteration()
            data = self.filelike.read(min(self.remaining, self.blksize))
            if not data:
                raise StopIteration()
            self.remaining -= len(data)
            return data


def stream(request, path):
    range_header = request.META.get('HTTP_RANGE', '').strip()
    range_match = range_re.match(range_header)
    size = os.path.getsize(path)
    content_type, encoding = mimetypes.guess_type(path)
    content_type = content_type or 'application/octet-stream'
    if range_match:
        first_byte, last_byte = range_match.groups()
        first_byte = int(first_byte) if first_byte else 0
        last_byte = int(last_byte) if last_byte else size - 1
        if last_byte >= size:
            last_byte = size - 1
        length = last_byte - first_byte + 1
        resp = StreamingHttpResponse(RangeFileWrapper(open(path, 'rb'), offset=first_byte, length=length), status=206, content_type=content_type)
        resp['Content-Length'] = str(length)
        resp['Content-Range'] = 'bytes %s-%s/%s' % (first_byte, last_byte, size)
    else:
        resp = StreamingHttpResponse(FileWrapper(open(path, 'rb')), content_type=content_type)
        resp['Content-Length'] = str(size)
    resp['Accept-Ranges'] = 'bytes'
    return resp

def convert_bytes(num):
    """
    this function will convert bytes to MB.... GB... etc
    """
    for unit in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%.2f %s" % (num, unit)
        num /= 1024.0

def ftp(request,path):
    document_root = os.path.dirname(path)
    path = posixpath.normpath(unquote(os.path.basename(path))).lstrip('/')
    fullpath = safe_join(document_root, path)
    if os.path.isdir(fullpath):
        files = []
        for f in os.listdir(fullpath):
            f_stat={}
            if not f.startswith('.'):
                p = os.path.join(fullpath, f)
                if os.path.isdir(p):
                    f_stat['type']='directory'
                    f_stat['size'] = ''
                else:
                    f_stat['type']='file'
                    f_stat['size'] = convert_bytes(os.path.getsize(p))
                f_stat['name'] = f
                f_stat['lastModified'] = ctime(os.path.getmtime(p))
                files.append(f_stat)
        return render(request,'gallery/gallery.html',{'directory': fullpath,'file_list': files})
    if not os.path.exists(fullpath):
        raise Http404(('"%(path)s" does not exist') % {'path': fullpath})
    return stream(request,fullpath)

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
