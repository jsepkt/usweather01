import os
import psycopg2
import time
from datetime import datetime


start_time = time.time() 
records_ingested = 0 

#connecting database from Postgresql

conn = psycopg2.connect(
    host="localhost",
    database="weather_data",
    user="postgres",
    password="password"
)

#Loading data from wx folder to DB

cursor = conn.cursor()

start_time = datetime.now()
print(f"Started at: {start_time}")

for filename in os.listdir(r"C:\usweather\code\wx_data"):
    if filename.endswith(".txt"):
        station = filename.split(".")[0]
        with open(os.path.join(r"C:\usweather\code\wx_data", filename)) as f:
            for line in f:
                date, max_temp, min_temp, precipitation = line.strip().split("\t")
                max_temp = float(max_temp) / 10
                min_temp = float(min_temp) / 10
                precipitation = float(precipitation) / 10

                # Check if a record with the same date and station exists
                cursor.execute("SELECT * FROM weather_data WHERE date=%s AND station=%s", (date, station))
                result = cursor.fetchone()

                if not result:
                    # Insert the record if it doesn't exist
                    cursor.execute(
                        "INSERT INTO weather_data (date, station, max_temp, min_temp, precipitation) VALUES (%s, %s, %s, %s, %s)",
                        (date, station, max_temp, min_temp, precipitation)
                    )
                    records_ingested += 1


conn.commit()
conn.close()

end_time = time.time()
end_time = datetime.now()
print(f"Ended at: {end_time}")
print(f"Ingested {records_ingested} records in {(end_time - start_time).total_seconds():.2f} seconds")


#Postgresql DB is created.



