
import json
from pathlib import Path


# Xác định thư mục gốc của project
BASE_DIR = Path(__file__).resolve().parent.parent

# Đường dẫn đến thư mục chứa các file JSON
DATA_DIR = BASE_DIR / "data"


def read_json_files():
    total_products = 0

    try:
        # Kiểm tra thư mục data có tồn tại không
        if not DATA_DIR.exists():
            raise FileNotFoundError(f"Data directory not found: {DATA_DIR}")

        # Lấy danh sách tất cả file JSON
        json_files = sorted(DATA_DIR.glob("*.json"))

        if not json_files:
            print("No JSON files found!")
            return

        # Đọc từng file JSON
        for file_path in json_files:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    products = json.load(file)

                # Kiểm tra dữ liệu JSON có phải danh sách không
                if not isinstance(products, list):
                    raise ValueError("JSON data must be a list!")

                total_products += len(products)

                print(f"Successfully read: {file_path.name}")

            except FileNotFoundError:
                print(f"Error: File not found: {file_path.name}")

            except PermissionError:
                print(f"Error: Permission denied: {file_path.name}")

            except json.JSONDecodeError as e:
                print(f"Error: Invalid JSON in {file_path.name}: {e}")

            except UnicodeDecodeError as e:
                print(f"Error: Encoding error in {file_path.name}: {e}")

            except ValueError as e:
                print(f"Error: Invalid data in {file_path.name}: {e}")

            except OSError as e:
                print(f"File error in {file_path.name}: {e}")

        print("--------------------------------")
        print(f"Total JSON files: {len(json_files)}")
        print(f"Total products read: {total_products}")

    except FileNotFoundError as e:
        print(f"Error: {e}")

    except PermissionError as e:
        print(f"Error: Permission denied: {e}")

    except OSError as e:
        print(f"System error: {e}")


if __name__ == "__main__":
    read_json_files()
