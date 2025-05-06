import feedparser
import mysql.connector

# RSS feed URLs for different categories
rss_feeds = {
    "tech": "https://news.google.com/rss/search?q=technology&hl=en-IN&gl=IN&ceid=IN:en",
    "ai": "https://news.google.com/rss/search?q=artificial+intelligence&hl=en-IN&gl=IN&ceid=IN:en",
    "entertainment": "https://news.google.com/rss/search?q=entertainment&hl=en-IN&gl=IN&ceid=IN:en",
    "news": "https://news.google.com/rss/search?q=india+news&hl=en-IN&gl=IN&ceid=IN:en",
}

# MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Sparsh@9660",
    database="hypewaves"
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
