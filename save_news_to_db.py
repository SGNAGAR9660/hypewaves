import feedparser
import psycopg2

# RSS feed URLs for different categories
rss_feeds = {
    "tech": "https://news.google.com/rss/search?q=technology&hl=en-IN&gl=IN&ceid=IN:en",
    "ai": "https://news.google.com/rss/search?q=artificial+intelligence&hl=en-IN&gl=IN&ceid=IN:en",
    "entertainment": "https://news.google.com/rss/search?q=entertainment&hl=en-IN&gl=IN&ceid=IN:en",
    "news": "https://news.google.com/rss/search?q=india+news&hl=en-IN&gl=IN&ceid=IN:en",
}

db = psycopg2.connect(
    host="dpg-d0cqpvadbo4c73fo4hig-a.oregon-postgres.render.com",
    database="hypewavesdb",
    user="hypewavesdb_user",
    password="lOSeA01nDkFq1qUOxvBW3G4EpD7WUN9C",
    port="5432"
)

cursor = db.cursor()

def fetch_and_save(category, url):
    feed = feedparser.parse(url)
    for entry in feed.entries:
        title = entry.title
        content = entry.summary
        image_url = ""  # RSS feeds usually don't have image, abhi blank rakho
        try:
            cursor.execute('INSERT INTO articles (title, content, category, image_url) VALUES (%s, %s, %s, %s)',
                           (title, content, category, image_url))
            db.commit()
            print(f"Saved: {title}")
        except Exception as e:
            print(f"Error saving {title}: {e}")
            db.rollback()

for category, url in rss_feeds.items():
    fetch_and_save(category, url)

cursor.close()
db.close()
