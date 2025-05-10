# fetch_and_save_news.py

import feedparser
import schedule
import time
from config import get_db_connection

def fetch_and_save_news():
    print("Fetching News...")

    # Example RSS Feed (Technology News)
    feed_url = 'https://news.google.com/rss/search?q=technology&hl=en-IN&gl=IN&ceid=IN:en'
    feed = feedparser.parse(feed_url)
    
    conn = get_db_connection()
    cursor = conn.cursor()

    for entry in feed.entries[:10]:  # Sirf top 10 news fetch kar rahe hain
        title = entry.title
        summary = entry.summary
        image_url = "https://via.placeholder.com/300x200"  # Future me image bhi RSS se le sakte hain
        category = 'tech'

        # Duplicate check (Simple Title Based)
        cursor.execute('SELECT * FROM articles WHERE title=%s', (title,))
        exists = cursor.fetchone()

        if not exists:
            try:
                cursor.execute('INSERT INTO articles (title, content, category, image_url) VALUES (%s, %s, %s, %s)',
                            (title, summary, category, image_url))
                conn.commit()
                print(f"✅ Added: {title}")
            except Exception as e:
                conn.rollback()
                print(f"❌ Error inserting article: {e}")
        else:
            print(f"⚡ Already Exists: {title}")

    cursor.close()
    conn.close()
    print("Finished fetching news!\n")

# Scheduler setup
schedule.every(6).hours.do(fetch_and_save_news)  # Har 6 ghante me news fetch karega

if __name__ == "__main__":
    fetch_and_save_news()  # Server start hone pe ek baar run
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute
