# fetch_and_save_videos.py

import requests
import schedule
import time
from config import get_db_connection

API_KEY = "AIzaSyCw_Aa7AKrXLxUrduYFviuMWHZRJ2Zvtjc"  # Apni wali API Key

YOUTUBE_API_URL = f"https://youtube.googleapis.com/youtube/v3/videos?part=snippet&chart=mostPopular&regionCode=IN&maxResults=10&key={API_KEY}"

def fetch_and_save_videos():
    print("Fetching Viral Videos...")

    response = requests.get(YOUTUBE_API_URL)
    data = response.json()

    conn = get_db_connection()
    cursor = conn.cursor()

    if 'items' in data:
        for item in data['items']:
            video_id = item['id']
            title = item['snippet']['title']
            description = item['snippet']['description']
            thumbnail_url = item['snippet']['thumbnails']['high']['url']
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            category = 'video'

            # Duplicate check
            cursor.execute('SELECT * FROM articles WHERE title=%s', (title,))
            exists = cursor.fetchone()

            if not exists:
                try:
                    cursor.execute('INSERT INTO articles (title, content, category, image_url) VALUES (%s, %s, %s, %s)', 
                                   (title, video_url, category, thumbnail_url))
                    conn.commit()
                    print(f"✅ Added Video: {title}")
                except Exception as e:
                    conn.rollback()
                    print(f"❌ Error inserting video: {e}")
            else:
                print(f"⚡ Video Already Exists: {title}")

    cursor.close()
    conn.close()
    print("Finished fetching videos!\n")

# Scheduler setup
schedule.every(6).hours.do(fetch_and_save_videos)

if __name__ == "__main__":
    fetch_and_save_videos()
    while True:
        schedule.run_pending()
        time.sleep(60)
