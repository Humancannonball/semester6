# Laboratory Work 5: MQTT Protocol - Data Visualization in Browser

## Objective
Learn to display MQTT messages in the browser and add new statistical groups that will be visualized in the browser using Flask-MQTT and Socket.IO.

## Implementation

### 1. Flask Application Enhancement
- Modified `flask_mqtt_pavyzdys.py` to handle multiple MQTT topics
- Added JSON parsing for sensor data
- Implemented real-time data broadcasting via Socket.IO
- Added support for Temperature, Humidity, and Pressure sensors

### 2. Frontend Visualization
- Created responsive Bootstrap-based dashboard
- Real-time sensor value display cards
- Live message log with formatting
- Connection status indicator
- Message counter and clear functionality

### 3. Key Features
- **Multi-topic Subscription**: Subscribes to all bedroom sensor topics using wildcards
- **Real-time Updates**: Uses Socket.IO for instant data updates
- **Data Parsing**: Handles JSON payloads from sensors
- **Visual Feedback**: Color-coded sensor cards and status indicators
- **Message History**: Scrollable log of recent messages

## File Structure
```
lab5/
├── mqtt_project/
│   ├── flask_mqtt_pavyzdys.py  # Main Flask application
│   └── templates/
│       └── index.html          # Dashboard HTML template
└── templates/
    └── index.html              # Original template location
```

## Testing Instructions

### 1. Install Dependencies
```bash
pip install flask_socketio==4.3.2
pip install flask_mqtt
pip install eventlet
pip install flask_bootstrap
```

### 2. Run the Application
```bash
cd /var/home/mark/Documents/semester6/smart_devices/mqtt_labs/lab5/mqtt_project
python flask_mqtt_pavyzdys.py
```

### 3. Access Dashboard
Open browser and navigate to: `http://localhost:5000`

### 4. Send Test Data via MQTTBox
Use the following payloads for testing:

**Temperature:**
- Topic: `Home/BedRoom/1/Temperature`
- Payload:
```json
{
  "Sensor_ID": "DHT22_01",
  "Date": "2024-01-15 14:30:25",
  "Temperature": "23.5"
}
```

**Humidity:**
- Topic: `Home/BedRoom/1/Humidity`
- Payload:
```json
{
  "Sensor_ID": "DHT22_01",
  "Date": "2024-01-15 14:30:30",
  "Humidity": "65.2"
}
```

**Pressure:**
- Topic: `Home/BedRoom/1/Pressure`
- Payload:
```json
{
  "Sensor_ID": "BMP280_01",
  "Date": "2024-01-15 14:30:35",
  "Pressure": "1013.25"
}
```

## Expected Results
1. Dashboard displays real-time sensor values in colored cards
2. Message log shows formatted MQTT messages as they arrive
3. Connection status indicator shows green when connected
4. Each sensor type displays with appropriate units and icons
5. Messages are automatically limited to last 50 entries

## Technical Architecture
- **Backend**: Flask with Flask-MQTT for MQTT handling
- **Real-time Communication**: Socket.IO for client-server communication
- **Frontend**: Bootstrap 5 for responsive UI
- **Message Format**: JSON parsing with error handling for non-JSON messages
- **Broker**: HiveMQ public broker (broker.hivemq.com)

## Issues Resolved
1. **Eventlet Monkey Patching**: Fixed import order to prevent application context errors
2. **Template Path**: Configured Flask to find templates in correct directory structure
3. **Socket.IO Compatibility**: Used eventlet mode for better compatibility
4. **MQTT Logging**: Reduced noise by filtering log levels

## Screenshots
The dashboard features:
- Three sensor cards (Temperature, Humidity, Pressure) with real-time values
- Color-coded cards (red for temperature, blue for humidity, green for pressure)
- Connection status indicator in the navigation bar
- Scrollable message log with formatted JSON payloads
- Clear messages button and message counter

## Conclusion
Lab 5 successfully demonstrates real-time MQTT data visualization in a web browser, combining multiple technologies to create an interactive IoT dashboard for monitoring sensor data. The implementation handles multiple sensor types, provides visual feedback, and maintains a clean, responsive interface.
