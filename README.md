# 📊 Excel to PostgreSQL ETL Pipeline

Automated ETL (Extract, Transform, Load) pipeline that reads Excel files, cleans the data, and loads it into a PostgreSQL database using Python and Pandas.

---

## 🚀 Project Overview

This project demonstrates a simple but powerful ETL pipeline:
- ✅ **Extract**: Load `.xlsx` files using `pandas` and `openpyxl`.
- 🧹 **Transform**: Clean column names, handle data types, remove missing/irrelevant data.
- 💾 **Load**: Insert the cleaned data into a PostgreSQL database using `SQLAlchemy`.

---

## 📁 Sample Excel File (Input)

> Contains mixed date formats, missing values, and inconsistent column names.

(![image](https://github.com/user-attachments/assets/1a3adbd6-7480-443d-924e-5ef8b4db63ce)
)
![image](https://github.com/user-attachments/assets/f80fd6b9-36fd-4cdb-8291-918398961355)


---

## 🛠️ Tech Stack

- Python 🐍
- Pandas
- openpyxl
- SQLAlchemy
- PostgreSQL 🐘

---

## 🧪 ETL Process Overview

```python
# Extract
df = pd.read_excel("data.xlsx")

# Transform
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
df['date_joined'] = pd.to_datetime(df['date_joined'], errors='coerce')
df = df.dropna(subset=['id'])

# Load
df.to_sql("employees", con=engine, if_exists='append', index=False)
