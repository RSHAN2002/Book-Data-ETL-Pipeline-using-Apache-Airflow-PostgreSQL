import requests
import os
import logging
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor

load_dotenv('config/.env')

NYTIMES_API_KEY = os.getenv("NYTIMES_API_KEY")
GOOGLE_BOOKS_API_KEY = os.getenv("GOOGLE_BOOKS_API_KEY")

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def fetch_nytimes_books():
    url = f"https://api.nytimes.com/svc/books/v3/lists/current/hardcover-fiction.json?api-key={NYTIMES_API_KEY}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        books = [{
            "title": book.get("title"),
            "author": book.get("author"),
            "isbn": book.get("primary_isbn13"),
            "rank": book.get("rank"),
            "list_name": data["results"]["list_name"],
            "weeks_on_list": book.get("weeks_on_list"),
            "publisher": book.get("publisher"),
            "description": book.get("description"),
            "book_image": book.get("book_image"),
            "buy_links": [link["url"] for link in book.get("buy_links", [])]
        } for book in data["results"]["books"]]
        logging.info(f"NYTimes API: Fetched {len(books)} books successfully.")
        return books
    except requests.exceptions.RequestException as e:
        logging.error(f"NYTimes API request failed: {e}")
        return []

def fetch_openlibrary_data(isbn):
    url = f"https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd=data"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        if not data or f"ISBN:{isbn}" not in data:
            return None
        book_data = data[f"ISBN:{isbn}"]
        return {
            "title": book_data.get("title"),
            "author": book_data.get("authors", [{}])[0].get("name"),
            "publisher": book_data.get("publishers", [{}])[0].get("name"),
            "publish_date": book_data.get("publish_date"),
            "cover_image": book_data.get("cover", {}).get("large"),
            "genres": book_data.get("subjects", [])
        }
    except requests.exceptions.RequestException as e:
        logging.error(f"Open Library API request failed for ISBN {isbn}: {e}")
        return None

def fetch_google_books_data(isbn):
    url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}&key={GOOGLE_BOOKS_API_KEY}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        if "items" not in data:
            return None
        book_data = data["items"][0]["volumeInfo"]
        return {
            "title": book_data.get("title"),
            "author": book_data.get("authors", [None])[0],
            "publisher": book_data.get("publisher"),
            "published_date": book_data.get("publishedDate"),
            "page_count": book_data.get("pageCount"),
            "categories": book_data.get("categories", []),
            "language": book_data.get("language"),
            "average_rating": book_data.get("averageRating"),
            "ratings_count": book_data.get("ratingsCount"),
            "cover_image": book_data.get("imageLinks", {}).get("thumbnail")
        }
    except requests.exceptions.RequestException as e:
        logging.error(f"Google Books API request failed for ISBN {isbn}: {e}")
        return None

def fetch_combined_book_data():
    nytimes_books = fetch_nytimes_books()
    combined_books = []
    def fetch_extra_data(book):
        isbn = book["isbn"]
        return {
            "nytimes": book,
            "open_library": fetch_openlibrary_data(isbn),
            "google_books": fetch_google_books_data(isbn)
        }
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(fetch_extra_data, nytimes_books))
    for result in results:
        nytimes, open_library, google_books = result["nytimes"], result["open_library"], result["google_books"]
        combined_books.append({**nytimes, **(open_library or {}), **(google_books or {})})
    logging.info(f"Combined data for {len(combined_books)} books.")
    print(combined_books)
    return combined_books