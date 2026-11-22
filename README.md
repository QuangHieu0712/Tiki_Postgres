# Tiki Product Data - PostgreSQL

This project loads product data collected from Tiki into a PostgreSQL database using Python.

The project is divided into two labs. Lab 01 focuses on reading product data from JSON files and inserting it into PostgreSQL. Lab 02 extends Lab 01 by adding exception handling for file reading and database operations.

| Lab | Goal | Git Tag |
|---|---|---|
| Lab 01 | Read product JSON files and load data into PostgreSQL | `lab-01` |
| Lab 02 | Add exception handling for file reading and database operations | `lab-02` |

## 1. Project Overview

The main purpose of this project is to practice loading data from JSON files into a relational database.

The workflow consists of:

1. Reading product data from JSON files.
2. Processing product information using Python.
3. Connecting to PostgreSQL.
4. Creating the product table.
5. Inserting product records into PostgreSQL.
6. Handling file and database errors.

The source data contains product information collected from Tiki.

## 2. Project Structure

```text
Tiki_Postgres/
├── data/
│   └── products_*.json
│
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── connect.py
│   ├── test_con.py
│   ├── create_table.py
│   ├── load_data.py
│   └── insert_data.py
│
├── .gitignore
├── README.md
└── requirements.txt
```

### Source Code Description

| File | Description |
|---|---|
| `config.py` | Stores PostgreSQL connection configuration. |
| `connect.py` | Establishes a connection to PostgreSQL. |
| `test_con.py` | Tests the database connection. |
| `create_table.py` | Creates the `tiki_products` table. |
| `load_data.py` | Reads JSON files and counts product records. |
| `insert_data.py` | Reads product data and inserts it into PostgreSQL. |
| `requirements.txt` | Lists the Python dependencies. |

## 3. Technologies

- Python 3.12
- PostgreSQL
- Psycopg2
- JSON
- pathlib
- Python standard library

## 4. Database Design

**Database name:** `tiki_db`

**Table name:** `tiki_products`

The table stores the following product information:

| Column | Data Type | Description |
|---|---|---|
| `id` | BIGINT | Product ID and primary key |
| `name` | TEXT | Product name |
| `url_key` | TEXT | Product URL key |
| `price` | BIGINT | Product price |
| `description` | TEXT | Product description |
| `images` | JSONB | List of product image URLs |

### Design Decisions

- `id` is the PRIMARY KEY to ensure that each product has a unique identifier.
- `ON CONFLICT (id) DO NOTHING` prevents duplicate products from being inserted.
- `images` uses PostgreSQL `JSONB` to preserve the list structure of image URLs.
- `execute_values` is used to insert multiple products in batches instead of inserting records one by one.

## 5. Installation

Clone the repository:

```bash
git clone https://github.com/QuangHieu0712/Tiki_Postgres
```

Navigate to the project directory:

```bash
cd Tiki_Postgres
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment in Git Bash:

```bash
source .venv/Scripts/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## 6. Configuration

Configure the PostgreSQL connection in `src/config.py`.

The connection configuration includes:

- Host
- Database name
- Username
- Password
- Port

Make sure PostgreSQL is running and the `tiki_db` database has been created before running the project.

**Security note:** Database credentials should not be committed to GitHub. Use environment variables or a local `.env` file excluded by `.gitignore` to store sensitive configuration.

## 7. How to Run

Run commands from the project root directory.

### Step 1: Test PostgreSQL Connection

```bash
python -m src.test_con
```

### Step 2: Create the Database Table

```bash
python -m src.create_table
```

### Step 3: Read JSON Files

```bash
python -m src.load_data
```

This script reads all JSON files in the `data` directory and calculates the total number of product records.

### Step 4: Insert Data into PostgreSQL

```bash
python -m src.insert_data
```

This script reads product information from JSON files and inserts it into the `tiki_products` table.

## 8. Lab 01 - Load JSON Data into PostgreSQL

### Objective

Read all product JSON files and load their data into a PostgreSQL database using Python.

### Implementation

Lab 01 consists of the following main tasks:

1. Read all JSON files from the `data` directory.
2. Parse JSON data using Python's `json` module.
3. Extract product information:
   - `id`
   - `name`
   - `url_key`
   - `price`
   - `description`
   - `images`
4. Connect to PostgreSQL using Psycopg2.
5. Create the `tiki_products` table.
6. Insert product records using `execute_values`.
7. Commit database transactions.

### Data Loading Strategy

The loader processes JSON files one at a time.

Product records are converted into tuples before being inserted into PostgreSQL.

The `ON CONFLICT (id) DO NOTHING` clause prevents duplicate records when the loader is executed multiple times.

### Results

- Total JSON files: 125
- Total products read: 124,298
- Total products in PostgreSQL: 124,298
- Duplicate product IDs: 0

The database was checked to confirm that all 124,298 product records were loaded successfully.

## 9. Lab 02 - Exception Handling

### Objective

Extend Lab 01 by adding exception handling for file reading and database operations.

The purpose is to make the data-loading process more reliable and easier to troubleshoot when errors occur.

### File Reading Exception Handling

The project handles errors that may occur while reading JSON files.

| Exception | Description | Behavior |
|---|---|---|
| `FileNotFoundError` | File or data directory does not exist | Display an error message |
| `PermissionError` | No permission to read the file | Report the error |
| `json.JSONDecodeError` | Invalid JSON format | Skip the affected file |
| `UnicodeDecodeError` | File encoding error | Skip the affected file |
| `OSError` | Other file system errors | Report the error |
| `ValueError` | JSON data has an invalid structure | Skip the affected file |

### Database Exception Handling

Database operations also include exception handling.

| Exception | Description | Behavior |
|---|---|---|
| `psycopg2.OperationalError` | Database connection or operational error | Display connection error |
| `psycopg2.Error` | PostgreSQL-related error | Roll back the transaction and report the error |
| `Exception` | Unexpected error | Display an error message |

### Transaction Management

The project uses two important database methods:

- `conn.commit()`: Saves successfully inserted records.
- `conn.rollback()`: Cancels the current transaction when a database error occurs.

The database cursor and connection are closed in the `finally` block to release resources.

### File and Database Error Handling Strategy

The implementation follows these principles:

- If a JSON file cannot be read or has invalid data, report the error and continue processing the next file.
- If a database insertion operation fails, roll back the transaction and stop further insertion.
- If the database connection fails, do not continue with insertion.
- Always close database resources after processing.

### Additional Improvements

Compared with Lab 01, Lab 02 includes:

- Specific exception handling for JSON file reading.
- Validation of JSON data structure.
- Exception handling for PostgreSQL connection errors.
- Exception handling for database insertion and query operations.
- Transaction rollback when database errors occur.
- Safe cursor and connection cleanup.

## 10. Verification

The project can be verified using the following PostgreSQL queries.

### Check Total Products

```sql
SELECT COUNT(*)
FROM tiki_products;
```

Expected result after the initial successful load:

```text
124298
```

### Check Duplicate Product IDs

```sql
SELECT id, COUNT(*)
FROM tiki_products
GROUP BY id
HAVING COUNT(*) > 1;
```

Expected result: No rows.

### Check Product Data

```sql
SELECT *
FROM tiki_products
LIMIT 10;
```

## 11. Conclusion

Through these two labs, the project demonstrates a basic data-loading workflow using Python and PostgreSQL.

Lab 01 focuses on reading JSON files, processing product information, and inserting records into PostgreSQL.

Lab 02 improves the reliability of the workflow by introducing exception handling for file reading and database operations.

These labs provide practical experience with Python file handling, PostgreSQL connectivity, batch insertion, database transactions, and error handling.
