import paho.mqtt.client as mqtt
import json
import time
import os
from datetime import datetime
import threading

class MQTTDataPublisher:
    """
    MQTT Publisher that sends scraped API data to MQTT topics
    Integrates web scraping data with MQTT protocol
    """
    
    def __init__(self, broker="broker.hivemq.com", port=1883):
        """
        Initialize MQTT publisher
        
        Args:
            broker (str): MQTT broker address
            port (int): MQTT broker port
        """
        self.broker = broker
        self.port = port
        self.client = mqtt.Client("APIDataPublisher")
        self.data_dir = "data"
        self.connected = False
        
        # Set up MQTT callbacks
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_publish = self.on_publish
        
    def on_connect(self, client, userdata, flags, rc):
        """Callback for when the client receives a CONNACK response from the server"""
        if rc == 0:
            print(f"Connected to MQTT broker {self.broker}:{self.port}")
            self.connected = True
        else:
            print(f"Failed to connect to MQTT broker. Result code: {rc}")
            self.connected = False
    
    def on_disconnect(self, client, userdata, rc):
        """Callback for when the client disconnects from the server"""
        print("Disconnected from MQTT broker")
        self.connected = False
    
    def on_publish(self, client, userdata, mid):
        """Callback for when a message is published"""
        print(f"Message published successfully (Message ID: {mid})")
    
    def connect(self):
        """Connect to MQTT broker"""
        try:
            print(f"Connecting to MQTT broker {self.broker}:{self.port}...")
            self.client.connect(self.broker, self.port, 60)
            self.client.loop_start()
            
            # Wait for connection
            timeout = 10
            while not self.connected and timeout > 0:
                time.sleep(1)
                timeout -= 1
            
            if not self.connected:
                print("Failed to connect to MQTT broker within timeout")
                return False
            
            return True
            
        except Exception as e:
            print(f"Error connecting to MQTT broker: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from MQTT broker"""
        self.client.loop_stop()
        self.client.disconnect()
    
    def load_json_data(self, filename):
        """
        Load JSON data from file
        
        Args:
            filename (str): JSON file to load
            
        Returns:
            dict: Loaded JSON data or None
        """
        filepath = os.path.join(self.data_dir, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"File not found: {filepath}")
            return None
        except json.JSONDecodeError:
            print(f"Invalid JSON in file: {filepath}")
            return None
    
    def publish_data(self, topic, data, qos=0):
        """
        Publish data to MQTT topic
        
        Args:
            topic (str): MQTT topic
            data (dict): Data to publish
            qos (int): Quality of Service level
            
        Returns:
            bool: True if published successfully
        """
        if not self.connected:
            print("Not connected to MQTT broker")
            return False
        
        try:
            # Convert data to JSON string
            json_data = json.dumps(data, indent=2, ensure_ascii=False)
            
            # Publish to MQTT topic
            result = self.client.publish(topic, json_data, qos)
            
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                print(f"Published to topic '{topic}': {len(json_data)} bytes")
                return True
            else:
                print(f"Failed to publish to topic '{topic}'. Error code: {result.rc}")
                return False
                
        except Exception as e:
            print(f"Error publishing data: {e}")
            return False
    
    def publish_posts_data(self):
        """Publish blog posts data to MQTT"""
        posts_data = self.load_json_data("jsonplaceholder_posts.json")
        if posts_data:
            # Publish individual posts
            if 'data' in posts_data and isinstance(posts_data['data'], list):
                for i, post in enumerate(posts_data['data'][:5]):  # First 5 posts
                    topic = f"api/data/posts/{post['id']}"
                    self.publish_data(topic, post)
                    time.sleep(0.5)  # Small delay between publishes
            
            # Publish summary
            summary = {
                "type": "posts_summary",
                "total_posts": len(posts_data.get('data', [])),
                "timestamp": datetime.now().isoformat(),
                "source": "JSONPlaceholder API"
            }
            self.publish_data("api/data/posts/summary", summary)
    
    def publish_cat_facts(self):
        """Publish cat facts data to MQTT"""
        facts_data = self.load_json_data("cat_facts.json")
        if facts_data:
            if 'data' in facts_data and 'data' in facts_data['data']:
                for i, fact in enumerate(facts_data['data']['data']):
                    topic = f"api/data/catfacts/{i+1}"
                    fact_with_metadata = {
                        "fact": fact['fact'],
                        "length": fact['length'],
                        "timestamp": datetime.now().isoformat(),
                        "source": "Cat Facts API"
                    }
                    self.publish_data(topic, fact_with_metadata)
                    time.sleep(0.5)
    
    def publish_weather_data(self):
        """Publish weather data to MQTT"""
        weather_data = self.load_json_data("weather_data.json")
        if weather_data and 'data' in weather_data:
            weather = weather_data['data']
            
            # Publish different weather components to different topics
            if 'main' in weather:
                temp_data = {
                    "temperature": weather['main']['temp'],
                    "feels_like": weather['main']['feels_like'],
                    "humidity": weather['main']['humidity'],
                    "pressure": weather['main']['pressure'],
                    "timestamp": datetime.now().isoformat(),
                    "location": weather.get('name', 'Unknown')
                }
                self.publish_data("api/data/weather/temperature", temp_data)
            
            if 'wind' in weather:
                wind_data = {
                    "speed": weather['wind']['speed'],
                    "direction": weather['wind'].get('deg', 0),
                    "timestamp": datetime.now().isoformat(),
                    "location": weather.get('name', 'Unknown')
                }
                self.publish_data("api/data/weather/wind", wind_data)
            
            # Publish complete weather data
            self.publish_data("api/data/weather/complete", weather)
    
    def publish_combined_data(self):
        """Publish the combined output.json data to MQTT"""
        combined_data = self.load_json_data("output.json")
        if combined_data:
            self.publish_data("api/data/combined", combined_data)
    
    def start_publishing_session(self):
        """Start a complete publishing session"""
        print("="*60)
        print("MQTT DATA PUBLISHING SESSION STARTED")
        print("="*60)
        
        if not self.connect():
            print("Failed to connect to MQTT broker. Exiting.")
            return
        
        try:
            # Publish different data types
            print("\n1. Publishing blog posts data...")
            self.publish_posts_data()
            
            print("\n2. Publishing cat facts...")
            self.publish_cat_facts()
            
            print("\n3. Publishing weather data...")
            self.publish_weather_data()
            
            print("\n4. Publishing combined data...")
            self.publish_combined_data()
            
            print("\n" + "="*60)
            print("PUBLISHING SESSION COMPLETED")
            print("="*60)
            
        except KeyboardInterrupt:
            print("\nPublishing interrupted by user")
        finally:
            self.disconnect()
    
    def start_continuous_publishing(self, interval=60):
        """
        Start continuous publishing with specified interval
        
        Args:
            interval (int): Publishing interval in seconds
        """
        print(f"Starting continuous publishing every {interval} seconds...")
        print("Press Ctrl+C to stop")
        
        if not self.connect():
            print("Failed to connect to MQTT broker. Exiting.")
            return
        
        try:
            while True:
                print(f"\n--- Publishing at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---")
                
                # Publish combined data
                combined_data = self.load_json_data("output.json")
                if combined_data:
                    # Add current timestamp
                    combined_data['publish_timestamp'] = datetime.now().isoformat()
                    self.publish_data("api/data/live", combined_data)
                
                print(f"Next publish in {interval} seconds...")
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\nContinuous publishing stopped by user")
        finally:
            self.disconnect()

def main():
    """Main function to demonstrate MQTT publishing"""
    print("MQTT Data Publisher - API Integration Demo")
    print("This application publishes scraped API data to MQTT topics")
    
    publisher = MQTTDataPublisher()
    
    print("\nChoose publishing mode:")
    print("1. Single publishing session")
    print("2. Continuous publishing (every 60 seconds)")
    print("3. Custom continuous publishing")
    
    choice = input("Enter your choice (1, 2, or 3): ").strip()
    
    if choice == "1":
        publisher.start_publishing_session()
    elif choice == "2":
        publisher.start_continuous_publishing(60)
    elif choice == "3":
        try:
            interval = int(input("Enter publishing interval in seconds: "))
            publisher.start_continuous_publishing(interval)
        except ValueError:
            print("Invalid interval. Using default 60 seconds.")
            publisher.start_continuous_publishing(60)
    else:
        print("Invalid choice. Running single session.")
        publisher.start_publishing_session()

if __name__ == "__main__":
    main()
