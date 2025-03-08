import logging
from dags.tasks.fetch_data import fetch_combined_book_data
from dotenv import load_dotenv

load_dotenv('config/.env')

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def transform_and_enrich_data():
    """
    Transforms and enriches book data by merging information from multiple sources,
    handling missing fields, and ensuring schema consistency.
    """
    
    books = fetch_combined_book_data()

    if not books:
        logging.warning("No books data fetched. Transformation skipped.")
        return []

    transformed_books = []

    for book in books:
        transformed_book = {
            "title": book.get("title", "Unknown Title"),
            "author": book.get("author", "Unknown Author"),
            "isbn": book.get("isbn"),
            "rank": book.get("rank"),
            "list_name": book.get("list_name"),
            "weeks_on_list": book.get("weeks_on_list", 0),
            "publisher": book.get("publisher", "Unknown Publisher"),
            "published_date": book.get("published_date", "Unknown Date"),
            "page_count": book.get("page_count", 0),  # Ensure it's an integer
            "genres": ", ".join([genre.get("name", "Unknown") for genre in book.get("genres", [])]),  # Convert list to string
            "language": book.get("language", "Unknown"),
            "average_rating": book.get("average_rating", 0.0),  # Ensure it's a float
            "ratings_count": book.get("ratings_count", 0),  # Ensure it's an integer
            "cover_image_url": book.get("cover_image"),
            "buy_links": ", ".join(book.get("buy_links", [])),  # Convert list to string
            "description": book.get("description", "No description available"),
            "data_source": "NYTimes, OpenLibrary, GoogleBooks",
        }

        transformed_books.append(transformed_book)

    logging.info(f"Transformation complete: {len(transformed_books)} books processed.")
    return transformed_books
