US Weather Data Project:

Step by step wise method to implement.

1. Install PostgreSQL 
https://www.postgresql.org/download/

2. Setup PGAdmin
set password for Admin.

3. Create Database on PostgreSQL PGAdmin.
Make weather_data
Make weather_statistics
set default values.

4. Execute "01create_weatherDB_table.py" to create weather_data DB table.

5. Execute "02main_code.py" to load data from RAW txt files to weather_data DB. It takes minimum 4mins.

6. Execute "03create_avg_table.py" to create weather_statistics DB table.

7. Execute "04average.py" to take average of the yearly temprature and precipitation. It takes about minimum 5mins.

8. Execute "05api.py" on Terminal to load API by following steps.
change directory to code directory.
$ cd c:\usweather\code
$ export FLASK_APP=05api.py
$ Flask run

9. Check API get points in
/api/weather
/api/weather/stats

can use curl, web browser.