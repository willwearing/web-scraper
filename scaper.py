from bs4 import BeautifulSoup
import urllib.request


url = "https://routific.com/"

headers = {'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.3'}

# make call to url, pass in headers, else you will get a 403 error
req = urllib.request.Request(url, headers=headers)
data = urllib.request.urlopen(req).read()

# parse the data
soup = BeautifulSoup(data, "html.parser")

# extract the text from the html data
text = soup.get_text()

# count how many occurrences of each word are in the text and return the list in order of most to least

def word_count(str):
    counts = dict()
    words = str.split()

    for word in words:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1

    counts_sorted = sorted(counts.items(), key=lambda x: x[1], reverse=True)

    return counts_sorted

print(word_count(text))