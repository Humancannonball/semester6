# Task: Lab Work 3 - CNN Development and Training

## Overview
This lab work focuses on image classification using deep learning techniques. You will work with the Oxford 102 Flowers dataset to develop and train convolutional neural networks (CNNs) using two approaches: building a custom CNN from scratch and applying transfer learning with a pre-trained model.

## Objectives
- Learn fundamental principles of image classification using deep learning
- Master the key steps of model training and evaluation:
  - Data preparation and augmentation
  - Model architecture design
  - Training process optimization
  - Model performance assessment
- Compare the performance of custom-built and pre-trained models

## Dataset
Oxford 102 Flowers dataset containing images of 102 flower categories.
- [Dataset Link](https://www.robots.ox.ac.uk/~vgg/data/flowers/102/)
- For this lab, select 5-10 classes with the highest number of images

## Tasks

### Part 1: Custom CNN (6 points)

1. **Setup Environment**
   - Configure Google Colab with TensorFlow and Keras

2. **Data Preparation (1.5 points)**
   - Load the Oxford 102 Flowers dataset
   - Select 5-10 classes with the highest number of images
   - Split data into training and testing sets
   - Normalize images
   - Implement image augmentation:
     - Rotation, shift, zoom
     - Horizontal and vertical flipping
     - Brightness adjustment
     - Random crop, color jitter

3. **CNN Model Creation (2 points)**
   - Design a custom CNN architecture with:
     - Convolutional layers with different padding parameters
     - Multiple convolutional layers between pooling layers
     - Dropout layers between convolutional layers
     - Multiple dense layers in the classification part

4. **Model Training (1 point)**
   - Use a portion of the training data for validation
   - Select appropriate loss function and optimizer
   - Monitor training/validation accuracy and loss
   - Save the best model (lowest validation loss) and final epoch model

5. **Evaluation and Visualization (1.5 points)**
   - Evaluate model performance on test data
   - Generate and visualize:
     - Accuracy and loss curves
     - Confusion matrix
     - Precision, recall, and F1 metrics
     - Prediction examples with ground truth labels

### Part 2: Transfer Learning and Fine-tuning (4 points)

1. **Pre-trained Model Selection**
   - Choose a pre-trained model from [Keras Applications](https://keras.io/api/applications/)

2. **Transfer Learning and Fine-tuning (2 points)**
   - Replace classification head with layers suitable for the flower dataset
   - Train only the new classification layers first
   - Unfreeze portions of the convolutional base for fine-tuning
   - Continue training with a lower learning rate

3. **Evaluation and Comparison (2 points)**
   - Monitor training and validation metrics
   - Evaluate performance with testing dataset
   - Compare with custom CNN model results
   - Analyze strengths and weaknesses of both approaches

## Requirements
- Visualize dataset images before and after augmentation
- Display model architecture summaries
- Show training and validation metrics throughout training
- Present prediction results of best models (image, true class, prediction probability)
- Include clear analysis and comparison of both models

## Submission Guidelines
- Upload all project files to a public GitHub repository
- Submit the repository link on Moodle
- Be prepared to present and defend your code and results

## Implementation Plan

### Step 1: Setting up the environment
- Install necessary libraries (TensorFlow, Keras, Matplotlib, NumPy, etc.)
- Import required modules
- Configure hardware accelerators if available

### Step 2: Data acquisition and exploration
- Download the Oxford 102 Flowers dataset
- Explore dataset structure and class distribution
- Visualize sample images from different classes

### Step 3: Data preprocessing
- Create data loading pipelines
- Implement data augmentation functions
- Split data into training, validation, and test sets
- Normalize pixel values

### Step 4: Custom CNN development
- Design CNN architecture
- Implement model using Keras
- Configure loss function and optimizer
- Set up callbacks for model checkpointing

### Step 5: Model training and monitoring
- Train the custom CNN model
- Monitor training and validation metrics
- Save best performing model
- Visualize training progress

### Step 6: Transfer learning implementation
- Load pre-trained model
- Configure new classification head
- Freeze base layers for initial training
- Unfreeze selective layers for fine-tuning

### Step 7: Evaluation and comparison
- Evaluate both models on test set
- Generate performance metrics
- Create visualizations of predictions
- Compare and analyze results

## Useful Resources
- [Image Classification from Scratch](https://keras.io/examples/vision/image_classification_from_scratch/)
- [Transfer Learning Guide](https://keras.io/guides/transfer_learning/)
- [Oxford 102 Flowers Dataset](https://www.robots.ox.ac.uk/~vgg/data/flowers/102/)
- [Albumentations Library](https://albumentations.ai/) for image augmentations
- [Scikit-learn](https://scikit-learn.org/) for visualization and metrics

## Grading Criteria
- Custom CNN (6 points):
  - Data preparation and augmentation (1.5 points)
  - Model design and explanation (2 points)
  - Training process optimization (1 point)
  - Evaluation metrics (1 point)
  - Prediction visualization (0.5 points)

- Transfer Learning (4 points):
  - Model selection and fine-tuning process (2 points)
  - Evaluation metrics (1 point)
  - Model comparison analysis (1 point)
