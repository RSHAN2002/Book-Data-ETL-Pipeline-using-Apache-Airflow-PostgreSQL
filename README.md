# 📚 Book Data Pipeline

## 🚀 Overview
This project is an **ETL (Extract, Transform, Load) data pipeline** that fetches book data from multiple sources (**NYTimes API, OpenLibrary API, Google Books API**), processes it, and loads it into a **PostgreSQL** database using **Apache Airflow**.

## 🏗️ Project Structure
```
book_data_pipeline/
│── dags/                         # Airflow DAGs (ETL Workflow)
│   ├── book_pipeline.py          # Main DAG defining ETL tasks
│   ├── tasks/
│       ├── fetch_data.py         # Fetch book data from APIs
│       ├── transform_data.py     # Process and clean data
│       ├── load_data.py          # Load data into PostgreSQL
│       ├── data_quality.py       # Validate loaded data
│── db/                           # Database setup files
│   ├── init.sql                  # PostgreSQL schema
│── Dockerfile                    # Airflow Docker setup
│── docker-compose.yml            # Multi-container setup
│── config/                       # Configuration files
│   ├── .env                      # Environment variables
│── requirements.txt              # Dependencies
│── README.md                     # Documentation
```

---

## 🔧 Setup and Installation

### 1️⃣ **Clone the Repository**
```bash
git clone https://github.com/your-repo/book_data_pipeline.git
cd book_data_pipeline
```

### 2️⃣ **Set Up Environment Variables**
Create a `.env` file in the `config/` folder:
```
NYTIMES_API_KEY=your_nytimes_api_key
GOOGLE_BOOKS_API_KEY=your_google_books_api_key
DB_CONN=postgresql://postgres:1234@postgres:5432/books_db
```

### 3️⃣ **Run the Pipeline with Docker**

```bash
docker-compose up --build
```
This starts **PostgreSQL, Airflow Webserver, Scheduler, and Worker** containers.

```bash
docker-compose run --rm airflow-webserver airflow db init
```
This initilize the database if needed

```bash
docker-compose run --rm airflow-webserver airflow users create  --username admin --password admin123  --firstname Admin --lastname User --role Admin --email admin@example.com
```
This defines ***role and admin*** for airflow webserver

### 4️⃣ **Access Airflow UI**
📌 **URL:** [http://localhost:8080](http://localhost:8080)  
**Login:** Username: `admin` | Password: `admin123`

### 5️⃣ **Trigger the DAG**
- Navigate to `book_data_pipeline`
- Click **Trigger DAG** (▶️)

---

## 🛠️ How It Works
1️⃣ **Fetch Data** (`fetch_data.py`) - Collects book data from NYTimes, OpenLibrary, and Google Books.  
2️⃣ **Transform Data** (`transform_data.py`) - Cleans and enriches the data.  
3️⃣ **Load Data** (`load_data.py`) - Inserts data into PostgreSQL.  
4️⃣ **Validate Data** (`data_quality.py`) - Ensures data integrity.

---

## 📊 Database Schema (`init.sql`)
```sql
CREATE TABLE public.books (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    publisher TEXT DEFAULT 'Unknown Publisher',
    published_date TEXT,
    isbn TEXT UNIQUE NOT NULL,
    genres TEXT[],
    description TEXT,
    rank INT CHECK (rank >= 0),
    list_name TEXT,
    weeks_on_list INT CHECK (weeks_on_list >= 0),
    page_count INT CHECK (page_count >= 0),
    language TEXT DEFAULT 'Unknown',
    average_rating FLOAT CHECK (average_rating >= 0 AND average_rating <= 5),
    ratings_count INT CHECK (ratings_count >= 0),
    cover_image_url TEXT,
    buy_links TEXT[],
    data_source TEXT DEFAULT 'NYTimes, OpenLibrary, GoogleBooks',
    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🛠️ Debugging & Logs
📌 **Check Logs for Errors:**
```bash
docker logs -f book_data_pipeline-airflow-webserver-1
```

📌 **Check PostgreSQL Data:**
```bash
docker exec -it book_data_pipeline-postgres-1 psql -U postgres -d books_db -c "SELECT * FROM books LIMIT 5;"
```

---

## 🏁 Stopping & Restarting
To stop all services:
```bash
docker-compose down
```
To restart with fresh data:
```bash
docker-compose down
docker volume rm book_data_pipeline_postgres_data
docker-compose up --build
```

---

## 📝 Future Improvements
- Add more book data sources (e.g., Goodreads API)
- Implement automated email notifications for pipeline failures
- Enhance data quality checks (e.g., duplicate detection)

---

### 🚀 **Your ETL Pipeline is Ready!** 🎉
Let me know if you need further refinements! ✅

