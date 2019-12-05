# This is a scrapper module to get news from fake news and real news sites. 
# Using BeautifulSoup as base library


import urllib3
from bs4 import BeautifulSoup

def getnpr(): 
    http = urllib3.PoolManager()
    quote_page = 'https://www.npr.org/tags/502124007/fake-news'
    r = http.request('GET', quote_page)
    # parse the html using beautiful soup and store in variable `soup`
    soup = BeautifulSoup(r.data, 'html.parser') 
    # Take out the <div> of name and get its value
    news = soup.find_all('h2', attrs={'class': 'title'})
    news = news[0:10]
    text = []
    for link in news:
        r = http.request('GET', link.a.get('href'))
        soup = BeautifulSoup(r.data, 'html.parser')
        text.append(soup.find('div', attrs={'class': 'storytitle'}).text.strip() + ' ' +
        soup.find('div', attrs={'class': 'storytext'}).text.strip())
    return text


def getbbc(): 
    http = urllib3.PoolManager()
    quote_page = 'https://www.bbc.com/news/world'
    r = http.request('GET', quote_page)
    # parse the html using beautiful soup and store in variable `soup`
    soup = BeautifulSoup(r.data, 'html.parser') 
    # Take out the <div> of name and get its value
    news = soup.find_all('article')
    news = news[0:10]
    text = []
    for link in news:
        new = link.header.div.h3.a.get('href')
        r = http.request('GET', 'https://www.bbc.com/'+new)
        soup = BeautifulSoup(r.data, 'html.parser')
        head = soup.find('h1', attrs={'class': 'story-body__h1'}).text.strip()
        body = soup.find('div', attrs={'class': 'story-body__inner'}).text.strip()
        text.append(head + ' ' +body)
    return text

# print(getbbc())










