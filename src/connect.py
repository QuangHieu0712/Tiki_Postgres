
import psycopg2

from src.config import DB_CONFIG


def connect_db():
    try:
        # Kết nối đến PostgreSQL
        conn = psycopg2.connect(**DB_CONFIG)

        print("PostgreSQL connection successful!")

        return conn

    except psycopg2.OperationalError as e:
        print(f"Database connection error: {e}")

    except psycopg2.Error as e:
        print(f"PostgreSQL error: {e}")

    except Exception as e:
        print(f"Unexpected error: {e}")

    return None
