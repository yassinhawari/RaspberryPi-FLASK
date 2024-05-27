import paho.mqtt.publish as publish
import Adafruit_DHT
import RPi.GPIO as GPIO
import json
import hashlib
import ecdsa
import random
import time
from datetime import datetime
import multiprocessing
import paho.mqtt.client as mqtt

# PIR Sensor setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN)

# Ultrasonic Sensor setup
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.IN)

# LDR Sensor setup
GPIO.setup(27, GPIO.IN)

# DHT11 Sensor setup
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4

def read_pir_sensor():
    if GPIO.input(17):
        return 1
    else:
        return 0

def read_ultrasonic_sensor():
    GPIO.output(23, True)
    time.sleep(0.00001)
    GPIO.output(23, False)

    start_time = time.time()
    stop_time = time.time()

    while GPIO.input(24) == 0:
        start_time = time.time()

    while GPIO.input(24) == 1:
        stop_time = time.time()

    time_elapsed = stop_time - start_time
    distance = (time_elapsed * 34300) / 2
    return distance

def read_ldr_sensor():
    return GPIO.input(27)

#def read_dht11_sensor():
#    humidity,temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
#    if humidity is not None and temperature is not None:
#        return temperature, humidity
#    else:
#		print("error temp")
#        return "Failed to retrieve data from humidity sensor"
        
# Generate ECDSA key pair
private_key = ecdsa.SigningKey.generate(curve=ecdsa.NIST256p)
public_key = private_key.get_verifying_key()
public_key_pem = public_key.to_pem().decode('utf-8')

def sign_data(hash_data):
	signature = private_key.sign(hash_data).hex()
	return signature

mqtt_broker_adress="127.0.0.1"
MQTT_TOPIC = 'sensor/data'
MQTT_TOPIC_KEY = 'sensor/key'

certificat = {
      "key": public_key_pem,
        }

publish.single("sensor/data",json.dumps(certificat),hostname="127.0.0.1")
print(json.dumps(certificat))
while True:
	try:
		#mouvement=read_pir_sensor()
		#distance=read_ultrasonic_sensor()
		#light=read_ldr_sensor()
		#temperature, humidity=read_dht11_sensor()
		
		humidity = round(random.uniform(68.0, 72.0),2)
		temperature = round(random.uniform(23.0, 24.5),2)
		distance = round(random.uniform(30,120),2)
		light= random.choice([0, 1])
		mouvement= random.choice([0, 1])
		
		date=datetime.now().strftime("%H:%M:%S")
		data = {"timestamp":date,"humidity": humidity,"temperature": temperature,"light": light,"mouvement":mouvement,"distance":distance}		
		data_str = json.dumps(data)
		hash_data = hashlib.sha256(data_str.encode('utf-8')).digest()
		
		pool=multiprocessing.Pool()
		parallele_start=time.time()
		signature_with_paralleslism= pool.apply_async(sign_data,args=(hash_data,))
		parallele_end=time.time()
		pool.close()
		pool.join()		
		total_with_parallele=parallele_end-parallele_start
			
		signing_start=time.time()
		signature=sign_data(hash_data)
		signing_end=time.time()
		signing_time=signing_end - signing_start		
		message = {
           "data": data,
           "signature": signature,
           "without_parallele_time":round(signing_time,5),
           "with_parallele_time":round(total_with_parallele,5)
		}
		publish.single(MQTT_TOPIC,json.dumps(message),hostname="127.0.0.1")
		print(message)
		time.sleep(3)
	except KeyboardInterrupt:
		print("Exiting...")
		break
	finally:
		GPIO.cleanup()

