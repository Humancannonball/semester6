import os
from pathlib import Path
from flask import Flask, render_template, request, send_from_directory
import requests
import json
from PIL import Image, ImageDraw
from dotenv import load_dotenv
import numpy as np
import base64
import io

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Configure application settings
UPLOAD_FOLDER = 'images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload directory exists
Path(UPLOAD_FOLDER).mkdir(exist_ok=True)

def get_api_credentials():
    """Get API credentials from environment variables."""
    return {
        'api_token': os.getenv('SENTISIGHT_API_TOKEN'),
        'project_id': os.getenv('SENTISIGHT_PROJECT_ID'),
        'model_name': os.getenv('SENTISIGHT_MODEL_NAME')
    }

def allowed_file(filename):
    """Check if the file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def make_prediction(image_path):
    """Make prediction using SentiSight.ai API."""
    credentials = get_api_credentials()
    
    # Use the single working endpoint format
    url = f"https://platform.sentisight.ai/api/predict/{credentials['project_id']}/{credentials['model_name']}/"
    
    print(f"Making API request to: {url}")
    
    headers = {
        "X-Auth-token": credentials['api_token'],
        "Content-Type": "application/octet-stream"
    }
    
    try:
        with open(image_path, 'rb') as image_file:
            response = requests.post(url, headers=headers, data=image_file)
        
        print(f"API Response Status: {response.status_code}")
        
        if response.status_code == 200:
            return json.loads(response.text)
        else:
            error_message = f"API error: {response.status_code}, {response.text}"
            print(error_message)
            raise Exception(error_message)
    except requests.RequestException as e:
        print(f"Request error: {e}")
        raise Exception(f"Connection error: {e}")

def annotate_image(image_path, prediction, annotated_path):
    """Annotate the image with prediction results."""
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    
    # Print prediction structure for debugging
    print("Prediction structure:", type(prediction))
    print(json.dumps(prediction, indent=2)[:500])  # Print first 500 chars
    
    # Check if the prediction contains segmentation masks
    if isinstance(prediction, dict) and 'segmentations' in prediction:
        # Handle segmentation masks
        print("Handling segmentation masks")
        for segment in prediction.get('segmentations', []):
            if 'mask' in segment and 'label' in segment:
                try:
                    # Create mask overlay
                    mask_data = base64.b64decode(segment['mask'])
                    mask = Image.open(io.BytesIO(mask_data))
                    
                    # Get bounding box if available for label placement
                    if 'bbox' in segment:
                        bbox = segment['bbox']
                        draw.rectangle(bbox, outline="red", width=2)
                        
                        # Add label with confidence score
                        label = segment.get('label', 'Unknown')
                        confidence = segment.get('confidence', 0) * 100
                        label_text = f"{label} ({confidence:.2f}%)"
                        draw.text((bbox[0], bbox[1] - 10), label_text, fill="red")
                except Exception as e:
                    print(f"Error processing mask: {e}")
    else:
        # Handle standard object detection results
        objects = []
        if isinstance(prediction, list):
            objects = prediction
        elif isinstance(prediction, dict) and 'predictions' in prediction:
            objects = prediction['predictions']
        elif isinstance(prediction, dict) and 'objects' in prediction:
            objects = prediction['objects']
        
        for obj in objects:
            # Check for different coordinate formats
            if all(k in obj for k in ['x0', 'y0', 'x1', 'y1']):
                coords = [obj['x0'], obj['y0'], obj['x1'], obj['y1']]  # Fixed syntax error here
            elif all(k in obj for k in ['bbox']):
                coords = obj['bbox']  # Assuming bbox is [x0, y0, x1, y1]
            else:
                print(f"Warning: Could not find coordinates in object: {obj}")
                continue
            
            # Draw bounding box
            draw.rectangle(coords, outline="red", width=2)
            
            # Add label with confidence score
            label = obj.get('label', obj.get('class', 'Unknown'))
            score = obj.get('score', obj.get('confidence', 0)) * 100  # Convert to percentage
            label_text = f"{label} ({score:.2f}%)"
            draw.text((coords[0], coords[1] - 10), label_text, fill="red")
    
    # Save the annotated image
    image.save(annotated_path)
    return os.path.basename(annotated_path)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    """Handle file uploads and process images."""
    if request.method != 'POST':
        return render_template('index.html')
    
    # Check if file is included in request
    if 'file' not in request.files:
        return render_template('index.html', message='No file part')
    
    file = request.files['file']
    if file.filename == '':
        return render_template('index.html', message='No selected file')
    
    if not allowed_file(file.filename):
        return render_template('index.html', message='File type not allowed')
    
    try:
        # Save uploaded file
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Process the image
        prediction = make_prediction(file_path)
        
        # Log prediction results for debugging
        print(json.dumps(prediction, indent=2))
        
        # Annotate and save the image
        annotated_filename = f"annotated_{filename}"
        annotated_path = os.path.join(app.config['UPLOAD_FOLDER'], annotated_filename)
        annotate_image(file_path, prediction, annotated_path)
        
        # Return both the annotated image and the raw prediction data to the template
        return render_template('index.html', 
                              filename=annotated_filename,
                              prediction=json.dumps(prediction, indent=2))
    
    except Exception as e:
        return render_template('index.html', message=f'Error: {str(e)}')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve uploaded files."""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)