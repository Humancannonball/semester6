# Smart Devices - Semester 6

## Laboratory Work

### MQTT Protocol Labs

- [Lab 1: JSON Usage](reports/lab1_report.md)
- [Lab 2: JSON File Merging](reports/lab2_report.md)  
- [Lab 3: MQTT Basic Implementation](mqtt_labs/reports/lab3/lab3_report.md)
- [Lab 4: MQTT with Database Storage](mqtt_labs/reports/lab4/lab4_report.md)
- [Lab 5: MQTT Data Visualization](mqtt_labs/reports/lab5/lab5_report.md)

### Web Development

- [Flask Lab](flask_lab/)

### Mobile Development

- [Expo Framework Testing](expo_labs/README.md)

### Final Coursework

- [API Integration & Data Visualization Assignment](mqtt_labs/coursework/README.md)

## Project Structure

```
smart_devices/
├── reports/
│   ├── lab1_report.md          # JSON Usage
│   ├── lab2_report.md          # JSON File Merging
│   └── ...other reports
├── mqtt_labs/
│   ├── reports/               # Lab reports only
│   │   ├── lab3/
│   │   │   └── lab3_report.md
│   │   ├── lab4/
│   │   │   └── lab4_report.md
│   │   └── lab5/
│   │       ├── lab5_report.md
│   │       ├── templates/
│   │       │   └── index.html
│   │       └── mqtt_project/
│   │           └── templates/
│   │               └── index.html
│   └── .gitignore            # Excludes working directories
├── expo_labs/                # Mobile development
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
