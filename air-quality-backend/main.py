from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from database import create_table, create_connection
import pika
import json
from datetime import datetime

# FastAPI uygulamanızı oluşturun
app = FastAPI()

# CORS Middleware ekleyin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React uygulamanızın portunu buraya ekleyin
    allow_credentials=True,
    allow_methods=["*"],  # Tüm HTTP metotlarına izin ver
    allow_headers=["*"],  # Tüm başlıklara izin ver
)

@app.post("/add_air_quality")
async def add_air_quality(latitude: float, longitude: float, pm25: float, pm10: float, no2: float, so2: float, o3: float):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='air_quality_queue')

    data = {
        "latitude": latitude,
        "longitude": longitude,
        "pm25": pm25,
        "pm10": pm10,
        "no2": no2,
        "so2": so2,
        "o3": o3
    }

    channel.basic_publish(
        exchange='',
        routing_key='air_quality_queue',
        body=json.dumps(data)
    )

    connection.close()
    return {"message": "Veri kuyruğa başarıyla gönderildi"}

@app.get("/air_quality_data")
async def get_air_quality_data():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM air_quality_data ORDER BY timestamp DESC")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()

    data = []
    for row in rows:
        data.append({
            "id": row[0],
            "latitude": row[1],
            "longitude": row[2],
            "pm25": row[3],
            "pm10": row[4],
            "no2": row[5],
            "so2": row[6],
            "o3": row[7],
            "timestamp": row[8]
        })

    return {"data": data}

@app.get("/anomalies")
async def get_anomalies():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM anomalies ORDER BY timestamp DESC")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()

    data = []
    for row in rows:
        data.append({
            "id": row[0],
            "latitude": row[1],
            "longitude": row[2],
            "pm25": row[3],
            "pm10": row[4],
            "no2": row[5],
            "so2": row[6],
            "o3": row[7],
            "reason": row[8],
            "timestamp": row[9]
        })

    return {"anomalies": data}

@app.get("/anomalies_by_time")
async def get_anomalies_by_time(
    start: datetime = Query(..., description="Başlangıç zamanı"),
    end: datetime = Query(..., description="Bitiş zamanı")
):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM anomalies WHERE timestamp BETWEEN %s AND %s ORDER BY timestamp DESC",
        (start, end)
    )
    rows = cursor.fetchall()
    cursor.close()
    connection.close()

    data = []
    for row in rows:
        data.append({
            "id": row[0],
            "latitude": row[1],
            "longitude": row[2],
            "pm25": row[3],
            "pm10": row[4],
            "no2": row[5],
            "so2": row[6],
            "o3": row[7],
            "reason": row[8],
            "timestamp": row[9]
        })

    return {"anomalies": data}

# Tabloyu oluştur
create_table()
