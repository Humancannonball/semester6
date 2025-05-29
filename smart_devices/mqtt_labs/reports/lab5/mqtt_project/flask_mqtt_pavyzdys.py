import eventlet
import os
eventlet.monkey_patch()

from flask import Flask, render_template
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
import json
from datetime import datetime

app = Flask(__name__, template_folder='../templates')
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['MQTT_BROKER_URL'] = 'broker.hivemq.com'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = ''
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_KEEPALIVE'] = 5
app.config['MQTT_TLS_ENABLED'] = False

mqtt = Mqtt(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code " + str(rc))
    # Subscribe to all sensor topics
    mqtt.subscribe('Home/BedRoom/1/Temperature')
    mqtt.subscribe('Home/BedRoom/1/Humidity')
    mqtt.subscribe('Home/BedRoom/1/Pressure')
    mqtt.subscribe('Home/BedRoom/#')  # Wildcard subscription for all bedroom sensors

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    try:
        # Parse JSON payload
        payload_str = message.payload.decode()
        payload_json = json.loads(payload_str)
        
        # Extract sensor type from topic
        topic_parts = message.topic.split('/')
        sensor_type = topic_parts[-1] if len(topic_parts) > 0 else "Unknown"
        
        # Prepare data for frontend
        data = {
            'topic': message.topic,
            'payload': payload_str,
            'sensor_type': sensor_type,
            'sensor_id': payload_json.get('Sensor_ID', 'Unknown'),
            'timestamp': payload_json.get('Date', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
            'value': payload_json.get(sensor_type, 'N/A'),
            'unit': get_unit_for_sensor(sensor_type)
        }
        
        print(f"Received {sensor_type} data: {data['value']}{data['unit']}")
        socketio.emit('mqtt_message', data=data)
        
    except json.JSONDecodeError:
        # Handle non-JSON messages
        data = {
            'topic': message.topic,
            'payload': message.payload.decode(),
            'sensor_type': 'Raw',
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'value': message.payload.decode(),
            'unit': ''
        }
        socketio.emit('mqtt_message', data=data)
    except Exception as e:
        print(f"Error processing message: {e}")

def get_unit_for_sensor(sensor_type):
    """Return appropriate unit for sensor type"""
    units = {
        'Temperature': '°C',
        'Humidity': '%',
        'Pressure': ' hPa'
    }
    return units.get(sensor_type, '')

@app.route('/')
def index():
    return render_template('index.html')

@mqtt.on_log()
def handle_logging(client, userdata, level, buf):
    # Only log important messages to reduce noise
    if level <= 16:  # Only log warnings and errors
        print(f"MQTT Log - Level: {level}, Message: {buf}")

if __name__ == '__main__':
    print("Starting MQTT IoT Dashboard...")
    print("Dashboard will be available at: http://localhost:5000")
    socketio.run(app, host='localhost', port=5000, debug=True, use_reloader=False)
