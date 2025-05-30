import requests
import json
import time
from datetime import datetime
import os

class APIWebScraper:
    """
    A web scraper class that fetches data from APIs and saves it to JSON files.
    This class demonstrates basic Python programming concepts and API integration.
    """
    
    def __init__(self, output_dir="data"):
        """
        Initialize the web scraper with output directory
        
        Args:
            output_dir (str): Directory to save JSON output files
        """
        self.output_dir = output_dir
        self.ensure_output_directory()
        
    def ensure_output_directory(self):
        """Create output directory if it doesn't exist"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            print(f"Created output directory: {self.output_dir}")
    
    def fetch_from_jsonplaceholder(self):
        """
        Fetch data from JSONPlaceholder API (a free testing API)
        This API provides fake JSON data for testing and prototyping
        
        Returns:
            dict: JSON response from the API
        """
        try:
            # JSONPlaceholder provides fake JSON data for testing
            url = "https://jsonplaceholder.typicode.com/posts"
            
            print(f"Fetching data from: {url}")
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # Raise an exception for bad status codes
            
            data = response.json()
            print(f"Successfully fetched {len(data)} posts")
            return data
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None
    
    def fetch_from_cat_facts_api(self):
        """
        Fetch data from Cat Facts API (alternative API source)
        
        Returns:
            dict: JSON response from the API
        """
        try:
            url = "https://catfact.ninja/facts?limit=10"
            
            print(f"Fetching cat facts from: {url}")
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            print(f"Successfully fetched {len(data.get('data', []))} cat facts")
            return data
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching cat facts: {e}")
            return None
    
    def fetch_from_weather_api(self):
        """
        Fetch weather data from OpenWeatherMap API (free tier)
        Note: This requires an API key for full functionality
        
        Returns:
            dict: JSON response from the API
        """
        try:
            # Using a sample weather API endpoint (this one doesn't require API key)
            url = "https://api.openweathermap.org/data/2.5/weather?q=London&appid=demo&units=metric"
            
            print(f"Fetching weather data from: {url}")
            response = requests.get(url, timeout=10)
            
            # Note: This will likely return an error due to invalid API key
            # but demonstrates the structure for real API integration
            if response.status_code == 200:
                data = response.json()
                print("Successfully fetched weather data")
                return data
            else:
                print(f"Weather API returned status code: {response.status_code}")
                # Return sample weather data for demonstration
                return self.get_sample_weather_data()
                
        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather data: {e}")
            return self.get_sample_weather_data()
    
    def get_sample_weather_data(self):
        """
        Provide sample weather data when API is not accessible
        
        Returns:
            dict: Sample weather data structure
        """
        return {
            "coord": {"lon": -0.1257, "lat": 51.5085},
            "weather": [{"id": 800, "main": "Clear", "description": "clear sky", "icon": "01d"}],
            "main": {
                "temp": 22.5,
                "feels_like": 23.1,
                "temp_min": 20.0,
                "temp_max": 25.0,
                "pressure": 1013,
                "humidity": 65
            },
            "wind": {"speed": 3.5, "deg": 180},
            "clouds": {"all": 0},
            "dt": int(time.time()),
            "sys": {"country": "GB", "sunrise": 1640757600, "sunset": 1640789200},
            "timezone": 0,
            "id": 2643743,
            "name": "London",
            "cod": 200,
            "note": "This is sample data for demonstration purposes"
        }
    
    def save_to_json(self, data, filename="output.json"):
        """
        Save data to JSON file with timestamp and formatting
        
        Args:
            data (dict): Data to save
            filename (str): Output filename
        """
        if data is None:
            print("No data to save")
            return False
            
        try:
            # Add metadata to the data
            output_data = {
                "timestamp": datetime.now().isoformat(),
                "scraping_info": {
                    "scraper_version": "1.0",
                    "total_records": len(data) if isinstance(data, list) else 1,
                    "data_source": "API Integration Demo"
                },
                "data": data
            }
            
            filepath = os.path.join(self.output_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=4, ensure_ascii=False)
            
            print(f"Data successfully saved to: {filepath}")
            return True
            
        except Exception as e:
            print(f"Error saving data to JSON: {e}")
            return False
    
    def run_scraping_session(self):
        """
        Run a complete scraping session with multiple APIs
        Demonstrates the full workflow of the web scraper
        """
        print("="*60)
        print("WEB SCRAPER APPLICATION - STARTING SCRAPING SESSION")
        print("="*60)
        
        # Scrape from JSONPlaceholder API
        print("\n1. Scraping JSONPlaceholder API...")
        posts_data = self.fetch_from_jsonplaceholder()
        if posts_data:
            self.save_to_json(posts_data, "jsonplaceholder_posts.json")
        
        # Scrape from Cat Facts API
        print("\n2. Scraping Cat Facts API...")
        cat_facts = self.fetch_from_cat_facts_api()
        if cat_facts:
            self.save_to_json(cat_facts, "cat_facts.json")
        
        # Scrape weather data
        print("\n3. Scraping Weather API...")
        weather_data = self.fetch_from_weather_api()
        if weather_data:
            self.save_to_json(weather_data, "weather_data.json")
        
        # Create a combined output file
        print("\n4. Creating combined output...")
        combined_data = {
            "posts": posts_data[:5] if posts_data else [],  # First 5 posts only
            "cat_facts": cat_facts.get('data', [])[:3] if cat_facts else [],  # First 3 facts
            "weather": weather_data
        }
        self.save_to_json(combined_data, "output.json")
        
        print("\n" + "="*60)
        print("SCRAPING SESSION COMPLETED")
        print("="*60)

def main():
    """
    Main function to demonstrate the web scraper functionality
    """
    print("Python Web Scraper and API Integration Demo")
    print("This application demonstrates:")
    print("- HTTP requests to APIs")
    print("- JSON data parsing and manipulation")
    print("- File I/O operations")
    print("- Error handling")
    print("- Object-oriented programming in Python")
    
    # Create and run the scraper
    scraper = APIWebScraper()
    scraper.run_scraping_session()
    
    print("\nFiles created in the 'data' directory:")
    if os.path.exists("data"):
        for file in os.listdir("data"):
            if file.endswith('.json'):
                print(f"  - {file}")

if __name__ == "__main__":
    main()
