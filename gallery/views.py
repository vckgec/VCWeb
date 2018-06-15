from django.shortcuts import render
from os import listdir
from os.path import isfile, join
from django.contrib.staticfiles.templatetags.staticfiles import static

# Create your views here.

def Home(request):
    mypath = 'static/gallery'
    allfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    return render(request,'gallery/gallery.html',{'results':allfiles})

def Youtube(request):
    try:
        from pip._vendor import requests
        import bs4    
        res = requests.get("https://www.youtube.com/channel/UCn-UsYWkx-2-bCCau0bjhRQ")
        #print(res.text)
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