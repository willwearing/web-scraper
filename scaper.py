import certifi
import ssl
from bs4 import BeautifulSoup
import urllib.request
import mongoscript as mongo
import URL_DATA as urls

headers = {'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.3'}

def fetchText(url):
    request = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(request, context=ssl.create_default_context(cafile=certifi.where()))
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text()
    return text

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
    # fetch text for each url
    text = fetchText(url)
    #  count words in each set of 'text' 
    # word_tally = count_words(text)
    # push url and word_tally to database
    mongo.load_data(url, text)
