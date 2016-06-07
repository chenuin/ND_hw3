#!/usr/bin/env python3
# Foundations of Python Network Programming, Third Edition
# https://github.com/chenuin/ND_hw3/blob/master/crawler.py
# Extract the email addresses from all the web pages reachable from that web site

import argparse, requests
import urllib.request,re
from urllib.parse import urljoin, urlsplit
from lxml import etree

def GET(url):
    response = requests.get(url)
    if response.headers.get('Content-Type', '').split(';')[0] != 'text/html':
        return
    text = response.text
    try:
        html = etree.HTML(text)
    except Exception as e:
        print('    {}: {}'.format(e.__class__.__name__, e))
        return
    links = html.findall('.//a[@href]')
    time2 = 0
    for link in links:
        yield GET, urljoin(url, link.attrib['href'])

def scrape(start, url_filter, numEXECUTE):
    further_work = {start}
    already_seen = {start}
    time = 0
    while further_work:
        call_tuple = further_work.pop()
        function, url, *etc = call_tuple
        print(function.__name__, url, *etc)

        try:
            tmp = str.encode(url)
            f = urllib.request.urlopen(url)
            s = f.read()
            mail = []
            mail = re.findall(b"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}",s)
            print(*mail, sep='\n')
			
        except Exception as e:
            print('    {}: {}'.format(e.__class__.__name__, e))


        for call_tuple in function(url, *etc):
            if call_tuple in already_seen:
                continue
            already_seen.add(call_tuple)
            function, url, *etc = call_tuple
            if not url_filter(url):
                continue
            further_work.add(call_tuple)
        time = time + 1
        #print (numEXECUTE)
        if time > numEXECUTE:
            exit()

def main(GET):
    parser = argparse.ArgumentParser(description='Scrape a simple site.')
    parser.add_argument('url', help='the URL at which to begin')
    parser.add_argument("-n", "--number", type=int, help="the number of reachable website", default=15)
    numEXECUTE = parser.parse_args().number
    #print (numEXECUTE)
    start_url = parser.parse_args().url
    starting_netloc = urlsplit(start_url).netloc
    url_filter = (lambda url: urlsplit(url).netloc == starting_netloc)
    scrape((GET, start_url), url_filter, numEXECUTE)

if __name__ == '__main__':
    main(GET)
