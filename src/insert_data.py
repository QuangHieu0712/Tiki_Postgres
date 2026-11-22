
import json
from pathlib import Path

import psycopg2
from psycopg2.extras import execute_values, Json

from src.connect import connect_db


# Xác định thư mục gốc của project
BASE_DIR = Path(__file__).resolve().parent.parent

# Đường dẫn đến thư mục chứa các file JSON
DATA_DIR = BASE_DIR / "data"


def insert_data():
    # Kết nối PostgreSQL
    conn = connect_db()

    if conn is None:
        print("Cannot insert data because database connection failed.")
        return

    cursor = None

    try:
        cursor = conn.cursor()

        # Kiểm tra thư mục data có tồn tại không
        if not DATA_DIR.is_dir():
            raise FileNotFoundError(f"Data directory not found: {DATA_DIR}")

        # Lấy danh sách tất cả file JSON
        json_files = sorted(DATA_DIR.glob("*.json"))

        if not json_files:
            print("No JSON files found!")
            return

        total_inserted = 0

        # Đọc và xử lý từng file JSON
        for file_path in json_files:
            print(f"Processing: {file_path.name}")

            try:
                # Đọc dữ liệu từ file JSON
                with open(file_path, "r", encoding="utf-8") as file:
                    products = json.load(file)

                # Kiểm tra dữ liệu JSON phải là danh sách
                if not isinstance(products, list):
                    raise ValueError("JSON data must be a list!")

                # Kiểm tra từng sản phẩm phải là dictionary
                if not all(isinstance(product, dict) for product in products):
                    raise ValueError("Each product must be a dictionary!")

                # Chuyển dữ liệu sản phẩm thành danh sách tuple
                values = []

                for product in products:
                    values.append((
                        product.get("id"),
                        product.get("name"),
                        product.get("url_key"),
                        product.get("price"),
                        product.get("description"),
                        Json(product.get("images", []))
                    ))

            except FileNotFoundError:
                print(f"Error: File not found: {file_path.name}")
                continue

            except PermissionError:
                print(f"Error: Permission denied: {file_path.name}")
                continue

            except json.JSONDecodeError as e:
                print(f"Error: Invalid JSON in {file_path.name}: {e}")
                continue

            except UnicodeDecodeError as e:
                print(f"Error: Encoding error in {file_path.name}: {e}")
                continue

            except (OSError, ValueError) as e:
                print(f"File processing error in {file_path.name}: {e}")
                continue

            # Bỏ qua nếu file không có sản phẩm
            if not values:
                print(f"No products found in {file_path.name}")
                continue

            # Câu lệnh thêm dữ liệu vào bảng
            query = """
                INSERT INTO tiki_products (
                    id,
                    name,
                    url_key,
                    price,
                    description,
                    images
                )
                VALUES %s
                ON CONFLICT (id) DO NOTHING
                RETURNING id;
            """

            try:
                # Thực hiện thêm nhiều sản phẩm cùng lúc
                inserted_rows = execute_values(
                    cursor,
                    query,
                    values,
                    fetch=True
                )

                # Lưu thay đổi vào database
                conn.commit()

                # Đếm chính xác số sản phẩm được thêm
                total_inserted += len(inserted_rows)

            except psycopg2.Error as e:
                # Hủy các thay đổi nếu Database gặp lỗi
                conn.rollback()
                print(f"Database error while inserting {file_path.name}: {e}")
                break

        print("--------------------------------")
        print(f"Total products inserted: {total_inserted}")

        try:
            # Kiểm tra tổng số sản phẩm trong Database
            cursor.execute("SELECT COUNT(*) FROM tiki_products")
            total_in_database = cursor.fetchone()[0]

            print(f"Total products in database: {total_in_database}")

        except psycopg2.Error as e:
            conn.rollback()
            print(f"Database query error: {e}")

    except FileNotFoundError as e:
        print(f"File error: {e}")

    except psycopg2.Error as e:
        conn.rollback()
        print(f"Database error: {e}")

    except Exception as e:
        conn.rollback()
        print(f"Unexpected error: {e}")

    finally:
        # Đóng cursor nếu đã được tạo
        if cursor is not None:
            cursor.close()

        # Đóng kết nối Database
        conn.close()


if __name__ == "__main__":
    insert_data()
