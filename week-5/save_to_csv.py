import csv
import firebase_admin
from firebase_admin import credentials, db


try:
    firebase_admin.get_app()  
except ValueError:
    cred = credentials.Certificate("firebase_key.json") 
    firebase_admin.initialize_app(cred, {"databaseURL": "https://dct5-1c-default-rtdb.firebaseio.com/"})  

# Retrieve Data
ref = db.reference("gyroscope_data")
data = ref.get()

# Save to CSV
if data:
    with open("gyroscope_data.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "X", "Y", "Z"])  # Headers
        
        for key, value in data.items():
            writer.writerow([value["timestamp"], value["x"], value["y"], value["z"]])

    print("Data saved to gyroscope_data.csv")
else:
    print("No data found in Firebase.")
