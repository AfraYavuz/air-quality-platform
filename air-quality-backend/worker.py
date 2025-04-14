import pika
import json
import psycopg2

# PostgreSQL bağlantısı
def create_connection():
    return psycopg2.connect(
        dbname="air_quality",
        user="admin",
        password="admin",
        host="localhost",
        port="5432"
    )

# Anomali tespiti fonksiyonu
def detect_anomalies(data):
    anomalies = []

    if data["pm25"] > 100:
        anomalies.append(f"Yüksek PM2.5: {data['pm25']}")

    if data["pm10"] > 150:
        anomalies.append(f"Yüksek PM10: {data['pm10']}")

    if data["no2"] > 200:
        anomalies.append(f"Yüksek NO2: {data['no2']}")

    if anomalies:
        print("🚨 Anomali Tespit Edildi:")
        for a in anomalies:
            print(f" - {a}")

def callback(ch, method, properties, body):
    data = json.loads(body)
    print("Veri alındı:", data)

    # Anomali kontrolü
    detect_anomalies(data)

    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("""
    INSERT INTO air_quality_data (latitude, longitude, pm25, pm10, no2, so2, o3)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        data["latitude"],
        data["longitude"],
        data["pm25"],
        data["pm10"],
        data["no2"],
        data["so2"],
        data["o3"]
    ))

    connection.commit()
    cursor.close()
    connection.close()
    print("[✓] Veri kaydedildi")

# RabbitMQ bağlantısı
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# Kuyruk oluştur (varsa sorun olmaz)
channel.queue_declare(queue='air_quality_queue')

# Kuyruğu dinlemeye başla
channel.basic_consume(
    queue='air_quality_queue',
    on_message_callback=callback,
    auto_ack=True
)

print(" [*] Kuyruk dinleniyor. Çıkmak için CTRL+C")
channel.start_consuming()
