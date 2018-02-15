def searchbooks(name):
    from pip._vendor import requests
    import bs4
    url="http://libgen.io/search.php?&res=25&page=1&req="
    url+=name
    #print("downloading page ", url)
    res = requests.get(url)
    #print(res)
    res.raise_for_status()    
    soup = bs4.BeautifulSoup(res.text, "lxml")
    #print(soup)
    print(soup.select('td')[2].getText())
    elems_temp = soup.select('tr') 
    elems=[]
    results=[]
    for i in elems_temp:
        if '[1]' in str(i):
            elems.append(i)
    for elem in elems:
        #print(elem)
        res = requests.get(elem.select('td a[title="Libgen.io"]')[0].attrs['href'], "lxml")
        res.raise_for_status()
        soup = bs4.BeautifulSoup(res.text, "lxml")
        #print(soup.select('a')[1].attrs['href'])
        result = {'booklink':soup.select('a')[1].attrs['href'],\
        'title':elem.select('td')[2].getText(),\
        'size':elem.select('td')[7].getText(),\
        'type':elem.select('td')[8].getText(),\
        'author':elem.select('td')[1].getText()}
        
        # res2=requests.get(result['adlink'])
        # res2.raise_for_status()
        # soup = bs4.BeautifulSoup(res2.text)
        """turns out, scraping for the direct download link is useless,
         since libgen wants you to visit their ads.php 
         page everytime you want to make the download.
         Hence removing this part."""
        #result['booklink'] = result['adlink'] #soup.select('td > a')[0].attrs['href']
        results.append(result)
    #print(results)
    return results
# searchbooks("Shantaram")
#searchbooks("numerical method")
