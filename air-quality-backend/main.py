from fastapi import FastAPI
from database import create_table
from database import create_connection
import pika
import json

app = FastAPI()

@app.post("/add_air_quality")
async def add_air_quality(latitude: float, longitude: float, pm25: float, pm10: float, no2: float, so2: float, o3: float):
    # RabbitMQ bağlantısı
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    # Kuyruk oluştur (varsa sorun olmaz)
    channel.queue_declare(queue='air_quality_queue')

    # Mesajı gönder
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

create_table()
