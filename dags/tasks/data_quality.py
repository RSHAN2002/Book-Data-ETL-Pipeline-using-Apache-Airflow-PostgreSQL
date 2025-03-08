import psycopg2
import os
import logging
from dotenv import load_dotenv

load_dotenv('config/.env')

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Get DB connection details from environment variables
DB_CONN = os.getenv("DB_CONN")

def data_quality_checks():
    """
    Perform data completeness, consistency, and quality checks on the books data stored in PostgreSQL.
    """

    try:
        conn = psycopg2.connect(DB_CONN)  # 
        cur = conn.cursor()
    
        logging.info("Starting Data Quality Checks...")

        # Check if the books table has any records
        cur.execute("SELECT COUNT(*) FROM books;")
        row_count = cur.fetchone()[0]
        if row_count == 0:
            logging.warning("Data Quality Check Failed: No records found in books table!")
        else:
            logging.info(f"Data Quality Check Passed: Found {row_count} records in books table.")

        # Check for missing critical fields
        critical_columns = ["title", "author", "isbn", "publisher", "published_date"]
        for column in critical_columns:
            cur.execute(f"SELECT COUNT(*) FROM books WHERE {column} IS NULL OR {column} = '';")
            missing_count = cur.fetchone()[0]
            if missing_count > 0:
                logging.warning(f"Data Quality Check Failed: {missing_count} records missing '{column}'.")
            else:
                logging.info(f"Data Quality Check Passed: No missing values in '{column}'.")

        # Check for duplicate ISBNs
        cur.execute("""
            SELECT isbn, COUNT(*) FROM books
            GROUP BY isbn
            HAVING COUNT(*) > 1;
        """)
        duplicates = cur.fetchall()
        if duplicates:
            logging.warning(f"Data Quality Check Failed: Found {len(duplicates)} duplicate ISBNs!")
        else:
            logging.info("Data Quality Check Passed: No duplicate ISBNs found.")

        # Check for invalid numerical values
        numeric_checks = {
            "rank": "rank < 0",
            "weeks_on_list": "weeks_on_list < 0",
            "page_count": "page_count < 0",
            "average_rating": "average_rating < 0 OR average_rating > 5",
            "ratings_count": "ratings_count < 0"
        }

        for column, condition in numeric_checks.items():
            cur.execute(f"SELECT COUNT(*) FROM books WHERE {condition};")
            invalid_count = cur.fetchone()[0]
            if invalid_count > 0:
                logging.warning(f"Data Quality Check Failed: {invalid_count} records with invalid '{column}' values.")
            else:
                logging.info(f"Data Quality Check Passed: No invalid '{column}' values.")

        logging.info("Data Quality Checks Completed!")

        cur.close()
        conn.close()

    except Exception as e:
        logging.error(f"Data Quality Check failed: {e}")

