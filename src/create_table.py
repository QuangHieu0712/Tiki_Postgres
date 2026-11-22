from src.connect import connect_db


def create_table():
    conn = connect_db()

    if conn is None:
        return

    try:
        cursor = conn.cursor()

        create_table_query = """
            CREATE TABLE IF NOT EXISTS tiki_products (
                id BIGINT PRIMARY KEY,
                name TEXT,
                url_key TEXT,
                price BIGINT,
                description TEXT,
                images JSONB
            );
        """

        cursor.execute(create_table_query)
        conn.commit()

        print("Tao bang tiki_products thanh cong!")

    except Exception as e:
        conn.rollback()
        print(f"Loi khi tao bang: {e}")

    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    create_table()
