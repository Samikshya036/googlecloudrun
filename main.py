from flask import Flask, jsonify
import psycopg2
from shapely.wkb import loads

# PostGIS database connection details
dbname = 'gis5572'
user = 'postgres'
password = 'sami@2010'
host = '35.202.65.52'  # Cloud DB Public IP address
port = '5432'

app = Flask(__name__)

def connect_to_postgres():
    try:
        connection = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        return connection
    except psycopg2.Error as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return None
