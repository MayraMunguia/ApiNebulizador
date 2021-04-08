#SqlLogsMqtt#
import paho.mqtt.client as mqtt
import sqlite3
from datetime import datetime
 
MQTT_HOST = '192.168.100.43'
MQTT_PORT = 1883
MQTT_CLIENT_ID = ''
MQTT_USER = 'kael1'
MQTT_PASSWORD = 'lonchis123'
TOPIC = 'dblog1'
 
DATABASE_FILE = 'db.sqlite3'
 
 
def on_connect(mqtt_client, user_data, flags, conn_result):
    mqtt_client.subscribe(TOPIC)
 
 
def on_message(mqtt_client, user_data, message):
    payload = message.payload.decode('utf-8')
 
    db_conn = user_data['db_conn']
    sql = 'INSERT INTO models_lectura (lectura) VALUES (?)'
    cursor = db_conn.cursor()
    cursor.execute(sql, (payload,))
    db_conn.commit()
    cursor.close()
 
 
def main():
    db_conn = sqlite3.connect(DATABASE_FILE)
    sql = """
    CREATE TABLE IF NOT EXISTS models_lectura (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        topic TEXT NOT NULL,
        payload TEXT NOT NULL
    )
    """
    cursor = db_conn.cursor()
    cursor.execute(sql)
    cursor.close()
 
    mqtt_client = mqtt.Client(MQTT_CLIENT_ID)
    mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    mqtt_client.user_data_set({'db_conn': db_conn})
 
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
 
    mqtt_client.connect(MQTT_HOST, MQTT_PORT)
    mqtt_client.loop_forever()
 
 
main()