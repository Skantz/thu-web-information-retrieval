from urllib.request import Request, urlopen
from urllib.parse import urlparse
from bs4 import BeautifulSoup as bs
from url_regex import URL_REGEX
import re
import sys
import os
import time
HEADERS = {'User-Agent': 'Mozilla/5.0'}
SLEEP   = 1
def get_links(webpage, filtr):
    req  = Request(webpage, headers=HEADERS)
    time.sleep(SLEEP)
    page = urlopen(webpage)
    soup = bs(page)
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
for link in crawl_flat(start_page, 1, filtr):
    with open(urlparse(link).netloc, 'w+') as f:
        req = Request(link, headers=HEADERS)
        f.write(urlopen(link).read().decode('utf-8') + ".html")
