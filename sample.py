import pandas as pd 
from sqlalchemy import create_engine

#connection to database
DB_URI = "postgresql+psycopg2://postgres:1234@localhost:5432/excel_pipeline"
engine = create_engine(DB_URI)


#Connecting csv file
file_path = "sample_dirty_data.xlsx"
df = pd.read_excel(file_path, engine='openpyxl')



# Clean the Data,Normalize column names
df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]
df.dropna(how="all", inplace=True)  # Drop completely empty rows
df.drop_duplicates(inplace=True)    # Drop duplicate rows

# Step 4: Replace NaNs with 'NA'
df.fillna("NA", inplace=True)

#keeping all the date format same
if 'joining_date' in df.columns:
    df['joining_date'] = pd.to_datetime(df['joining_date'], errors='coerce')

# Insert into PostgreSQL
table_name = "employees"

df.to_sql(table_name, con=engine, if_exists='replace', index=False)


print(f"✅ Successfully inserted {len(df)} rows into table '{table_name}'")
