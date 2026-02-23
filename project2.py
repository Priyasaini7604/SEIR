import sys
import requests
from bs4 import BeautifulSoup
import re

# 64-bit polynomial rolling hash
def word_hash(word):
    p = 53
    mod = 2**64
    h = 0
    power = 1

    for ch in word:
        h = (h + ord(ch) * power) % mod
        power = (power * p) % mod

    return h


# Get word frequency from URL
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


# Compute SimHash
def compute_simhash(freq):
    vector = [0] * 64

    for word, count in freq.items():
        h = word_hash(word)

        for i in range(64):
            if (h >> i) & 1:
                vector[i] += count
            else:
                vector[i] -= count

    simhash = 0
    for i in range(64):
        if vector[i] > 0:
            simhash |= (1 << i)

    return simhash


# Count common bits
def common_bits(h1, h2):
    xor = h1 ^ h2
    diff = bin(xor).count("1")
    return 64 - diff



if len(sys.argv) < 3:
    print("Give two URLs in command line")
    sys.exit()

url1 = sys.argv[1]
url2 = sys.argv[2]

freq1 = get_word_freq(url1)
freq2 = get_word_freq(url2)

#  PRINT WORD FREQUENCY
print("\nWord Frequency for URL 1:\n")
for word, count in freq1.items():
    print(word, ":", count)

print("\nWord Frequency for URL 2:\n")
for word, count in freq2.items():
    print(word, ":", count)

#  Compute SimHash
simhash1 = compute_simhash(freq1)
simhash2 = compute_simhash(freq2)

print("\nSimHash 1:", simhash1)
print("SimHash 2:", simhash2)


print("\nCommon bits:", common_bits(simhash1, simhash2))
