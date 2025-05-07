import requests
import psycopg2

# --- Database Connection ---
def get_db_connection():
    db = psycopg2.connect(
        host="dpg-d0cqpvadbo4c73fo4hig-a.oregon-postgres.render.com",
        database="hypewavesdb",
        user="hypewavesdb_user",
        password="lOSeA01nDkFq1qUOxvBW3G4EpD7WUN9C",
        port=5432
    )
    return db

# --- Fetch Inshorts News ---
def fetch_inshorts_news():
    try:
        url = "https://inshortsapi.vercel.app/news?category=all"
        response = requests.get(url)
        data = response.json()

        if data['success']:
            news_list = data['data']
            
            db = get_db_connection()
            cursor = db.cursor()

            for news in news_list:
                title = news['title']
                content = news['content']
                image_url = news['imageUrl']
                category = news['category']

                # Check duplicate title
                cursor.execute('SELECT * FROM articles WHERE title = %s', (title,))
                if cursor.fetchone() is None:
                    cursor.execute(
                        'INSERT INTO articles (title, content, category, image_url) VALUES (%s, %s, %s, %s)',
                        (title, content, category, image_url)
                    )
                    print(f"Inserted: {title}")
            
            db.commit()
            cursor.close()
            db.close()
        
        else:
            print("No news found from Inshorts API")

    except Exception as e:
        print(f"Error fetching news: {e}")

# --- Run ---
if __name__ == "__main__":
    fetch_inshorts_news()
