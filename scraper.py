
import requests
from bs4 import BeautifulSoup
import json

data = {
    "headlines": [],
    "quotes": []
}

try:
    # Scrape headlines
    response = requests.get(
        "https://quotes.toscrape.com/",
        timeout=10
    )
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    for item in soup.select(".quote"):
        quote = item.select_one(".text")
        author = item.select_one(".author")

        if quote and author:
            data["quotes"].append({
                "quote": quote.get_text(strip=True),
                "author": author.get_text(strip=True)
            })

    # Scrape headlines from a practice news site
    response = requests.get(
        "https://www.bbc.com/news",
        timeout=10
    )
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    for item in soup.select("h2"):
        headline = item.get_text(strip=True)
        if headline and headline not in data["headlines"]:
            data["headlines"].append(headline)

    with open("scraped_data.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    print("Quotes found:", len(data["quotes"]))
    print("Headlines found:", len(data["headlines"]))
    print("Data saved to scraped_data.json")

except requests.RequestException as error:
    print("Website request failed:", error)
    
