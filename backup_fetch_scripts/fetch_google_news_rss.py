import feedparser
import psycopg2

db = psycopg2.connect(
    host="dpg-d0cqpvadbo4c73fo4hig-a.oregon-postgres.render.com",
    database="hypewavesdb",
    user="hypewavesdb_user",
    password="lOSeA01nDkFq1qUOxvBW3G4EpD7WUN9C",
    port=5432
)
cursor = db.cursor()

rss_url = "https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en"
feed = feedparser.parse(rss_url)

for entry in feed.entries:
    title = entry.title
    link = entry.link
    summary = entry.summary
    category = "news"
    image_url = ""

    try:
        cursor.execute(
            'INSERT INTO articles (title, content, category, image_url) VALUES (%s, %s, %s, %s)',
            (title, summary, category, image_url)
        )
        db.commit()
        print(f"Inserted: {title}")
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")

cursor.close()
db.close()
