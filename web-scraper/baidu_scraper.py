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

def get_baidu_content(search_page):
    search_res = []
    req  = Request(search_page, headers=HEADERS)
    page = urlopen(req)
    soup = bs(page, "html.parser")
    all_links = soup.find_all(class_="result")
    for idx, link in enumerate(all_links):

        #'{"title":"$108 Flights to Beijing, China (BJS) - Tripadvisor","url":"http://www.baidu.com/link?url=-VvkH4M5BDkpOJOu8DnoMe3n_6z0CnkH5RL6wZcwRiY39RyLrZZ_6_cPV4TI4rZoH8l4SWm4-QDKyBmR-KqR5_fVeh3RQFh_kM0i9VGhFUqZSs1xaWPNyFtlEZpsSFhj"}\' 
        re_split = re.split('\"title\":\"|\","url":\"|\"\}\'|\&quot\;\:\&quot\;|\&quot\;\}\"', str(link))
        ##print("\n\n\n\n\n".join(re_split))
        #print("title", re_split[1])
        #print("temp url", re_split[2])
        search_res.append({'rank':idx+1, 'title':re_split[1], 'baidu_link':re_split[2]})
    return search_res

try:
    start_page = sys.argv[1]
except IndexError:
    print("Use: arg1 - target url")

search_res = get_baidu_content(start_page)

for r in search_res:

    try:
        #req = Request(r['baidu_link'], HEADERS, method='POST')
        print(r['baidu_link'])
        page = urlopen(r['baidu_link'], timeout=2)
        r['url'] = page.geturl()
        with open(urlparse(r['url']).netloc + ".html", 'w+') as f:
            f.write(page.read().decode('utf-8'))
    except Exception as e:
        print(e)
        continue
    del r['baidu_link']


for r in search_res:
    print(r)

"""
for idx, link in enumerate(crawl_flat(start_page, 1, filtr)):
    #dict = {"rank": idx + 1, "title":, "url": urlparse(link).netloc}
    time.sleep(SLEEP)
    if "microsoft" in link:
        continue
    if "baidu" in link:
        baidu_results = get_baidu_content(link)
        for r in baidu_results:
            print(r)
    with open(urlparse(link).netloc + ".html", 'w+') as f:
        print("Try to open", urlparse(link).netloc)
        try:
            req = Request(link, headers=HEADERS)
            f.write(urlopen(link).read().decode('utf-8'))
        except Exception as e: #HTTPerror
            print(e)
"""
