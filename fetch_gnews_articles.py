# fetch_gnews_articles.py
import requests
import psycopg2
from config import get_db_connection

API_KEY = '0d63e809d8d6b8ac78315b2cb3cab866'  # Yahan apna actual API key daalna

def fetch_and_store_articles():
    url = f"https://gnews.io/api/v4/top-headlines?lang=en&country=in&max=10&apikey={API_KEY}"
    try:
        response = requests.get(url)
        data = response.json()

        if 'articles' in data:
            conn = get_db_connection()
            cursor = conn.cursor()
            for article in data['articles']:
                title = article['title']
                description = article['description']
                content = article.get('content', '')
                image_url = article['image']
                publishedAt = article['publishedAt']

                try:
                    cursor.execute('INSERT INTO articles (title, content, category, image_url) VALUES (%s, %s, %s, %s)',
                                   (title, content, 'news', image_url))
                    conn.commit()
                    print(f"Inserted: {title}")
                except Exception as e:
                    conn.rollback()
                    print(f"Error inserting article: {e}")
            cursor.close()
            conn.close()
        else:
            print("No articles found.")
    except Exception as e:
        print(f"Error fetching news: {e}")

if __name__ == "__main__":
    fetch_and_store_articles()
