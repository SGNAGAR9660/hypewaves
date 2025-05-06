import feedparser
import psycopg2
import schedule
import time

def fetch_and_save_news():
    print("Fetching latest news...")

    feed_url = "https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en"
    feed = feedparser.parse(feed_url)

    # PostgreSQL Database Connection
    db = psycopg2.connect(
        host="dpg-d0cqpvadbo4c73fo4hig-a.oregon-postgres.render.com",
        database="hypewavesdb",
        user="hypewavesdb_user",
        password="lOSeA01nDkFq1qUOxvBW3G4EpD7WUN9C",
        port=5432
    )
    cursor = db.cursor()

    # Default image (अगर RSS में image नहीं हो)
    default_image_url = "https://via.placeholder.com/800x400.png?text=+News"

    for entry in feed.entries:
        title = entry.title
        link = entry.link
        summary = entry.summary
        published = entry.published

        # Shorten title if it's too long
        if len(title) > 80:
            title = title[:77] + "..."

        content = f"{summary} <br><br> Read More: <a href='{link}' target='_blank'>Click Here</a>"
        image_url = default_image_url
        category = "news"  # Default category

        try:
            # Duplicate Title check
            cursor.execute("SELECT id FROM articles WHERE title = %s", (title,))
            if cursor.fetchone():
                continue  # skip if already exists

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

# Scheduler: हर 1 घंटे में चलाना
schedule.every(1).hours.do(fetch_and_save_news)

if __name__ == "__main__":
    fetch_and_save_news()  # पहली बार चलते ही kaam हो जाए
    while True:
        schedule.run_pending()
        time.sleep(60)
