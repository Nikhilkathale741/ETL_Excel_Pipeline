import pandas as pd
import sqlalchemy
import logging


# -------------------- Logging Setup --------------------
logging.basicConfig(
    filename='etl_log.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# -------------------- Config --------------------
EXCEL_FILE = 'sample_dirty_data.xlsx'  # Replace with your actual file name
TABLE_NAME = 'employees'
DATE_COLUMNS = ['date_joined']  # Update according to your sheet
POSTGRES_URI = 'postgresql://postgres:1234@localhost:5432/excel_pipeline'




# -------------------- Extract --------------------
try:
    logging.info("Step 1: Reading Excel file...")
    df = pd.read_excel(EXCEL_FILE, engine='openpyxl')
    logging.info(f"Excel file read successfully. Rows: {len(df)} Columns: {len(df.columns)}")
except Exception as e:
    logging.error(f"Error reading Excel file: {e}")
    raise

# -------------------- Transform --------------------
try:
    # Clean column names: lower case, no spaces
    df.columns = [col.strip().lower().replace(' ', '_') for col in df.columns]
    logging.info("Column names cleaned.")

    # Convert and format date columns
    for col in DATE_COLUMNS:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
            df[col] = df[col].dt.strftime('%d-%m-%y')
            logging.info(f"Formatted date column '{col}' to DD-MM-YY format.")

    # Example cleanup: drop rows with missing values in a key column
    if 'name' in df.columns:
        original_len = len(df)
        df = df.dropna(subset=['name'])
        logging.info(f"Dropped rows with empty 'name'. Original: {original_len}, Remaining: {len(df)}")

except Exception as e:
    logging.error(f"Error during data transformation: {e}")
    raise

# -------------------- Load --------------------
try:
    logging.info("Step 3: Connecting to PostgreSQL...")
    engine = sqlalchemy.create_engine(POSTGRES_URI)
    df.to_sql(TABLE_NAME, engine, if_exists='replace', index=False)
    logging.info(f"Data loaded into PostgreSQL table '{TABLE_NAME}' successfully.")
except Exception as e:
    logging.error(f"Error loading data into PostgreSQL: {e}")
    raise

logging.info("ETL process completed successfully.")
