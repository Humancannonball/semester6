import sqlite3
import paho.mqtt.client as mqtt
import json

MQTT_Topic = "Home/BedRoom/#"
mqttBroker ="broker.hivemq.com"

# SQLite DB Name
DB_Name =  "IoT.db"

# SQLite DB Table Schema
TableSchema="""
drop table if exists Temperature_Data ;
create table Temperature_Data (
  id integer primary key autoincrement,
  SensorID text,
  Date_n_Time text,
  Temperature text
);


drop table if exists Humidity_Data ;
create table Humidity_Data (
  id integer primary key autoincrement,
  SensorID text,
  Date_n_Time text,
  Humidity text
);

drop table if exists Pressure_Data;
create table Pressure_Data (
  id integer primary key autoincrement,
  SensorID text,
  Date_n_Time text,
  Pressure text
);
"""

class DatabaseManager():
	def __init__(self):
		self.conn = sqlite3.connect(DB_Name)
		self.conn.execute('pragma foreign_keys = on')
		self.conn.commit()
		self.cur = self.conn.cursor()
		
	def add_del_update_db_record(self, sql_query, args=()):
		self.cur.execute(sql_query, args)
		self.conn.commit()
		return

	def __del__(self):
		self.cur.close()
		self.conn.close()

def build_db(TableSchema):
	#Connect or Create DB File
	conn = sqlite3.connect(DB_Name)
	curs = conn.cursor()

	#Create Tables
	sqlite3.complete_statement(TableSchema)
	curs.executescript(TableSchema)

	#Close DB
	curs.close()
	conn.close()

def check_and_create_db():
    """Check if database exists and create tables only if they don't exist"""
    conn = sqlite3.connect(DB_Name)
    curs = conn.cursor()
    
    # Check if tables exist
    curs.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Temperature_Data'")
    if not curs.fetchone():
        # Tables don't exist, create them
        sqlite3.complete_statement(TableSchema)
        curs.executescript(TableSchema)
        print("Database tables created.")
    
    curs.close()
    conn.close()

# Function to save Temperature to DB Table
def Temp_Data_Handler(jsonData):
	#Parse Data 
	json_Dict = json.loads(jsonData)
	SensorID = json_Dict['Sensor_ID']
	Data_and_Time = json_Dict['Date']
	Temperature = json_Dict['Temperature']
	
	#Push into DB Table
	dbObj = DatabaseManager()
	dbObj.add_del_update_db_record("insert into Temperature_Data (SensorID, Date_n_Time, Temperature) values (?,?,?)",[SensorID, Data_and_Time, Temperature])
	del dbObj
	print("Inserted Temperature Data into Database.")

# Function to save Humidity to DB Table
def Humidity_Data_Handler(jsonData):
	json_Dict = json.loads(jsonData)
	SensorID = json_Dict['Sensor_ID']
	Data_and_Time = json_Dict['Date']
	try:
		Humidity = json_Dict['Humidity']
		dbObj = DatabaseManager()
		dbObj.add_del_update_db_record("insert into Humidity_Data (SensorID, Date_n_Time, Humidity) values (?,?,?)",[SensorID, Data_and_Time, Humidity])
		del dbObj
		print("Inserted Humidity Data into Database.")
	except:
		""

def Pressure_Data_Handler(jsonData):
    json_Dict = json.loads(jsonData)
    SensorID = json_Dict['Sensor_ID']
    Data_and_Time = json_Dict['Date']
    try:
        Pressure = json_Dict['Pressure']
        dbObj = DatabaseManager()
        dbObj.add_del_update_db_record(
            "insert into Pressure_Data (SensorID, Date_n_Time, Pressure) values (?,?,?)",
            [SensorID, Data_and_Time, Pressure]
        )
        del dbObj
        print("Inserted Pressure Data into Database.")
    except Exception as e:
        print(f"Error inserting pressure data: {e}")

# Function to read and display all database contents
def read_database_contents():
    """Read and display all sensor data from the database"""
    # Ensure database and tables exist without dropping existing data
    check_and_create_db()
    
    conn = sqlite3.connect(DB_Name)
    cur = conn.cursor()
    
    print("\n" + "="*50)
    print("DATABASE CONTENTS")
    print("="*50)
    
    # Read Temperature Data
    print("\nTEMPERATURE DATA:")
    print("-" * 40)
    cur.execute("SELECT * FROM Temperature_Data ORDER BY Date_n_Time DESC")
    temp_data = cur.fetchall()
    if temp_data:
        for row in temp_data:
            print(f"ID: {row[0]}, Sensor: {row[1]}, Date: {row[2]}, Temperature: {row[3]}°C")
    else:
        print("No temperature data found.")
    
    # Read Humidity Data
    print("\nHUMIDITY DATA:")
    print("-" * 40)
    cur.execute("SELECT * FROM Humidity_Data ORDER BY Date_n_Time DESC")
    humidity_data = cur.fetchall()
    if humidity_data:
        for row in humidity_data:
            print(f"ID: {row[0]}, Sensor: {row[1]}, Date: {row[2]}, Humidity: {row[3]}%")
    else:
        print("No humidity data found.")
    
    # Read Pressure Data
    print("\nPRESSURE DATA:")
    print("-" * 40)
    cur.execute("SELECT * FROM Pressure_Data ORDER BY Date_n_Time DESC")
    pressure_data = cur.fetchall()
    if pressure_data:
        for row in pressure_data:
            print(f"ID: {row[0]}, Sensor: {row[1]}, Date: {row[2]}, Pressure: {row[3]} hPa")
    else:
        print("No pressure data found.")
    
    cur.close()
    conn.close()
    print("="*50)

def sensor_Data_Handler(Topic, jsonData):
	if Topic == "Home/BedRoom/1/Temperature":
		Temp_Data_Handler(jsonData)
	elif Topic == "Home/BedRoom/1/Humidity":
		Humidity_Data_Handler(jsonData)	
	elif Topic == "Home/BedRoom/1/Pressure":
		Pressure_Data_Handler(jsonData)

def on_message(client, userdata, message):
	print("received message: " ,str(message.payload.decode("utf-8")))
	sensor_Data_Handler(message.topic, message.payload)

if __name__ == "__main__":
    print("MQTT IoT Database Lab 4")
    print("Choose an option:")
    print("1. Start MQTT listener and store data")
    print("2. Read and display database contents")
    print("3. Clear database and start MQTT listener")
    
    choice = input("Enter your choice (1, 2, or 3): ").strip()
    
    if choice == "1":
        print("Starting MQTT listener...")
        check_and_create_db()  
        client = mqtt.Client("SnifferID", transport='websockets')
        client.connect(mqttBroker, 8000)
        client.subscribe("Home/BedRoom/#")  
        client.on_message = on_message
        print(f"Connected to {mqttBroker} and subscribed to {MQTT_Topic}")
        print("Waiting for messages... Press Ctrl+C to stop")
        try:
            client.loop_forever()
        except KeyboardInterrupt:
            print("\nStopping MQTT listener...")
            client.disconnect()
            
    elif choice == "2":
        read_database_contents()
        
    elif choice == "3":
        print("Clearing database and starting MQTT listener...")
        build_db(TableSchema)
        read_database_contents()  # Show empty database
        client = mqtt.Client("SnifferID", transport='websockets')
        client.connect(mqttBroker, 8000)
        client.subscribe("Home/BedRoom/#")  
        client.on_message = on_message
        print(f"Connected to {mqttBroker} and subscribed to {MQTT_Topic}")
        print("Waiting for messages... Press Ctrl+C to stop")
        try:
            client.loop_forever()
        except KeyboardInterrupt:
            print("\nStopping MQTT listener...")
            client.disconnect()
            
    else:
        print("Invalid choice. Please run the program again.")
