import certifi
import ssl
from bs4 import BeautifulSoup
import urllib.request
from urls import urlList
import pandas as pd
from langdetect import detect
from googletrans import Translator

translator = Translator()

# urlListOne = ["https://trunkrs.nl"]

headers = {'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.3'}

def fetchText(urlList):
    request = urllib.request.Request(url, headers=headers)
    print('request: ', request.__dict__)
    response = urllib.request.urlopen(request, context=ssl.create_default_context(cafile=certifi.where()))
    print('response: ', response.__dict__)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text()
    print('text ', text)
    translated_text = translator.translate(text)
    print('translated_text: ', translated_text.text)
    return translated_text.text

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

for index, url in enumerate(urlList):
    try:
        text = fetchText(url)
        text = text.replace("\n", "") 
        print('text: ', text)
        if(detect(text) == 'en'):
            df = pd.DataFrame({'Index': index,'URL': url, 'Data': text}, index=[index])
            print('df', df)
            df.to_csv('data.csv', mode='a',index=False, header=False)
        else:
            raise Exception('other language')

    except Exception as e:
        print('error: ', e)
        df = pd.DataFrame({'Index': index,'URL': url}, index=[index])
        df.to_csv('failed.csv', mode='a',index=False, header=False)
        continue

