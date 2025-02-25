import time
import psycopg2
from config import Config

def wait_for_db():
    while True:
        try:
            conn = psycopg2.connect(Config.SQLALCHEMY_DATABASE_URI)
            conn.close()
            print("Database is ready!")
            break
        except Exception as e:
            print("Waiting for database...")
            time.sleep(2)

if __name__ == "__main__":
    wait_for_db()