# news_scheduler.py
import feedparser
import psycopg2
import schedule
import time
from config import get_db_connection

def fetch_and_save_news():
    print("Fetching latest news...")

    feed_url = "https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en"
    feed = feedparser.parse(feed_url)

    conn = get_db_connection()
    cursor = conn.cursor()

    default_image_url = "https://via.placeholder.com/800x400.png?text=+News"

    for entry in feed.entries:
        title = entry.title
        link = entry.link
        summary = entry.summary
        published = entry.published

        if len(title) > 80:
            title = title[:77] + "..."

        content = f"{summary} <br><br> Read More: <a href='{link}' target='_blank'>Click Here</a>"
        image_url = default_image_url
        category = "news"

        try:
            cursor.execute("SELECT id FROM articles WHERE title = %s", (title,))
            if cursor.fetchone():
                continue

            cursor.execute(
                'INSERT INTO articles (title, content, category, image_url) VALUES (%s, %s, %s, %s)',
                (title, content, category, image_url)
            )
            conn.commit()
        except Exception as e:
            print(f"Error inserting news: {e}")
            conn.rollback()

    cursor.close()
    conn.close()
    print("News fetching completed!")

schedule.every(1).hours.do(fetch_and_save_news)

if __name__ == "__main__":
    fetch_and_save_news()
    while True:
        schedule.run_pending()
        time.sleep(60)
