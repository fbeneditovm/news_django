from psycopg import connect
from psycopg.errors import DuplicateDatabase
from environs import env

# Read .env file
env.read_env()

def create_database():
    new_db_name = env('DB_NAME', default='news_api')
    conn = connect(
        dbname='postgres',
        user=env('DB_USER', default='postgres'),
        password=env('DB_PASSWORD', default='postgres'),
        host=env('DB_HOST', default='localhost')
    )
    conn.autocommit = True

    try:
        cur = conn.cursor()
        cur.execute(f"CREATE DATABASE {new_db_name}")
        print(f"Database {new_db_name} created successfully")
    except DuplicateDatabase:
        print(f"Database {new_db_name} already exists")
    finally:
        conn.close()

if __name__ == "__main__":
    create_database()
