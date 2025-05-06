# config.py
import psycopg2
import os

def get_db_connection():
    conn = psycopg2.connect(
        host="dpg-d0cqpvadbo4c73fo4hig-a.oregon-postgres.render.com",
        database="hypewavesdb",
        user="hypewavesdb_user",
        password="lOSeA01nDkFq1qUOxvBW3G4EpD7WUN9C",
        port="5432"
    )
    return conn
