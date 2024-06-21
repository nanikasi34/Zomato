import sqlite3
import pandas as pd

# Database connection
conn = sqlite3.connect('zomato.db')
cursor = conn.cursor()

# Create table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS restaurants (
        Restaurant_ID INTEGER PRIMARY KEY,
        Restaurant_Name TEXT,
        Country_Code INTEGER,
        City TEXT,
        Address TEXT,
        Locality TEXT,
        Locality_Verbose TEXT,
        Longitude REAL,
        Latitude REAL,
        Cuisines TEXT,
        Average_Cost_for_two INTEGER,
        Currency TEXT,
        Has_Table_booking BOOLEAN,
        Has_Online_delivery BOOLEAN,
        Is_delivering_now BOOLEAN,
        Switch_to_order_menu BOOLEAN,
        Price_range INTEGER,
        Aggregate_rating REAL,
        Rating_color TEXT,
        Rating_text TEXT,
        Votes INTEGER
    )
''')

# Load data from CSV
df = pd.read_csv('zomato.csv',encoding='latin1')

# Insert data into table
df.to_sql('restaurants', conn, if_exists='replace', index=False)

# Verify table creation and data insertion
print("Tables in the database:")
tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
print(tables)

print("Number of rows in 'restaurants' table:")
count = cursor.execute("SELECT COUNT(*) FROM restaurants").fetchone()[0]
print(count)

conn.commit()
conn.close()
