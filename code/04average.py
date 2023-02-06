import psycopg2

# Connect to the database
conn = psycopg2.connect(
    host="localhost",
    database="weather_data",
    user="postgres",
    password="password"
)
cursor = conn.cursor()

# Calculate and insert the statistics
cursor.execute(
    "INSERT INTO weather_statistics ( "
    "    year, station, avg_max_temp, avg_min_temp, total_precipitation "
    ") SELECT "
    "    date_trunc('year', date) as year, "
    "    station, "
    "    AVG(CASE WHEN max_temp = -9999 THEN NULL ELSE max_temp END), "
    "    AVG(CASE WHEN min_temp = -9999 THEN NULL ELSE min_temp END), "
    "    SUM(CASE WHEN precipitation = -9999 THEN NULL ELSE precipitation END) "
    "FROM weather_data "
    "WHERE precipitation >= 0 "
    "GROUP BY year, station"
)
conn.commit()
conn.close()
