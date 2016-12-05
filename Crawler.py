#imports
from bs4 import BeautifulSoup
import re
from urllib.parse import urlsplit
from collections import deque
import requests
import requests.exceptions as reqExc
from PopularAgents import DesktopAgents
from random import choice

#listMode
list_urls = [line.rstrip('\n') for line in open(r'urls.txt')]

# a queue of URLS to be crawled
new_urls = deque(['http://fx-today.com/'])

#list of URLs already crawled
processed_urls = set()

#globalRegex1
#used to keep crawler on the domain in question
pattern = re.compile(".*http:\/\/fx-today.com.*")

#globalRegex2
#used to block of parts of the site you don't want
pattern2 = re.compile("(.*badpath.*|.*awfulpath.*)")

#Pulls a random UserAgent from the PopularAgents file
def random_desktop_agent():
    agent = choice(DesktopAgents)
    return {'User-Agent': agent}

def requestPage(url):
    try:
        r = requests.get(url,headers=random_desktop_agent(),timeout=20)
        return r.url, r.text
    except reqExc.InvalidURL:
        with open('ErrorLog.txt','a',encoding='utf-8') as ErrorLog:
            ErrorLog.write('"{}","{}"'.format(url,'Invalid URL'))
    except reqExc.TooManyRedirects:
        with open('ErrorLog.txt','a',encoding='utf-8') as ErrorLog:
            ErrorLog.write('"{}","{}"'.format(url,'Too Many Redirects'))
    except:
        pass

def create_soup(html):
    try:
        soup = BeautifulSoup(html,'lxml')
        return soup
    except:
        soup = ''
        return soup

def extract_elements(soup,url):
    try:
        title = soup.find('title').get_text()
        title = title.strip()
    except:
        title = 'Not Found'
    try:
        primaryh1 = soup.find("h1").get_text()
        primaryh1 = primaryh1.strip()
    except:
        primaryh1 = 'Not Found'
    try:
        ResultsCount = soup.find('span', attrs={'class': 'nonexistant'}).get_text()
        ResultsCount = ResultsCount.strip()
    except:
        ResultsCount = 'Not Found'
    with open('Results.csv','a',encoding='utf-8') as resultsfile:
        resultsfile.write('"{}","{}","{}","{}"\n'.format(url,title,primaryh1,ResultsCount))

def extract_base_url(url):
    parts = urlsplit(url)
    base_url = "{0.scheme}://{0.netloc}".format(parts)
    path = url[:url.rfind('/') + 1] if '/' in parts.path else url
    return base_url,path

def process_anchors(soup,base_url,path):
    for anchor in soup.find_all("a"):
        link = anchor.attrs["href"] if "href" in anchor.attrs else ''
        if link.startswith('/'):
            link = base_url + link
        elif not link.startswith('http'):
            link = path + link
        if pattern.match(link) and not pattern2.match(link):
            if link not in new_urls and not link in processed_urls:
                new_urls.append(link)

def main():
    while len(new_urls) > 0:
        url = new_urls.popleft()
        processed_urls.add(url)
        url,html = requestPage(url)
        soup = create_soup(html)
        extract_elements(soup,url)
        base_url,path = extract_base_url(url)
        process_anchors(soup,base_url,path)

def list_mode():
    while len(list_urls) > 0:
        url = list_urls.pop()
        url,html = requestPage(url)
        soup = create_soup(html)
        extract_elements(soup,url)

#main()

#list_mode()








