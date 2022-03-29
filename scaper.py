import certifi
import ssl
from bs4 import BeautifulSoup
import urllib.request
from urllib.error import URLError, HTTPError
import mongoscript as mongo
import URL_DATA as urls

headers = {'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.3'}

def fetchText(url):
    request = urllib.request.Request(url, headers=headers)
    print(request.__dict__)
    try:
        response = urllib.request.urlopen(request, context=ssl.create_default_context(cafile=certifi.where()))
        print(response.__dict__)
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')
        text = soup.get_text()
        return text
    except HTTPError as e:
        print('Error code: ', e.code)
        return None
    except URLError as e:
        print('Reason: ', e.reason)
        return None


# def count_words(str):
#     counts = dict()
#     words = str.split()

#     for word in words:
#         if word in counts:
#             counts[word] += 1
#         else:
#             counts[word] = 1

#     counts_sorted = sorted(counts.items(), key=lambda x: x[1], reverse=True)

#     return counts_sorted

for url in urls:
    text = fetchText(url)
    # word_tally = count_words(text)
    mongo.load_data(url, text)
    # mongo.load_data(url, word_tally)
