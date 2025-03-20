import paho.mqtt.client as mqtt
import pymongo
import json
import urllib.parse

username = urllib.parse.quote_plus("makkarsaab18")
password = urllib.parse.quote_plus("Makkar123") 

MONGO_URI = f"mongodb+srv://{username}:{password}@cluster0.6yjbe.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
mongo_client = pymongo.MongoClient(MONGO_URI)
db = mongo_client["sensor_data"]
collection = db["gyroscope"]

MQTT_BROKER = "9ee13c6e36f24d13b7aed1c23d643834.s1.eu.hivemq.cloud"
MQTT_PORT = 8883  
MQTT_TOPIC = "sensor/gyroscope"
MQTT_USER = "sukhman"
MQTT_PASSWORD = "Makkar@123"

def on_message(client, userdata, message):
    try:
        data = json.loads(message.payload.decode())
        print("Received Data:", data)

        collection.insert_one(data)
        print("Data saved to MongoDB Atlas.")

    except Exception as e:
        print("Error:", e)

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)  
client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
client.tls_set() 

client.on_message = on_message
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.subscribe(MQTT_TOPIC)

print("Listening for MQTT messages...")
client.loop_forever()
