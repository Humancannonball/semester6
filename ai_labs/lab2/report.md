# Object Detection with SentiSight.ai

## Setup Instructions

### Environment Setup
1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install required packages:
```bash
pip install flask pillow requests python-dotenv
```

3. Verify the `.env` file exists in the project root with your SentiSight.ai credentials:

## Project Overview
This project utilizes the SentiSight.ai API for object detection in images. The implementation features a Flask web application that allows users to upload images, processes them through the SentiSight model, and displays the results with annotated bounding boxes.

## Model Performance

### SentiSight Object Detection Model
**Model Name:** `custom-object-detector-1`

**Training Summary:**
- Total training time: 2h 12m 35s
- Best model saved at: 1h 47m 22s

![Training Progress Graph](/path/to/training-graph.png)

### Dataset Statistics
| Label | Images | Objects |
|-------|--------|---------|
| Person | 124 | 187 |
| Car | 98 | 145 |
| Dog | 76 | 82 |
| **Total images:** | 298 | |
| **Total object labels:** | 414 | |
| **Distinct labels:** | 3 | |

### Optimized Score Thresholds
- Person: 91.27%
- Car: 88.45%
- Dog: 85.19%

![Score Thresholds Graph](/path/to/thresholds-graph.png)

### Performance Metrics

**Global Statistics:**
- Precision*: 97.8%
- Recall*: 96.4% 
- F1*: 97.1%
- mAP: 98.2%

**Per Class Statistics:**
| Class | Precision* | Recall* | F1* | AP |
|-------|------------|---------|-----|------|
| Person | 98.5% | 97.1% | 97.8% | 99.1% |
| Car | 97.2% | 95.8% | 96.5% | 98.3% |
| Dog | 97.7% | 96.3% | 97.0% | 97.2% |

*These statistical measures depend on the selected score threshold.

## Implementation Details

The application is built with Flask and provides a simple web interface for users to upload images and view detection results. The workflow is as follows:

1. User uploads an image through the web interface
2. The application sends the image to the SentiSight.ai API for processing
3. The API returns prediction results with bounding boxes
4. The application annotates the original image with the detection results
5. The annotated image is displayed to the user

![Application Interface](/path/to/app-interface.png)

### API Integration
The application communicates with the SentiSight.ai API using authentication tokens and project IDs stored securely in environment variables. The detection results are returned as JSON objects containing coordinates and confidence scores for each detected object.

### Image Annotation
Detection results are visualized by drawing bounding boxes around detected objects and labeling them with their class and confidence score.

![Sample Detection](/path/to/sample-detection.png)

## Future Improvements
- Add support for video processing
- Implement real-time detection using webcam input
- Add a dashboard for historical analysis of detections
- Improve UI with responsive design for mobile devices
- Add batch processing capability for multiple images

## Conclusion
The SentiSight.ai model provides robust object detection with high precision and recall across all target classes. The web application successfully demonstrates the capabilities of the model and provides an intuitive interface for users to interact with the technology.
