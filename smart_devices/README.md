# Smart Devices - Semester 6

## Laboratory Work

### MQTT Protocol Labs

- [Lab 1: JSON Usage](mqtt_labs/reports/lab1_report.md)
- [Lab 2: JSON File Merging](mqtt_labs/reports/lab2_report.md)  
- [Lab 3: MQTT Basic Implementation](mqtt_labs/reports/lab3/)
- [Lab 4: MQTT with Database Storage](mqtt_labs/reports/lab4/)
- [Lab 5: MQTT Data Visualization](mqtt_labs/reports/lab5/)

### Web Development

- [Flask Lab](flask_lab/)

### Mobile Development
- [Lab 1: Expo Mobile App Setup](expo_labs/lab1/)
- [Lab 2: Expo Sensor Integration](expo_labs/lab2/)
- [Lab 3: Expo Data Visualization](expo_labs/lab3/)

### Final Coursework

- [API Integration & Data Visualization Assignment](coursework/)

## Project Structure

```
smart_devices/
├── coursework/               # Final coursework
│   ├── README.md
│   ├── flask_visualizer.py
│   ├── mqtt_publisher.py
│   ├── web_scraper.py
│   ├── requirements.txt
│   ├── data/
│   └── templates/
├── mqtt_labs/
│   ├── reports/               # All lab reports
│   │   ├── lab1_report.md     # JSON Usage
│   │   ├── lab2_report.md     # JSON File Merging
│   │   ├── lab3/              # MQTT Basic Implementation
│   │   │   └── lab3_report.md 
│   │   ├── lab4/              # MQTT with Database Storage
│   │   │   ├── lab4_report.md 
│   │   │   └── mqtt_iot_db.py # Database implementation
│   │   └── lab5/              # MQTT Data Visualization
│   │       ├── lab5_report.md 
│   │       ├── templates/
│   │       │   └── index.html
│   │       └── mqtt_project/
│   │           ├── flask_mqtt_pavyzdys.py
│   │           └── templates/
│   │               └── index.html
│   └── .gitignore            # Excludes working directories from mqtt_labs
├── expo_labs/                # Mobile development
│   ├── lab1/
│   ├── lab2/
│   ├── lab3/
│   └── .gitignore            # Excludes Expo app build/dev directories
└── flask_lab/                # Web development
```

## Technologies Used

- **MQTT Protocol**: Message queuing for IoT communication
- **Flask**: Python web framework with Socket.IO for real-time updates
- **Bootstrap 5**: Responsive web UI framework
- **SQLite**: Database for sensor data storage
- **JSON**: Data interchange format
- **Python**: Primary programming language
- **JavaScript**: Frontend interactivity
- **Expo/React Native**: Mobile app development

## Notes

Working lab directories (`lab2/`, `lab4/`, `lab5/`) are excluded from version control via `.gitignore` to keep the repository focused on documentation and reports only.
