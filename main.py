from flask import Flask, jsonify
import psycopg2
from shapely.wkb import loads
import os

# PostGIS database connection details
dbname = os.getenv('DB_NAME', 'gis5572')
user = os.getenv('DB_USER', 'postgres')
password = os.getenv('DB_PASSWORD')
host = os.getenv('DB_HOST', '34.31.152.38')
port = os.getenv('DB_PORT', '5432')

app = Flask(__name__)

def connect_to_postgres():
    try:
        connection = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        return connection
    except psycopg2.Error as e:
        app.logger.error(f"Error connecting to PostgreSQL: {e}")
        return None

@app.route('/et_points', methods=['GET'])
def get_temp_points():
    connection = connect_to_postgres()
    if connection:
        with connection:
            with connection.cursor() as cursor:
                try:
                    table_name = 'et2023_idw_points'
                    sql_query = f"SELECT shape FROM {table_name};"
                    cursor.execute(sql_query)
                    rows = cursor.fetchall()

                    features = []
                    for row in rows:
                        try:
                            geojson = wkb_to_geojson(row[0])
                            features.append({"type": "Feature", "geometry": geojson})
                        except Exception as e:
                            app.logger.error(f"Error converting geometry: {e}")

                    return jsonify({"type": "FeatureCollection", "features": features})
                except psycopg2.Error as e:
                    app.logger.error(f"Error executing SQL query: {e}")
                    return jsonify({"error": "Internal Server Error"}), 500
    else:
        return jsonify({"error": "Database Connection Error"}), 500
        
def wkb_to_geojson(wkb):
    geometry = loads(wkb)  # Assuming binary format
    return geometry.__geo_interface__

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
