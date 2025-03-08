import psycopg2
import os
import logging
from dags.tasks.transform_data import transform_and_enrich_data
from dotenv import load_dotenv

load_dotenv('config/.env')

# Load database connection from environment variables
DB_CONN = os.getenv("DB_CONN")

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def load_to_postgres():
    """
    Loads transformed book data into PostgreSQL.
    Skips records with missing ISBN and logs inserted records.
    """
    books = transform_and_enrich_data()
    
    if not books:
        logging.warning("No books to insert. Skipping database load.")
        return

    try:
        conn = psycopg2.connect(DB_CONN)
        cur = conn.cursor()

        inserted_count = 0

        for book in books:
            if not book["isbn"]:
                logging.warning(f"Skipping book '{book['title']}' due to missing ISBN.")
                continue

            # ✅ Ensure `categories` exists and format as PostgreSQL array
            categories = book.get("categories", [])
            if isinstance(categories, list):
                categories = "{" + ",".join([c.replace(",", "").replace(" ", "_") for c in categories]) + "}"
            else:
                categories = "{}"

            # ✅ Ensure `buy_links` exists and format as PostgreSQL array
            buy_links = book.get("buy_links", [])
            if isinstance(buy_links, list):
                buy_links = "{" + ",".join([f'"{link}"' for link in buy_links]) + "}"
            else:
                buy_links = "{}"

            cur.execute("""
                INSERT INTO books (
                    title, author, isbn, rank, list_name, weeks_on_list, publisher, published_date,
                    page_count, genres, language, average_rating, ratings_count, cover_image_url,
                    buy_links, data_source, ingested_at
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
                ON CONFLICT (isbn) DO NOTHING;
            """, (
                book["title"], book["author"], book["isbn"], book["rank"], book["list_name"],
                book["weeks_on_list"], book["publisher"], book["published_date"],
                book["page_count"], categories, book["language"], book["average_rating"],
                book["ratings_count"], book.get("cover_image", None), buy_links, "NYTimes, OpenLibrary, GoogleBooks"
            ))

            inserted_count += 1

        conn.commit()
        cur.close()
        conn.close()

        logging.info(f"Successfully inserted {inserted_count} books into PostgreSQL.")

    except Exception as e:
        logging.error(f"Database insert failed: {e}")
