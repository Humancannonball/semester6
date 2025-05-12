import cv2
import time
from inference_sdk import InferenceHTTPClient
import numpy as np

def connect_to_model():
    # Initialize the Roboflow client
    client = InferenceHTTPClient(
        api_url="https://serverless.roboflow.com",
        api_key="gvIOiLe0SFh0wozPCJYg"
    )
    return client

def process_webcam(client, model_id="spagetti/6", device_id=0):
    # Connect to the local webcam
    cap = cv2.VideoCapture(device_id)
    
    if not cap.isOpened():
        print(f"Error: Cannot open webcam (device {device_id})")
        return
        
    print(f"Connected to webcam (device {device_id})")
    
    try:
        while True:
            # Read frame from webcam
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame from webcam")
                break
                
            # Convert frame to RGB (Roboflow expects RGB)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Get prediction from model
            prediction = client.infer(frame_rgb, model_id=model_id)
            
            # Process prediction (example: draw bounding boxes)
            # This will depend on the model output format
            visualize_prediction(frame, prediction)
            
            # Display the frame
            cv2.imshow("Webcam Stream", frame)
            
            # Exit on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
            # Limit the frame rate
            time.sleep(0.05)
            
    finally:
        cap.release()
        cv2.destroyAllWindows()

def process_ip_camera(client, ip_address, model_id="spagetti/6"):
    # Connect to the IP camera
    stream_url = f"http://{ip_address}/video"  # Modify URL pattern if needed
    cap = cv2.VideoCapture(stream_url)
    
    if not cap.isOpened():
        print(f"Error: Cannot connect to IP camera at {stream_url}")
        return
        
    print(f"Connected to IP camera at {stream_url}")
    
    try:
        while True:
            # Read frame from IP camera
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame from IP camera")
                break
                
            # Convert frame to RGB (Roboflow expects RGB)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Get prediction from model
            prediction = client.infer(frame_rgb, model_id=model_id)
            
            # Process prediction (example: draw bounding boxes)
            visualize_prediction(frame, prediction)
            
            # Display the frame
            cv2.imshow("3D Printer Camera Stream", frame)
            
            # Exit on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
            # Limit the frame rate
            time.sleep(0.05)
            
    finally:
        cap.release()
        cv2.destroyAllWindows()

def visualize_prediction(frame, prediction):
    """
    Visualize the prediction on the frame
    Customize this based on your model's output format
    """
    # Example for object detection model
    if 'predictions' in prediction:
        for pred in prediction['predictions']:
            if 'x' in pred and 'y' in pred and 'width' in pred and 'height' in pred:
                # Convert normalized coordinates to pixel values
                x = int(pred['x'] * frame.shape[1])
                y = int(pred['y'] * frame.shape[0])
                w = int(pred['width'] * frame.shape[1])
                h = int(pred['height'] * frame.shape[0])
                
                # Calculate bounding box coordinates
                x1 = int(x - w/2)
                y1 = int(y - h/2)
                x2 = int(x + w/2)
                y2 = int(y + h/2)
                
                # Draw bounding box
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                
                # Draw label
                if 'class' in pred and 'confidence' in pred:
                    label = f"{pred['class']}: {pred['confidence']:.2f}"
                    cv2.putText(frame, label, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

def main():
    # Connect to the model
    client = connect_to_model()
    model_id = "spagetti/6"
    
    # Process local webcam (for testing)
    # Uncomment to use:
    process_webcam(client, model_id=model_id)
    
    # Process 3D printer IP camera
    # Replace with your 3D printer camera's IP address
    # printer_ip = "192.168.1.100"  # Example IP, replace with your printer's IP
    # process_ip_camera(client, printer_ip, model_id=model_id)

if __name__ == "__main__":
    main()