# Python Web Scraping and API Integration Assignment

## Overview

This assignment demonstrates the fundamentals of Python programming through a comprehensive web scraping and API integration application. The project includes three main components:

1. **Web Scraper**: Fetches data from multiple APIs and saves to JSON files
2. **Flask Visualizer**: Displays scraped data in a web browser
3. **MQTT Publisher**: Sends scraped data to MQTT topics for IoT integration

## Project Structure

```
assignment/
├── web_scraper.py          # Main web scraping application
├── flask_visualizer.py     # Flask web application for data visualization
├── mqtt_publisher.py       # MQTT publisher for IoT integration
├── requirements.txt        # Python dependencies
├── README.md              # This documentation file
├── templates/
│   └── dashboard.html     # Main dashboard template
└── data/                  # Directory for scraped JSON files
    ├── output.json        # Combined output file
    ├── jsonplaceholder_posts.json
    ├── cat_facts.json
    └── weather_data.json
```

## Features

### 1. Web Scraper (`web_scraper.py`)
- **Object-Oriented Design**: Uses classes and methods
- **Multiple API Sources**: 
  - JSONPlaceholder API (fake blog posts)
  - Cat Facts API (random cat facts)
  - Weather API (sample weather data)
- **Error Handling**: Robust exception handling for network issues
- **JSON File Output**: Saves data to multiple JSON files
- **Data Aggregation**: Combines data from multiple sources

### 2. Flask Visualizer (`flask_visualizer.py`)
- **Web Dashboard**: Beautiful Bootstrap-based interface
- **Real-time Data**: Live API calls for fresh content
- **Multiple Views**: Different pages for different data types
- **JSON API Endpoints**: RESTful API for data access
- **Responsive Design**: Mobile-friendly interface

### 3. MQTT Publisher (`mqtt_publisher.py`)
- **MQTT Integration**: Publishes data to MQTT topics
- **Multiple Topics**: Organizes data into logical topic structure
- **Continuous Publishing**: Option for real-time data streaming
- **Quality of Service**: Configurable QoS levels
- **Error Recovery**: Handles connection issues gracefully

## Installation

### 1. Install Dependencies

```bash
cd /var/home/mark/Documents/semester6/smart_devices/mqtt_labs/assignment
pip install -r requirements.txt
```

### 2. Create Data Directory

```bash
mkdir -p data
```

## Usage

### Step 1: Run Web Scraper

```bash
python web_scraper.py
```

This will:
- Fetch data from multiple APIs
- Save individual JSON files to `data/` directory
- Create a combined `output.json` file
- Display progress and results

### Step 2: Visualize Data in Browser

```bash
python flask_visualizer.py
```

Then open your browser and go to: `http://localhost:5001`

Available endpoints:
- `/` - Main dashboard
- `/posts` - Blog posts data
- `/weather` - Weather information
- `/facts` - Cat facts
- `/api/data` - All data as JSON
- `/api/live` - Live data feed

### Step 3: Publish to MQTT

```bash
python mqtt_publisher.py
```

Choose from publishing options:
1. Single publishing session
2. Continuous publishing (60-second intervals)
3. Custom interval publishing

MQTT Topics used:
- `api/data/posts/{id}` - Individual blog posts
- `api/data/posts/summary` - Posts summary
- `api/data/catfacts/{id}` - Individual cat facts
- `api/data/weather/temperature` - Temperature data
- `api/data/weather/wind` - Wind data
- `api/data/weather/complete` - Complete weather data
- `api/data/combined` - All combined data
- `api/data/live` - Live data feed

## Code Documentation

### Web Scraper Components

```python
class APIWebScraper:
    """Main scraper class with methods for different APIs"""
    
    def fetch_from_jsonplaceholder(self):
        """Fetches blog posts from JSONPlaceholder API"""
    
    def fetch_from_cat_facts_api(self):
        """Fetches cat facts from Cat Facts API"""
    
    def save_to_json(self, data, filename):
        """Saves data to JSON file with metadata"""
```

### Flask Application Structure

```python
class DataVisualizer:
    """Handles data loading and processing for visualization"""
    
    def load_json_file(self, filename):
        """Loads JSON data from scraped files"""
    
    def get_live_data(self):
        """Fetches fresh data from APIs for real-time display"""
```

### MQTT Publisher Architecture

```python
class MQTTDataPublisher:
    """MQTT client for publishing scraped data"""
    
    def publish_data(self, topic, data):
        """Publishes JSON data to MQTT topic"""
    
    def start_continuous_publishing(self, interval):
        """Continuous publishing with specified interval"""
```

## Testing

### Testing Web Scraper

1. Run the scraper: `python web_scraper.py`
2. Check `data/` directory for JSON files
3. Verify JSON structure and content

### Testing Flask Application

1. Start Flask app: `python flask_visualizer.py`
2. Open browser to `http://localhost:5001`
3. Navigate through different pages
4. Test API endpoints: `/api/data`, `/api/live`

### Testing MQTT Publisher

1. Use MQTT client (like MQTTBox) to subscribe to topics
2. Run publisher: `python mqtt_publisher.py`
3. Verify messages are received on subscribed topics
4. Check message format and content

## API Sources

1. **JSONPlaceholder** (`https://jsonplaceholder.typicode.com/`)
   - Free fake JSON API for testing
   - Provides blog posts, users, comments, etc.
   - No authentication required

2. **Cat Facts API** (`https://catfact.ninja/`)
   - Free API providing random cat facts
   - Simple JSON responses
   - No rate limiting

3. **Weather API** (Sample data)
   - Demonstrates weather API structure
   - Uses sample data for demonstration
   - Shows real API integration patterns

## Error Handling

The application includes comprehensive error handling:

- **Network Errors**: Handles connection timeouts and failures
- **JSON Parsing**: Manages malformed JSON responses
- **File Operations**: Handles file not found and permission errors
- **MQTT Connectivity**: Manages broker connection issues

## Learning Objectives Achieved

### Python Programming Fundamentals
- ✅ Variables and data types
- ✅ Functions and classes
- ✅ Error handling with try/except
- ✅ File I/O operations
- ✅ JSON data manipulation

### Web Development
- ✅ HTTP requests with `requests` library
- ✅ Flask web framework
- ✅ HTML templating with Jinja2
- ✅ Bootstrap CSS framework
- ✅ JavaScript for interactivity

### API Integration
- ✅ RESTful API consumption
- ✅ JSON data parsing
- ✅ Rate limiting consideration
- ✅ Authentication concepts

### MQTT Protocol
- ✅ MQTT client implementation
- ✅ Topic-based messaging
- ✅ Quality of Service (QoS)
- ✅ Continuous data streaming

## Conclusion

This assignment successfully demonstrates:

1. **Web Scraping Skills**: Fetching data from multiple APIs with error handling
2. **Data Processing**: JSON manipulation and file operations
3. **Web Visualization**: Creating interactive dashboards with Flask
4. **IoT Integration**: MQTT protocol for real-time data distribution
5. **Best Practices**: Code organization, documentation, and error handling

The application serves as a foundation for more complex IoT and web development projects, showcasing practical Python programming skills in real-world scenarios.

## Future Enhancements

- Add database storage (SQLite/PostgreSQL)
- Implement user authentication
- Add data caching for better performance
- Include more API sources
- Add automated testing
- Implement logging system
- Add configuration management
- Create Docker containerization
