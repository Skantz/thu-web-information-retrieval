from urllib.request import Request, urlopen
from urllib.parse import urlparse
from bs4 import BeautifulSoup as bs
from url_regex import URL_REGEX
import re
import sys
import os
import time
HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
         'Referer': 'https://cssspritegenerator.com',
         'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
         'Accept-Encoding': 'none',
         'Accept-Language': 'en-US,en;q=0.8',
         'Connection': 'keep-alive'}
SLEEP   = 0.2
def get_bing_content(search_page):
    req  = Request(search_page, headers=HEADERS)
    time.sleep(SLEEP)
    page = urlopen(req)
    soup = bs(page, "html.parser")
    #for remove_tag in ['a', 'strong', 'cite']:
    #    for m in soup.findAll(remove_tag):
    #        m.replaceWithChildren()
    #    if link.attrs['class'] == "b_algo":
    #        print(link.attrs)
    all_links = soup.find_all(class_="b_algo")
    for link in all_links:
        temp_res = str(link.find("h2"))
        print(temp_res)
        re_split = re.split('href=\"*|\">|</a>', temp_res)
        print(re_split)
        #print(link.get_text())
    print("printed all links")
def get_links(webpage, filtr):
    req  = Request(webpage, headers=HEADERS)
    time.sleep(SLEEP)
    page = urlopen(req)
    soup = bs(page, "html.parser")
    all_links= soup.findAll('a')
    res = []
    print("Crawl on ", webpage)
    print("# links ", len(all_links))
    for link in all_links:
        try:
            if re.search(URL_REGEX, link.get('href')): #and re.search(filtr, link.get('href')):
                res.append(link.get('href'))
                #print(link.get('href'))
        except TypeError:  #BS returns bs, sometimes
            continue
    return res
def crawl_flat(start_page, max_depth, filtr):
    res = [start_page]
    buf = [start_page]
    for _ in range(max_depth):
        new_buf = []
        for link in buf:
            new_pages = get_links(link, filtr)
            new_buf += new_pages
            res += new_pages
        buf = new_buf
    return res
try:
    start_page = sys.argv[1]
except IndexError:
    print("Use: arg1 - target url")
filtr = "/^((?!microsoft).)*$/"
for idx, link in enumerate(crawl_flat(start_page, 1, filtr)):
    #dict = {"rank": idx + 1, "title":, "url": urlparse(link).netloc}
    if "microsoft" in link or "bing" in link:
        if "bing" in link:
            print(get_bing_content(link))
    with open(urlparse(link).netloc + ".html", 'w+') as f:
        print("Try to open", urlparse(link).netloc)
        try:
            req = Request(link, headers=HEADERS)
            f.write(urlopen(link).read().decode('utf-8'))
        except Exception as e: #HTTPerror
            print(e)
