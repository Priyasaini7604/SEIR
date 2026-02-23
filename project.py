
import sys
import requests
from bs4 import BeautifulSoup

# Check if URL is provided
if len(sys.argv) < 2:
    print("Please provide a URL")
    sys.exit()

url = sys.argv[1]

# Add header to avoid blocking
headers = {
    "User-Agent": "Mozilla/5.0"
}

# Fetch page
response = requests.get(url, headers=headers)

# Parse HTML
document = BeautifulSoup(response.text, "html.parser")

# 1. Print Page Title
if document.title:
    print(document.title.get_text(strip=True))
else:
    print("No Title Found")

# 2. Print Page Body (only text)
if document.body:
    body_text = document.body.get_text(separator=" ", strip=True)
    print(body_text)
else:
    print("No Body Found")

# 3. Print All Links
for tag in document.find_all("a"):
    link = tag.get("href")
    if link:
        print(link)




