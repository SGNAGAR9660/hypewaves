import feedparser
import mysql.connector
import schedule
import time

def fetch_and_save_news():
    print("Fetching latest news...")

    feed_url = "https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en"
    feed = feedparser.parse(feed_url)

    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Sparsh@9660",
        database="hypewaves"
    )
    cursor = db.cursor()

    # Default image (agar RSS me image nahi hoti)
    default_image_url = "https://via.placeholder.com/800x400.png?text=Hypewaves+News"

    for entry in feed.entries:
        title = entry.title
        link = entry.link
        summary = entry.summary
        published = entry.published

        # Shorten title if it's too long
        if len(title) > 80:
            title = title[:77] + "..."

        # Final values
        content = f"{summary} <br><br> Read More: <a href='{link}' target='_blank'>Click Here</a>"
        image_url = default_image_url
        category = "news"  # Abhi sabko default "news" category de rahe hain

        try:
            # Duplicate Title check karlo (optional)
            cursor.execute("SELECT id FROM articles WHERE title = %s", (title,))
            if cursor.fetchone():
                continue  # Skip agar already hai

            cursor.execute(
                'INSERT INTO articles (title, content, category, image_url) VALUES (%s, %s, %s, %s)',
                (title, content, category, image_url)
            )
            db.commit()
        except Exception as e:
            print(f"Error inserting news: {e}")
            db.rollback()

    cursor.close()
    db.close()
    print("News fetching completed!")

# Scheduler: Har 1 ghante me news update
schedule.every(1).hours.do(fetch_and_save_news)

if __name__ == "__main__":
    fetch_and_save_news()
    while True:
        schedule.run_pending()
        time.sleep(60)
