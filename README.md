# PythonCrawler
A (hopefully) robust crawler built in Python. Supports both list crawling and entire site crawling. 

### Starting the crawl
The crawler supports two modes list mode which crawls through a list of URLs and a standard crawling mode. In list mode it loads a .txt file of URLs with using a list comprehension. For the standard crawler you just add in the URLs which you want to use as a start point.
```
#listMode
#list_urls = [line.rstrip('\n') for line in open(r'urls.txt')]

# a queue of URLS to be crawled
new_urls = deque(['http://fx-today.com'])

```

### Use of Regex
The crawler relies heavily on regex - to make sure it sticks on the domain in question.

Pattern is used to match the domain in question - allowing only links matching the regex to be put into the crawl backlog. In theory this could be potentially changed to use urlparse or urlsplit from the urllib library. This regex matching is not required if you are just crawling a list of URLs.
```
#globalRegex1
#used to keep crawler on the domain in question
pattern = re.compile(".*http:\/\/:fx-today\.com*")

#globalRegex2
#used to block of parts of the site you don't want
pattern2 = re.compile("(.*badpath.*|.*awfulpath.*)")
```
### Extracting Stuff
Change the below code to extract the stuff you actually want. This function also writes your results to a CSV file. Arguably this should be split out into different functions.
```
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
 ```
