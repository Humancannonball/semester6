import os
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import requests
import tarfile
import shutil
from pathlib import Path
import random
from config import *

def download_and_extract_dataset():
    """Download and extract the Oxford 102 Flowers dataset."""
    print("Downloading and extracting the dataset...")
    
    # Download flower images
    flowers_path = os.path.join(BASE_DIR, "102flowers.tgz")
    if not os.path.exists(flowers_path):
        print("Downloading flower images...")
        response = requests.get(DATASET_URL, stream=True)
        with open(flowers_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                f.write(chunk)
    
    # Extract flower images
    extract_dir = os.path.join(BASE_DIR, "extracted")
    if not os.path.exists(extract_dir):
        os.makedirs(extract_dir, exist_ok=True)
        print("Extracting flower images...")
        with tarfile.open(flowers_path) as tar:
            tar.extractall(path=extract_dir)
    
    # Download labels
    labels_path = os.path.join(BASE_DIR, "imagelabels.mat")
    if not os.path.exists(labels_path):
        print("Downloading labels...")
        response = requests.get(LABELS_URL)
        with open(labels_path, "wb") as f:
            f.write(response.content)
    
    print("Dataset download and extraction complete.")
    return extract_dir, labels_path

def prepare_dataset(extracted_dir, labels_path):
    """Prepare the dataset by organizing images into class folders."""
    print("Preparing the dataset...")
    
    # Load labels
    from scipy.io import loadmat
    labels = loadmat(labels_path)['labels'][0]
    
    # Count occurrences of each class to find the top N classes
    class_counts = {}
    for label in labels:
        if label not in class_counts:
            class_counts[label] = 0
        class_counts[label] += 1
    
    # Get top N classes with most images
    top_classes = sorted(class_counts.items(), key=lambda x: x[1], reverse=True)[:NUM_CLASSES]
    top_class_ids = [cls[0] for cls in top_classes]
    
    print(f"Selected top {NUM_CLASSES} classes: {top_class_ids}")
    
    # Create directories for dataset organization
    dataset_dir = os.path.join(BASE_DIR, "flowers_dataset")
    if os.path.exists(dataset_dir):
        print("Dataset already organized. Skipping preparation.")
        return dataset_dir
    
    os.makedirs(dataset_dir, exist_ok=True)
    
    # Source directory with all images
    source_dir = os.path.join(extracted_dir, "jpg")
    
    # Create class directories and copy images
    for cls_id in top_class_ids:
        class_dir = os.path.join(dataset_dir, f"class_{cls_id}")
        os.makedirs(class_dir, exist_ok=True)
    
    # Copy images to respective class folders
    for idx, label in enumerate(labels, 1):
        if label in top_class_ids:
            source_file = os.path.join(source_dir, f"image_{idx:05d}.jpg")
            target_file = os.path.join(dataset_dir, f"class_{label}", f"image_{idx:05d}.jpg")
            if os.path.exists(source_file) and not os.path.exists(target_file):
                shutil.copy(source_file, target_file)
    
    print("Dataset preparation complete.")
    return dataset_dir

def split_dataset(dataset_dir):
    """Split the dataset into train, validation, and test sets."""
    print("Splitting dataset into train, validation, and test sets...")
    
    from sklearn.model_selection import train_test_split
    
    train_dir = os.path.join(BASE_DIR, "train")
    val_dir = os.path.join(BASE_DIR, "validation")
    test_dir = os.path.join(BASE_DIR, "test")
    
    # Check if splits already exist
    if os.path.exists(train_dir) and os.path.exists(val_dir) and os.path.exists(test_dir):
        print("Dataset splits already exist. Skipping split.")
        return train_dir, val_dir, test_dir
    
    # Create directories
    for dir_path in [train_dir, val_dir, test_dir]:
        os.makedirs(dir_path, exist_ok=True)
        # Create class subdirectories
        for class_dir in os.listdir(dataset_dir):
            if os.path.isdir(os.path.join(dataset_dir, class_dir)):
                os.makedirs(os.path.join(dir_path, class_dir), exist_ok=True)
    
    # Split data for each class
    for class_dir in os.listdir(dataset_dir):
        class_path = os.path.join(dataset_dir, class_dir)
        if os.path.isdir(class_path):
            images = [img for img in os.listdir(class_path) if img.endswith('.jpg')]
            
            # Split into train (70%), validation (15%), and test (15%)
            train_imgs, temp_imgs = train_test_split(images, test_size=0.3, random_state=42)
            val_imgs, test_imgs = train_test_split(temp_imgs, test_size=0.5, random_state=42)
            
            # Copy images to respective directories
            for img in train_imgs:
                shutil.copy(os.path.join(class_path, img), os.path.join(train_dir, class_dir, img))
            for img in val_imgs:
                shutil.copy(os.path.join(class_path, img), os.path.join(val_dir, class_dir, img))
            for img in test_imgs:
                shutil.copy(os.path.join(class_path, img), os.path.join(test_dir, class_dir, img))
    
    print("Dataset split complete.")
    return train_dir, val_dir, test_dir

def create_data_generators(train_dir, val_dir, test_dir):
    """Create data generators with augmentation for training."""
    print("Creating data generators...")
    
    # Training data generator with augmentation
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        vertical_flip=True,
        brightness_range=[0.8, 1.2],
        fill_mode='nearest'
    )
    
    # Validation and test data generators (only rescaling)
    val_test_datagen = ImageDataGenerator(rescale=1./255)
    
    # Create generators
    train_generator = train_datagen.flow_from_directory(
        train_dir,
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        shuffle=True
    )
    
    validation_generator = val_test_datagen.flow_from_directory(
        val_dir,
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        shuffle=False
    )
    
    test_generator = val_test_datagen.flow_from_directory(
        test_dir,
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        shuffle=False
    )
    
    # Visualize some augmented images
    visualize_augmented_images(train_generator)
    
    return train_generator, validation_generator, test_generator

def visualize_augmented_images(train_generator):
    """Visualize sample original and augmented images."""
    plt.figure(figsize=(16, 8))
    
    # Get a batch of images and their labels
    x_batch, y_batch = next(train_generator)
    
    for i in range(min(8, len(x_batch))):
        plt.subplot(2, 4, i+1)
        plt.imshow(x_batch[i])
        class_idx = np.argmax(y_batch[i])
        class_name = list(train_generator.class_indices.keys())[class_idx]
        plt.title(f'Class: {class_name}')
        plt.axis('off')
    
    plt.suptitle('Sample Augmented Images')
    plt.savefig(os.path.join(RESULTS_DIR, 'augmented_images.png'))
    plt.close()

def prepare_data():
    """Main function to prepare the data."""
    # Download and prepare dataset
    extracted_dir, labels_path = download_and_extract_dataset()
    dataset_dir = prepare_dataset(extracted_dir, labels_path)
    train_dir, val_dir, test_dir = split_dataset(dataset_dir)
    
    # Create data generators
    train_generator, validation_generator, test_generator = create_data_generators(train_dir, val_dir, test_dir)
    
    return train_generator, validation_generator, test_generator
