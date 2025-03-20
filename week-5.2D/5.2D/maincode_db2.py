import paho.mqtt.client as mqtt
import json
import couchdb
from datetime import datetime

couch = couchdb.Server("http://127.0.0.1:5984/")
couch.resource.credentials = ("Makkar", "Makkar@123")

db_name = "gyroscope_db2"
if db_name in couch:
    db = couch[db_name]
else:
    db = couch.create(db_name)

def on_message(client, userdata, msg):
    payload = json.loads(msg.payload.decode())  
    timestamp = datetime.now().isoformat() 

    db.save({
        "_id": timestamp,  
        "sensor_name": payload["sensor_name"],
        "timestamp": payload["timestamp"],
        "x": payload["x"],
        "y": payload["y"],
        "z": payload["z"]
    })

    print(f" Data Inserted into CouchDB: {payload}")


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)  
client.on_message = on_message
client.username_pw_set("sukhman", "Makkar@123")  
client.tls_set()  
client.connect("9ee13c6e36f24d13b7aed1c23d643834.s1.eu.hivemq.cloud", 8883)
client.subscribe("sensor/gyroscope")
client.loop_forever()
