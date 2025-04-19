from fastapi import FastAPI, Query, WebSocket, WebSocketDisconnect, Request
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from database import create_table, create_connection
import pika
import json
from datetime import datetime

app = FastAPI()

# CORS ayarları
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# WebSocket bağlantı yöneticisi
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

# WebSocket endpoint
@app.websocket("/ws/anomalies")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()  # bağlantıyı canlı tut
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# Broadcast endpoint (worker'dan çağrılacak)
@app.post("/broadcast_anomaly")
async def broadcast_anomaly(request: Request):
    payload = await request.json()
    message = json.dumps(payload)
    await manager.broadcast(message)
    return {"status": "broadcasted"}

# Veri kuyruğa gönderme endpoint'i
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

# Son verileri çekme endpoint'i
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

# Anomalileri çekme
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

# Veritabanı tablolarını oluştur
create_table()
