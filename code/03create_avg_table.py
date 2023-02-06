import psycopg2

# Connect to the database
conn = psycopg2.connect(
    host="localhost",
    database="weather_data",
    user="postgres",
    password="password"
)
cursor = conn.cursor()

# Create the weather_statistics table
cursor.execute(
    "CREATE TABLE IF NOT EXISTS weather_statistics ( "
    "    year date, "
    "    station text, "
    "    avg_max_temp double precision, "
    "    avg_min_temp double precision, "
    "    total_precipitation double precision "
    ")"
)
conn.commit()
conn.close()
