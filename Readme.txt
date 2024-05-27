Raspberry Pi MQTT and Flask Project
Introduction
This project involves setting up a Raspberry Pi with various sensors, collecting data using MQTT, and displaying it on a local webpage using Flask. The data includes temperature, humidity, motion, light, and distance measurements.

Components
Raspberry Pi (any model with GPIO pins)
DHT11 Sensor (temperature and humidity)
PIR Sensor (motion detection)
Ultrasonic Sensor (distance measurement)
LDR Sensor (light detection)
Jumper wires
Breadboard
Setup
Installing Raspbian
Download and Install Raspberry Pi Imager: Raspberry Pi Imager
Install Raspbian: Use Raspberry Pi Imager to install Raspbian onto the microSD card.
Set Up Raspberry Pi: Insert the microSD card into your Raspberry Pi and follow the on-screen instructions to set up your Raspberry Pi.
Installing Libraries and Tools
Update System: Open a terminal on your Raspberry Pi and run:
bash
Copier le code
sudo apt update && sudo apt upgrade
Install Python 3 and pip:
bash
Copier le code
sudo apt install python3 python3-pip
Install Flask:
bash
Copier le code
pip3 install Flask
Install Adafruit DHT library:
bash
Copier le code
pip3 install Adafruit_DHT
Install Paho MQTT library:
bash
Copier le code
pip3 install paho-mqtt
Install ecdsa library:
bash
Copier le code
pip3 install ecdsa
Install and Set Up Mosquitto MQTT broker:
bash
Copier le code
sudo apt install mosquitto mosquitto-clients
sudo systemctl enable mosquitto
sudo systemctl start mosquitto
Wiring the Sensors
Use the following diagram to connect your sensors to the Raspberry Pi GPIO pins:

[Insert Wiring Diagram Image Here]

Sensor	Raspberry Pi GPIO
DHT11 Data Pin	GPIO 4
PIR Out Pin	GPIO 17
Ultrasonic Trig Pin	GPIO 23
Ultrasonic Echo Pin	GPIO 24
LDR Pin	GPIO 27
Running the Code
Setting Up MQTT Broker
Ensure Mosquitto MQTT broker is running:

bash
Copier le code
sudo systemctl start mosquitto
Running the Sensor Code
Create a file named sensor.py and paste the Raspberry Pi sensor code into it.
Run the sensor code:
bash
Copier le code
python3 sensor.py
Running the Flask App
Create a file named app.py and paste the Flask application code into it.
Create a templates directory and add the index.html file with the provided HTML content.
Run the Flask app:
bash
Copier le code
python3 app.py
Open a web browser and navigate to http://<your_raspberry_pi_ip>:5000 to view the sensor data.
Screenshots
[Insert Screenshots Here]