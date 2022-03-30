import certifi
import ssl
from bs4 import BeautifulSoup
import urllib.request
from urls import urlList
import pandas as pd
from langdetect import detect

urlListOne = ["https://enjoy.com"]

headers = {'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.3'}

def fetchText(url):
    request = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(request, context=ssl.create_default_context(cafile=certifi.where()))
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text()
    return text

def count_words(str):
    counts = dict()
    words = str.split()
    
    for word in words:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1
            
    counts_sorted = sorted(counts.items(), key=lambda x: x[1], reverse=True)

    return counts_sorted

for index, url in enumerate(urlListOne):
    try:
        text = fetchText(url)
        text = text.replace("\n", "") 
        if(detect(text) == 'en'):
            df = pd.DataFrame({'Index': index,'URL': url, 'Data': text}, index=[index])
            df.to_csv('data.csv', mode='a',index=False, header=False)
        else:
            raise Exception('other language')
            
    except Exception as e:
        df = pd.DataFrame({'Index': index,'URL': url}, index=[index])
        df.to_csv('failed.csv', mode='a',index=False, header=False)
        continue