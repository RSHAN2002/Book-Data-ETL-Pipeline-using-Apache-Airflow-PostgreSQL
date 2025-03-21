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
