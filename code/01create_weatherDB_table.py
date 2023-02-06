#creating Postgresql DB Table using this script 

import psycopg2

#connect DB

conn = psycopg2.connect(
    host="localhost",
    database="weather_data",
    user="postgres",
    password="password"
)

#create table colums

cursor = conn.cursor()

table_create_query = """
CREATE TABLE IF NOT EXISTS weather_data (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    station VARCHAR(255) NOT NULL,
    max_temp FLOAT NOT NULL,
    min_temp FLOAT NOT NULL,
    precipitation FLOAT NOT NULL
);
"""

cursor.execute(table_create_query)
conn.commit()

#avoid data replica

unique_constraint_query = """
ALTER TABLE weather_data
ADD CONSTRAINT weather_data_unique_constraint UNIQUE (date, station);
"""
cursor.execute(unique_constraint_query)
conn.commit()

cursor.close()
conn.close()
