import requests
import psycopg2

db = psycopg2.connect(
    host="dpg-d0cqpvadbo4c73fo4hig-a.oregon-postgres.render.com",
    database="hypewavesdb",
    user="hypewavesdb_user",
    password="lOSeA01nDkFq1qUOxvBW3G4EpD7WUN9C",
    port=5432
)
cursor = db.cursor()

url = "https://inshorts.deta.dev/news?category=technology"

try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()

    if data.get('success'):
        for article in data['data']:
            title = article.get('title')
            content = article.get('content')
            image_url = article.get('imageUrl', '')
            category = "tech"

            try:
                cursor.execute(
                    'INSERT INTO articles (title, content, category, image_url) VALUES (%s, %s, %s, %s)',
                    (title, content, category, image_url)
                )
                db.commit()
                print(f"Inserted: {title}")
            except Exception as e:
                db.rollback()
                print(f"Database error: {e}")
    else:
        print("No articles fetched.")

except requests.RequestException as e:
    print(f"Error fetching news: {e}")

cursor.close()
db.close()
