import psycopg2
from psycopg2 import sql

def create_connection():
    connection = psycopg2.connect(
        dbname="air_quality",
        user="admin",
        password="admin",
        host="localhost",
        port="5432"
    )
    return connection

def create_table():
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS air_quality_data (
        id SERIAL PRIMARY KEY,
        latitude DOUBLE PRECISION,
        longitude DOUBLE PRECISION,
        pm25 DOUBLE PRECISION,
        pm10 DOUBLE PRECISION,
        no2 DOUBLE PRECISION,
        so2 DOUBLE PRECISION,
        o3 DOUBLE PRECISION,
        timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
    )
    """)

    connection.commit()
    cursor.close()
    connection.close()