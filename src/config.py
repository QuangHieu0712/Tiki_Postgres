
import os

from dotenv import load_dotenv

# Xác định thư mục gốc của project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Đọc thông tin từ file .env
load_dotenv(os.path.join(BASE_DIR, ".env"))

# Cấu hình kết nối PostgreSQL
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "port": os.getenv("DB_PORT", "5432")
}
