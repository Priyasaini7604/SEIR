import sys
import requests
from bs4 import BeautifulSoup
import re


def word_hashing(word):
    p = 53
    mod = 2**64
    h = 0
    power = 1

    for ch in word:
        h = (h + ord(ch) * power) % mod
        power = (power * p) % mod

    return h



def get_word_freq(url):
    
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    document = BeautifulSoup(response.text, "html.parser")

    if not document.body:
        return {}

    text = document.body.get_text()
    text = text.lower()

    words = re.findall(r"[a-z0-9]+", text)

    freq = {}

    for word in words:
        if word in freq:
            freq[word] += 1
        else:
            freq[word] = 1

    return freq



if len(sys.argv) < 3:
    print("Give two URLs in command line")
    sys.exit()

url1 = sys.argv[1]
url2 = sys.argv[2]

freq1 = get_word_freq(url1)
freq2 = get_word_freq(url2)

print("\nWord Frequency for URL 1:\n")
for word, count in freq1.items():
    print(word, ":", count)

print("\nWord Frequency for URL 2:\n")
for word, count in freq2.items():
    print(word, ":", count)

print("\nHash values for URL 1 words:\n")
for word in freq1:
    print(word, "->", word_hashing(word))

print("\nHash values for URL 2 words:\n")
for word in freq2:
    print(word, "->", word_hashing(word))


# Sir I had to complete 4 parts of the code, but I couldn’t do it. I have completed only 2 parts i did only wordfrequency and wordahshing.
