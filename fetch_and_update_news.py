import feedparser
import mysql.connector
import schedule
import time

# MySQL Database Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Sparsh@9660",
    database="hypewaves"
)

def fetch_and_store_news():
    print("Fetching latest news...")

    feed_url = "https://news.google.com/rss/search?q=technology+OR+AI+OR+entertainment+OR+latest&hl=en-IN&gl=IN&ceid=IN:en"
    feed = feedparser.parse(feed_url)

    for entry in feed.entries:
        title = entry.title
        link = entry.link
        summary = entry.summary if hasattr(entry, 'summary') else ''

        # Decide Category
        if 'tech' in title.lower() or 'technology' in title.lower():
            category = 'tech'
        elif 'ai' in title.lower() or 'artificial intelligence' in title.lower():
            category = 'ai'
        elif 'movie' in title.lower() or 'film' in title.lower() or 'entertainment' in title.lower():
            category = 'entertainment'
        else:
            category = 'news'

        try:
            cursor = db.cursor(buffered=True)  # 👈 cursor(buffered=True) important
            cursor.execute("SELECT id FROM articles WHERE title = %s", (title,))
            existing_article = cursor.fetchone()

            if existing_article is None:
                cursor.execute(
                    "INSERT INTO articles (title, content, image_url, video_url, category) VALUES (%s, %s, %s, %s, %s)",
                    (title, summary, '', '', category)
                )
                db.commit()
                print(f"Inserted: {title}")
            else:
                print(f"Already exists: {title}")

        except Exception as e:
            print(f"Error: {e}")
            db.rollback()

        finally:
            cursor.close()  # Important to close every cursor!

    print("Fetch Complete!\n")

# Schedule: Fetch every 1 hour
schedule.every(1).hours.do(fetch_and_store_news)

# --- Main Loop ---
print("News fetch scheduler started...")

schedule.run_all()

while True:
    schedule.run_pending()
    time.sleep(1)
