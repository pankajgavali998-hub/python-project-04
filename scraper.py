import requests
from bs4 import BeautifulSoup
import json

url = "https://quotes.toscrape.com/"

try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    quotes = []

    for item in soup.select(".quote"):
        text = item.select_one(".text")
        author = item.select_one(".author")

        if text and author:
            quotes.append({
                "quote": text.get_text(strip=True),
                "author": author.get_text(strip=True)
            })

    with open("quotes.json", "w", encoding="utf-8") as file:
        json.dump(quotes, file, indent=4, ensure_ascii=False)

    print(f"Saved {len(quotes)} quotes to quotes.json")

except requests.RequestException as error:
    print("Website request failed:", error)
