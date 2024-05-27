from flask import Flask, render_template, jsonify
import paho.mqtt.client as mqtt
import json
import hashlib
import ecdsa
import csv
import time

# Functions to create a csv file and insert the data
csv_file="sensor _data.csv"
def create_csv(file_name):
    header = ["Timestamp","Humidity (%)","Temp(C)","Mouvement","Light","Distance(CM)","Time with parallelism","Time without parallelism","Sginature status"]
    with open(file_name, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)

def insert_values(file_name,data,signature_validity,payload):   
    with open(file_name, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([data['timestamp'],data['humidity'],data['temperature'],data['mouvement'],data['light'],data['distance'],payload['with_parallele_time'],payload['without_parallele_time'],signature_validity])
    print(f"Values inserted into '{file_name}")

# Global variable to store sensor data and the public key
sensor_data = {"humidity": "No data", "temperature": "No data", "sound": "No data"}
public_key = None
signature_validity = "No signature checked"
para_time=0
non_para_time=0

app = Flask(__name__)

mqtt_broker_address = "192.168.1.37"

# MQTT message callback
def on_connect(client, userdata, flags, rc):
    print(f"connected with result code {rc}")
    client.subscribe("sensor/data")
    create_csv(csv_file)

def on_message(client, userdata, msg):
    global sensor_data, public_key, signature_validity,para_time,non_para_time
    payload = json.loads(msg.payload.decode('utf-8'))
    if 'key' in payload:
        public_key_pem = payload['key']
        public_key = ecdsa.VerifyingKey.from_pem(public_key_pem)
        print("Public key received")
    else:
        signature = bytes.fromhex(payload['signature'])
        data = payload['data']
        para_time=payload['with_parallele_time']
        non_para_time=payload['without_parallele_time']
        data_str = json.dumps(data)
        hash_data = hashlib.sha256(data_str.encode('utf-8')).digest()
        print(payload)
        try:
            if public_key:
                public_key.verify(signature, hash_data)
                signature_validity = "Valid signature"
                print("valid sig")
            else:
                signature_validity = "No public key to verify signature"
                print("no sig")
        except ecdsa.BadSignatureError:
            signature_validity = "Invalid signature"
            print("invalid sig")
        sensor_data = data
        insert_values(csv_file,data,signature_validity,payload)

# Create MQTT client instance
mqtt_client = mqtt.Client()

# Configure MQTT client
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

mqtt_client.connect(mqtt_broker_address, 1883, 60)

# Function to fetch sensor data
def get_sensor_data():
    global sensor_data
    return sensor_data

# Function to fetch signature validity
def get_signature_validity():
    global signature_validity
    return signature_validity

def get_para_time():
    global para_time
    return para_time

def get_non_para_time():
    global non_para_time
    return non_para_time


# Flask route to serve HTML file
@app.route('/')
def index():
    return render_template('index.html')

# Endpoint to provide sensor data via AJAX request
@app.route('/sensor_data')
def send_sensor_data():
    data = get_sensor_data()
    return jsonify(data)

# Endpoint to provide signature validity via AJAX request
@app.route('/signature_validity')
def send_signature_validity():
    sig = get_signature_validity()
    return jsonify(sig)

@app.route('/para_time')
def send_para_time():
     para = get_para_time()
     return jsonify(para)

@app.route('/non_para_time')
def send_non_para_time():
    non_para = get_non_para_time()
    return jsonify(non_para)

if __name__ == '__main__':
    mqtt_client.loop_start()
    app.run(debug=True)