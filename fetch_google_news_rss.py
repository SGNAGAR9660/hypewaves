import feedparser
import psycopg2

# --- Database Connection ---
def get_db_connection():
    db = psycopg2.connect(
        host="dpg-d0cqpvadbo4c73fo4hig-a.oregon-postgres.render.com",
        database="hypewavesdb",
        user="hypewavesdb_user",
        password="lOSeA01nDkFq1qUOxvBW3G4EpD7WUN9C",
        port=5432
    )
    return db

# --- Fetch Google News RSS ---
def fetch_google_news():
    rss_url = "https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en"  # India news feed
    feed = feedparser.parse(rss_url)
    
    db = get_db_connection()
    cursor = db.cursor()

    for entry in feed.entries:
        title = entry.title
        summary = entry.summary
        link = entry.link
        published = entry.published

        # Image URL nahi milta RSS se normally, to empty chodenge
        image_url = ''

        # Check duplicate title
        cursor.execute('SELECT * FROM articles WHERE title = %s', (title,))
        if cursor.fetchone() is None:
            cursor.execute(
                'INSERT INTO articles (title, content, category, image_url) VALUES (%s, %s, %s, %s)',
                (title, summary, 'news', image_url)
            )
            print(f"Inserted: {title}")
    
    db.commit()
    cursor.close()
    db.close()

# --- Run ---
if __name__ == "__main__":
    fetch_google_news()
