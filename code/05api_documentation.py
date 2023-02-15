from flask import Flask, request
from flask_restx import Api, Resource, fields
import psycopg2
import json

app = Flask(__name__)
api = Api(app, version='1.0', title='Weather Data API',
          description='API to retrieve weather data based on date and station')

weather_data_model = api.model('WeatherData', {
    'date': fields.String(required=True, description='Date in the format YYYY-MM-DD'),
    'station': fields.String(required=True, description='Name of the weather station'),
    'max_temp': fields.Float(required=True, description='Maximum temperature'),
    'min_temp': fields.Float(required=True, description='Minimum temperature'),
    'precipitation': fields.Float(required=True, description='Precipitation')
})

stats_data = api.model('Weather Stats', {
    'year': fields.String(required=True, description='Year of the weather statistics'),
    'station': fields.String(required=True, description='Weather station location'),
    'avg_max_temp': fields.Float(required=True, description='Average maximum temperature'),
    'avg_min_temp': fields.Float(required=True, description='Average minimum temperature'),
    'precipitation': fields.Float(required=True, description='Total precipitation amount')
})

@api.route('/api/weather')
class WeatherData(Resource):
    @api.doc('get_weather_data')
    @api.marshal_list_with(weather_data_model)
    def get(self):
        conn = psycopg2.connect(
            host="localhost",
            database="weather_data",
            user="postgres",
            password="password"
        )
        cursor = conn.cursor()

        date = request.args.get("date")
        station = request.args.get("station")
        page = request.args.get("page")
        per_page = request.args.get("per_page")

        params = []
        query = "SELECT date, station, max_temp, min_temp, precipitation FROM weather_data WHERE date IS NOT NULL"

        if date:
            query += " AND date = %s"
            params.append(date)

        if station:
            query += " AND station = %s"
            params.append(station)

        if page and per_page:
            query += " LIMIT %s OFFSET %s"
            params.append(per_page)
            params.append((int(page) - 1) * int(per_page))

        cursor.execute(query, params)
        result = cursor.fetchall()

        weather_data = []
        for row in result:
            weather_data.append({
                "date": row[0].strftime("%Y-%m-%d"),
                "station": row[1],
                "max_temp": row[2],
                "min_temp": row[3],
                "precipitation": row[4]
            })

        return weather_data

@api.route("/api/weather/stats")
class Stats(Resource):
    @api.doc(description='Retrieve weather statistics')
    @api.marshal_with(stats_data)
    def get(self):
        conn =psycopg2.connect(
            host="localhost",
            database="weather_data",
            user="postgres",
            password="password"
        )
        cursor = conn.cursor()
        
        year = request.args.get("year")
        station = request.args.get("station")
        page = request.args.get("page")
        per_page = request.args.get("per_page")

        params = []
        query = "SELECT year, station, avg_max_temp, avg_min_temp, total_precipitation FROM weather_statistics"

        if year:
            query += " WHERE year = %s"
            params.append(str(year))

        if station:
            if not year:
                query += " WHERE"
            else:
                query += " AND"
            query += " station = %s"
            params.append(station)

        if page and per_page:
            query += " LIMIT %s OFFSET %s"
            params.append(per_page)
            params.append((int(page) - 1) * int(per_page))

        cursor.execute(query, params)
        result = cursor.fetchall()

        stats_data = []
        for row in result:
            stats_data.append({
                "date": row[0].strftime("%Y-%m-%d"),
                "year": row[0].strftime("%Y"),
                "station": row[1],
                "avg_max_temp": row[2],
                "avg_min_temp": row[3],
                "precipitation": row[4]
            })
        return stats_data


if __name__ == '__main__':
    app.run(debug=True)
