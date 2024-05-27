# Raspberry Pi MQTT and Flask Project

## Overview

This project combines Raspberry Pi, MQTT, Flask and ECDSA certification algorithme to create a comprehensive solution for sensor data collection and visualization. The Raspberry Pi collects data from various sensors, publishes it using MQTT, and displays it on a local webpage using Flask.

## Components

- Raspberry Pi (any model with GPIO pins)
- DHT11 Sensor (temperature and humidity)
- PIR Sensor (motion detection)
- Ultrasonic Sensor (distance measurement)
- LDR Sensor (light detection)
- Jumper wires
- Breadboard

## Setup

### Installing Raspbian

1. Download and install Raspberry Pi Imager: [Raspberry Pi Imager](https://www.raspberrypi.org/software/)
2. Use Raspberry Pi Imager to install Raspbian onto the microSD card.
3. Insert the microSD card into your Raspberry Pi and follow the on-screen instructions to set up your Raspberry Pi.

### Installing Libraries and Tools

1. **Update System**: Open a terminal on your Raspberry Pi and run:
    ```bash
    sudo apt update && sudo apt upgrade
    ```

2. **Install Python 3 and pip**:
    ```bash
    sudo apt install python3 python3-pip
    ```

3. **Install Flask**:
    ```bash
    pip3 install Flask
    ```

4. **Install Adafruit DHT library**:
    ```bash
    pip3 install Adafruit_DHT
    ```

5. **Install Paho MQTT library**:
    ```bash
    pip3 install paho-mqtt
    ```

6. **Install ecdsa library**:
    ```bash
    pip3 install ecdsa
    ```

7. **Install and Set Up Mosquitto MQTT broker**:
    ```bash
    sudo apt install mosquitto mosquitto-clients
    sudo systemctl enable mosquitto
    sudo systemctl start mosquitto
    ```

## Wiring the Sensors

Use the following diagram to connect your sensors to the Raspberry Pi GPIO pins:

[Insert Wiring Diagram Image Here]

| Sensor         | Raspberry Pi GPIO |
|----------------|-------------------|
| DHT11 Data Pin | GPIO 4            |
| PIR Out Pin    | GPIO 17           |
| Ultrasonic Trig Pin | GPIO 23     |
| Ultrasonic Echo Pin | GPIO 24     |
| LDR Pin        | GPIO 27           |

## Running the Code

### Setting Up MQTT Broker

Ensure Mosquitto MQTT broker is running:
```bash
sudo systemctl start mosquitto
```
Running the Sensor Code
Create a file named sensor.py and paste the Raspberry Pi sensor code into it.
Run the sensor code:
```bash
python3 sensor.py
```
Running the Flask App
Create a file named app.py and paste the Flask application code into it.
Create a templates directory and add the index.html file with the provided HTML content.
Run the Flask app:
```bash
python3 app.py
```
Open a web browser and navigate to http://<your_raspberry_pi_ip>:5000 to view the sensor data.
## Screenshots
![Capture](https://github.com/yassinhawari/RaspberryPi-FLASK/assets/107224248/f60f0f21-b17b-4c46-a6b2-0799b3f43aca)

## Contributing
Contributions are welcome! To contribute, follow these steps:

Fork the repository.
Create a new branch (git checkout -b feature/YourFeature).
Make your changes and commit them (git commit -m 'Add some feature').
Push to the branch (git push origin feature/YourFeature).
Open a pull request.
## License

## Contact
For any questions or suggestions, please contact me at hawari.yassine.yh@gmail.com.
