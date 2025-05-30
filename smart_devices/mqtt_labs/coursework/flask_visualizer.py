from flask import Flask, render_template, jsonify
import json
import os
from datetime import datetime
import requests

app = Flask(__name__)

class DataVisualizer:
    """
    A class to handle data loading and processing for web visualization
    """
    
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
    
    def load_json_file(self, filename):
        """
        Load JSON data from file
        
        Args:
            filename (str): Name of the JSON file to load
            
        Returns:
            dict: Loaded JSON data or None if file doesn't exist
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
    
    def get_all_data(self):
        """
        Load all scraped data files
        
        Returns:
            dict: Dictionary containing all loaded data
        """
        data = {}
        
        # Load main output file
        output_data = self.load_json_file("output.json")
        if output_data:
            data['main'] = output_data
        
        # Load individual files
        files_to_load = [
            ("posts", "jsonplaceholder_posts.json"),
            ("cat_facts", "cat_facts.json"),
            ("weather", "weather_data.json")
        ]
        
        for key, filename in files_to_load:
            file_data = self.load_json_file(filename)
            if file_data:
                data[key] = file_data
        
        return data
    
    def get_live_data(self):
        """
        Fetch live data from APIs for real-time display
        
        Returns:
            dict: Live data from various APIs
        """
        live_data = {}
        
        try:
            # Fetch a random cat fact
            response = requests.get("https://catfact.ninja/fact", timeout=5)
            if response.status_code == 200:
                live_data['cat_fact'] = response.json()
        except:
            live_data['cat_fact'] = {"fact": "Cats are amazing creatures!", "length": 26}
        
        try:
            # Fetch a random quote
            response = requests.get("https://api.quotable.io/random", timeout=5)
            if response.status_code == 200:
                live_data['quote'] = response.json()
        except:
            live_data['quote'] = {"content": "The journey of a thousand miles begins with one step.", "author": "Lao Tzu"}
        
        live_data['timestamp'] = datetime.now().isoformat()
        return live_data

# Initialize data visualizer
visualizer = DataVisualizer()

@app.route('/')
def index():
    """
    Main dashboard page showing all scraped data
    """
    data = visualizer.get_all_data()
    return render_template('dashboard.html', data=data)

@app.route('/api/data')
def api_data():
    """
    API endpoint to get all scraped data as JSON
    """
    data = visualizer.get_all_data()
    return jsonify(data)

@app.route('/api/live')
def api_live():
    """
    API endpoint to get live data
    """
    live_data = visualizer.get_live_data()
    return jsonify(live_data)

@app.route('/posts')
def posts_page():
    """
    Dedicated page for blog posts data
    """
    posts_data = visualizer.load_json_file("jsonplaceholder_posts.json")
    return render_template('posts.html', posts_data=posts_data)

@app.route('/weather')
def weather_page():
    """
    Dedicated page for weather data
    """
    weather_data = visualizer.load_json_file("weather_data.json")
    return render_template('weather.html', weather_data=weather_data)

@app.route('/facts')
def facts_page():
    """
    Dedicated page for cat facts
    """
    facts_data = visualizer.load_json_file("cat_facts.json")
    return render_template('facts.html', facts_data=facts_data)

if __name__ == '__main__':
    print("Starting Flask Data Visualization Server...")
    print("Dashboard will be available at: http://localhost:5001")
    print("\nAvailable endpoints:")
    print("  - /          : Main dashboard")
    print("  - /posts     : Blog posts data")
    print("  - /weather   : Weather data")
    print("  - /facts     : Cat facts data")
    print("  - /api/data  : All data as JSON")
    print("  - /api/live  : Live data as JSON")
    
    app.run(host='localhost', port=5001, debug=True)
