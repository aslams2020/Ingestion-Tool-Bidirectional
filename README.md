# Zeotap Bidirectional Data Ingestion Tool (Assignment 2) Solution 

Submitted By - Aslam Sayyad
Github - https://github.com/aslams2020
Linkedin - https://www.linkedin.com/in/aslamsayyad02/

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![ClickHouse](https://img.shields.io/badge/ClickHouse-24.3-yellow)
![Flask](https://img.shields.io/badge/Flask-2.3-green)

A solution for bidirectional data transfer between ClickHouse databases and flat files (CSV/TSV) with schema discovery capabilities.

1. **CSV to Table Ingestion**
   - Reads a CSV file.
   - Inserts the data into a specified database table (e.g., `uk_price_paid`).
   - Handles data parsing (e.g., types like `String`, `Date`, `UInt8`, etc.).

2. **Table to CSV Export**
   - Queries data from a specified table.
   - Writes the data into a CSV file (e.g., `output.csv`).
   - Includes headers in the exported file.

3. **Optional Transformations**
   - Ability to apply simple transformations (e.g., column filtering, row filtering).
   - Can be configured through parameters or options in the script.

4. **Command Line Interface (CLI)**
   - Should accept arguments/flags to:
     - Specify the CSV file path.
     - Choose between ingestion/export mode.
     - Specify database/table names.
     - Apply optional transformation rules.


### Technologies Used
- **Python 3.10+**
- **ClickHouse** (as the database)
- **ClickHouse Driver (`clickhouse-connect`)**
- **pandas** (for data manipulation and CSV handling)
- **argparse** (for CLI support)
- 
## Local Setup

```bash
# 1. Clone repository
git clone https://github.com/aslams2020/Ingestion-Tool-Bidirectional.git
cd Ingestion-Tool-Bidirectional

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start ClickHouse (Docker)
docker run -d \
  -p 9000:9000 \
  -p 8123:8123 \
  --name clickhouse-server \
  clickhouse/clickhouse-server

# 4. Load sample data
docker exec -it clickhouse-server \
  clickhouse-client --query "CREATE DATABASE IF NOT EXISTS uk_price_paid"

# 5. Run application
python backend/app.py

```


