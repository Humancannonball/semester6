# Laboratory Work 3: MQTT Protocol Basic Implementation

## Objective
Learn the basics of MQTT protocol by implementing a simple publisher client that connects to a public MQTT broker and publishes messages to a topic.

## Implementation

### Code Analysis
The `mqtt_app.py` file implements a basic MQTT publisher with the following components:

```python
import paho.mqtt.client as mqtt
import time

def connect_broker(broker_address, client_name):
    client = mqtt.Client(client_name)
    client.connect(broker_address)
    time.sleep(1)
    client.loop_start()
    return client

if __name__ == "__main__":
    server = "broker.hivemq.com"
    client_name = "hivemq"
    client = connect_broker(server, client_name)
    try:
        while True:
            message = input('Send some random message:')
            client.publish("lab3/topic", message)
    except KeyboardInterrupt:
        client.disconnect()
        client.loop_stop()
```

### Key Components

1. **MQTT Client Creation**: Uses `paho.mqtt.client` library
2. **Broker Connection**: Connects to HiveMQ public broker
3. **Message Publishing**: Publishes user input to `lab3/topic`
4. **Loop Management**: Handles continuous message sending
5. **Graceful Shutdown**: Disconnects properly on Ctrl+C

### Testing Instructions

1. **Install Dependencies**:
   ```bash
   pip install paho-mqtt
   ```

2. **Run the Publisher**:
   ```bash
   python mqtt_app.py
   ```

3. **Send Messages**:
   - Enter messages when prompted
   - Messages are published to topic `lab3/topic`

4. **Test with MQTTBox**:
   - Subscribe to topic `lab3/topic` on `broker.hivemq.com`
   - Observe messages sent from the Python script

### Configuration Details

- **Broker**: `broker.hivemq.com` (public HiveMQ broker)
- **Client ID**: `hivemq`
- **Topic**: `lab3/topic`
- **QoS**: Default (0 - At most once)

### Expected Behavior

1. Application connects to MQTT broker
2. User can enter messages interactively
3. Each message is published to the specified topic
4. Subscribers to the topic receive the messages
5. Application can be stopped with Ctrl+C

### Conclusion

Lab 3 demonstrates the fundamental concepts of MQTT publishing:
- Client-broker connection establishment
- Message publishing to topics
- Basic loop management for continuous operation
- Proper resource cleanup on shutdown

This forms the foundation for more complex MQTT applications like the database storage (Lab 4) and web visualization (Lab 5) implementations.
