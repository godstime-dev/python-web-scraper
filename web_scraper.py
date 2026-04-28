import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_website(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("Error fetching page:", e)
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    # Generic extraction (works for many demo/e-commerce sites)
    items = soup.find_all("h3")

    data = []

    for item in items:
        title = item.get_text(strip=True)
        data.append({"title": title})

    return data


# Main execution block
if __name__ == "__main__":
    url = input("Enter website URL: ")

    results = scrape_website(url)

    if results:
        df = pd.DataFrame(results)
        df.to_csv("output.csv", index=False)
        print("Done! File saved as output.csv")
    else:
        print("No data scraped.")