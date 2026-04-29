import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re

# CONFIGURATION
base_url = "http://books.toscrape.com/catalogue/page-{}.html"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115 Safari/537.36"
}
delay = 1.5

rating_map = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}

# CORE SCRAPER
def fetch_page(url):
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"[ERROR] Failed to fetch {url}: {e}")
        return None


def parse_books(html):
    soup = BeautifulSoup(html, "html.parser")
    books = soup.find_all("article", class_="product_pod")

    results = []

    for book in books:
        try:
            title = book.h3.a.get("title", "").strip()

            price_text = book.find("p", class_="price_color").text
            price = float(re.search(r"\d+\.\d+", price_text).group())

            rating_class = book.find("p", class_=re.compile("star-rating")).get("class")
            rating_word = next((c for c in rating_class if c in rating_map), None)
            rating = rating_map.get(rating_word, 0)

            results.append({
                "title": title,
                "price": price,
                "rating": rating
            })

        except Exception as e:
            print(f"[WARNING] Skipped item: {e}")

    return results


# Orchestration
def scrape_pages(total_pages):
    all_results = []

    for page in range(1, total_pages + 1):
        url = base_url.format(page)
        print(f"[INFO] Scraping page {page}...")

        html = fetch_page(url)
        if html:
            books = parse_books(html)
            all_results.extend(books)

        time.sleep(delay)

    return all_results


# EXPORTATION
def save_to_csv(data, filename="products.csv"):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False, encoding="utf-8")
    print(f"[SUCCESS] Data saved to {filename}")
    

def validate_data(data):
    """Remove invalid or incomplete records."""
    cleaned = []

    for item in data:
        if (
            item.get("title")
            and isinstance(item.get("price"), (int, float))
            and isinstance(item.get("rating"), int)
        ):
            cleaned.append(item)

    return cleaned


# MAIN
if __name__ == "__main__":

    try:
        pages = int(input("Enter number of pages to scrape: "))
        if pages <= 0:
            raise ValueError
    except ValueError:
        print("Invalid input. Using default = 1 page")
        pages = 1

    data = scrape_pages(pages)
    data = validate_data(data)

    if data:
        save_to_csv(data)
    else:
        print("[INFO] No valid data scraped.")        try:
            # Title
            title = book.h3.a.get("title", "").strip()

            # Price (convert to float)
            price_text = book.find("p", class_="price_color").text
            price_match = re.search(r"\d+\.\d+", price_text)
            price = float(price_match.group()) if price_match else 0

            # Rating (find the correct p tag with star-rating class)
            rating_p = book.find("p", class_=re.compile("star-rating"))
            if rating_p:
                classes = rating_p.get("class", [])
                rating_text = next((c for c in classes if c in rating_map), None)
                rating = rating_map.get(rating_text, 0)
            else:
                rating = 0

            data.append({
                "title": title,
                "price": price,
                "rating": rating
            })

        except (AttributeError, IndexError, ValueError) as e:
            print(f"Skipping item due to error: {e}")
            continue

    return data


def scrape_multiple_pages(pages=3):
    all_data = []

    for page in range(1, pages + 1):
        url = BASE_URL.format(page)
        print(f"Scraping page {page}...")
        data = scrape_page(url)
        all_data.extend(data)

        time.sleep(2)  # Be respectful to the server

    return all_data


if __name__ == "__main__":
    # Input validation
    while True:
        try:
            pages = int(input("Enter number of pages to scrape: "))
            if pages > 0:
                break
            print("Please enter a positive number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    results = scrape_multiple_pages(pages)

    if results:
        df = pd.DataFrame(results)
        df.to_csv("products.csv", index=False, encoding="utf-8")
        print("Done! Data saved to products.csv")
    else:
        print("No data scraped.")
