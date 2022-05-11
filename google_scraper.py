import certifi
import ssl
from bs4 import BeautifulSoup
import urllib.request
import re
import pandas as pd

# UNCOMMENT WHICHEVER DATA YOU WANT TO RUN THE SCRAPER ON
from us_states import states
# from canadian_provinces import provinces

locations = states

headers = {'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.3'}

businessType = '+courier'
page = "1"

def fetchText(url):
    request = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(request, context=ssl.create_default_context(cafile=certifi.where()))
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text()
    return text

def query_google(url):
    request = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(request, context=ssl.create_default_context(cafile=certifi.where()))
    html = response.read()
    urls = parse(html)
    print('query_google urls: ', urls)
    return urls

def parse(html):
    soup = BeautifulSoup(html, 'html.parser')

    results = soup.find_all('div', attrs={'class': 'g'})

    clean_urls = []

    for result in results:
        link = result.find('a', href=True)
        clean_url = re.findall("(?P<url>https?://[^\s]+)", link['href'])
        print('clean_url: ', clean_url)
        if(len(clean_url) > 0):
            clean_urls.append(clean_url[0])

    return clean_urls

urls_to_be_scraped = []

for location in locations:
    try:
        searchQuery = location + businessType
        url = 'https://www.google.com/search?q=' + searchQuery + '&start=' + page
        urls = query_google(url)
        print('urls: ', urls)
        urls_to_be_scraped.extend(urls)
    except Exception as e:
        print('google_scrape error: ', e)
        continue

print('urls_to_be_scraped: ', urls_to_be_scraped)

for index, url in enumerate(urls_to_be_scraped):
    df = pd.DataFrame({'Index': index, 'URL': url}, index=[index])
    df.to_csv('google_urls.csv', mode='a',index=False, header=False)
    try:
        text = fetchText(url)
        text = text.replace("\n", "") 
        print('text: ', text)
        df = pd.DataFrame({'Index': index,'URL': url, 'Data': text}, index=[index])
        print('df', df)
        df.to_csv('google_text_data.csv', mode='a',index=False, header=False)
    except Exception as e:
        print('error: ', e)
        df = pd.DataFrame({'Index': index,'URL': url}, index=[index])
        df.to_csv('failed_scraped_google_urls.csv', mode='a',index=False, header=False)
        continue
