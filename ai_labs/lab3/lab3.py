import os
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Dense, Dropout, Conv2D, MaxPooling2D, Flatten, BatchNormalization, Input, GlobalAveragePooling2D
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import requests
import tarfile
import shutil
from pathlib import Path
import random
from sklearn.utils.class_weight import compute_class_weight
import seaborn as sns

# Set random seeds for reproducibility
np.random.seed(42)
tf.random.set_seed(42)
random.seed(42)

# Constants
IMG_SIZE = 224
BATCH_SIZE = 32
EPOCHS = 20
NUM_CLASSES = 10  # We'll use top 10 classes with most images
DATASET_URL = "https://www.robots.ox.ac.uk/~vgg/data/flowers/102/102flowers.tgz"
LABELS_URL = "https://www.robots.ox.ac.uk/~vgg/data/flowers/102/imagelabels.mat"
BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dataset")
MODEL_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models")

# Create necessary directories
os.makedirs(BASE_DIR, exist_ok=True)
os.makedirs(MODEL_DIR, exist_ok=True)

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
    plt.savefig(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'augmented_images.png'))
    plt.close()

def create_custom_cnn_model(input_shape, num_classes):
    """Create a custom CNN model."""
    print("Creating custom CNN model...")
    
    model = Sequential([
        # First convolutional block - with 'same' padding
        Conv2D(32, (3, 3), activation='relu', padding='same', input_shape=input_shape),
        Conv2D(32, (3, 3), activation='relu', padding='same'),
        BatchNormalization(),
        MaxPooling2D(2, 2),
        Dropout(0.25),
        
        # Second convolutional block - with 'valid' padding
        Conv2D(64, (3, 3), activation='relu', padding='valid'),
        Conv2D(64, (3, 3), activation='relu', padding='valid'),
        BatchNormalization(),
        MaxPooling2D(2, 2),
        Dropout(0.25),
        
        # Third convolutional block
        Conv2D(128, (3, 3), activation='relu', padding='same'),
        Conv2D(128, (3, 3), activation='relu', padding='same'),
        Conv2D(128, (3, 3), activation='relu', padding='same'),
        BatchNormalization(),
        MaxPooling2D(2, 2),
        Dropout(0.3),
        
        # Flatten and dense layers
        Flatten(),
        Dense(512, activation='relu'),
        BatchNormalization(),
        Dropout(0.5),
        Dense(256, activation='relu'),
        Dropout(0.3),
        Dense(num_classes, activation='softmax')
    ])
    
    # Compile model
    model.compile(
        optimizer=Adam(learning_rate=0.001),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model

def train_custom_model(model, train_generator, validation_generator):
    """Train the custom CNN model."""
    print("Training custom CNN model...")
    
    # Callbacks
    model_checkpoint = ModelCheckpoint(
        os.path.join(MODEL_DIR, 'best_custom_model.keras'),
        monitor='val_loss',
        save_best_only=True,
        mode='min',
        verbose=1
    )
    
    early_stopping = EarlyStopping(
        monitor='val_loss',
        patience=5,
        verbose=1,
        restore_best_weights=True
    )
    
    # Train model
    history = model.fit(
        train_generator,
        epochs=EPOCHS,
        validation_data=validation_generator,
        callbacks=[model_checkpoint, early_stopping],
        verbose=1
    )
    
    # Save final model
    model.save(os.path.join(MODEL_DIR, 'final_custom_model.keras'))
    
    return history

def create_transfer_learning_model(input_shape, num_classes):
    """Create a transfer learning model using MobileNetV2."""
    print("Creating transfer learning model...")
    
    # Load pre-trained MobileNetV2 base model
    base_model = MobileNetV2(
        weights='imagenet',
        include_top=False,
        input_shape=input_shape
    )
    
    # Freeze the base model
    base_model.trainable = False
    
    # Create a new model on top
    inputs = Input(shape=input_shape)
    x = base_model(inputs, training=False)
    x = GlobalAveragePooling2D()(x)
    x = Dense(512, activation='relu')(x)
    x = Dropout(0.5)(x)
    x = BatchNormalization()(x)
    x = Dense(256, activation='relu')(x)
    x = Dropout(0.3)(x)
    outputs = Dense(num_classes, activation='softmax')(x)
    
    model = Model(inputs, outputs)
    
    # Compile model
    model.compile(
        optimizer=Adam(learning_rate=0.001),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model, base_model

def train_transfer_learning_model(model, base_model, train_generator, validation_generator):
    """Train the transfer learning model in two phases."""
    print("Training transfer learning model...")
    
    # Phase 1: Train only the top layers
    print("Phase 1: Training only the top layers...")
    
    # Callbacks
    model_checkpoint = ModelCheckpoint(
        os.path.join(MODEL_DIR, 'best_transfer_model_phase1.keras'),
        monitor='val_loss',
        save_best_only=True,
        mode='min',
        verbose=1
    )
    
    early_stopping = EarlyStopping(
        monitor='val_loss',
        patience=5,
        verbose=1,
        restore_best_weights=True
    )
    
    # Train model (phase 1)
    history1 = model.fit(
        train_generator,
        epochs=10,
        validation_data=validation_generator,
        callbacks=[model_checkpoint, early_stopping],
        verbose=1
    )
    
    # Phase 2: Fine-tuning - unfreeze some layers of the base model
    print("Phase 2: Fine-tuning...")
    
    # Unfreeze the last 15 layers
    base_model.trainable = True
    for layer in base_model.layers[:-15]:
        layer.trainable = False
    
    # Recompile model with a lower learning rate
    model.compile(
        optimizer=Adam(learning_rate=0.0001),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    # Callbacks for phase 2
    model_checkpoint = ModelCheckpoint(
        os.path.join(MODEL_DIR, 'best_transfer_model_phase2.keras'),
        monitor='val_loss',
        save_best_only=True,
        mode='min',
        verbose=1
    )
    
    # Train model (phase 2)
    history2 = model.fit(
        train_generator,
        epochs=10,
        validation_data=validation_generator,
        callbacks=[model_checkpoint, early_stopping],
        verbose=1
    )
    
    # Save final model
    model.save(os.path.join(MODEL_DIR, 'final_transfer_model.keras'))
    
    # Combine histories
    history = {}
    for k in history1.history.keys():
        history[k] = history1.history[k] + history2.history[k]
    
    return history

def evaluate_model(model, test_generator, model_name="model"):
    """Evaluate model and display metrics."""
    print(f"Evaluating {model_name}...")
    
    # Get predictions
    predictions = model.predict(test_generator)
    y_pred = np.argmax(predictions, axis=1)
    
    # Get true labels
    y_true = test_generator.classes
    
    # Calculate metrics
    report = classification_report(
        y_true, 
        y_pred, 
        target_names=list(test_generator.class_indices.keys()),
        output_dict=True
    )
    
    # Print metrics summary
    print(f"\n{model_name} Evaluation Results:")
    print("Classification Report:")
    for cls in report:
        if cls not in ('accuracy', 'macro avg', 'weighted avg'):
            print(f"Class {cls}: Precision={report[cls]['precision']:.4f}, Recall={report[cls]['recall']:.4f}, F1-Score={report[cls]['f1-score']:.4f}")
    
    print(f"Accuracy: {report['accuracy']:.4f}")
    print(f"Macro Avg F1-Score: {report['macro avg']['f1-score']:.4f}")
    
    # Plot confusion matrix
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=list(test_generator.class_indices.keys()),
                yticklabels=list(test_generator.class_indices.keys()))
    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.title(f'Confusion Matrix - {model_name}')
    plt.savefig(os.path.join(os.path.dirname(os.path.abspath(__file__)), f'{model_name}_confusion_matrix.png'))
    plt.close()
    
    # Visualize some predictions
    visualize_predictions(model, test_generator, model_name)
    
    return report

def visualize_predictions(model, test_generator, model_name):
    """Visualize model predictions on sample test images."""
    # Reset generator to start
    test_generator.reset()
    
    # Get a batch of test images
    x_batch, y_batch = next(test_generator)
    
    # Make predictions
    preds = model.predict(x_batch)
    
    # Plot images with predictions
    plt.figure(figsize=(16, 12))
    class_names = list(test_generator.class_indices.keys())
    
    for i in range(min(12, len(x_batch))):
        plt.subplot(3, 4, i+1)
        plt.imshow(x_batch[i])
        true_class_idx = np.argmax(y_batch[i])
        pred_class_idx = np.argmax(preds[i])
        
        true_class = class_names[true_class_idx]
        pred_class = class_names[pred_class_idx]
        confidence = preds[i][pred_class_idx]
        
        color = 'green' if true_class_idx == pred_class_idx else 'red'
        plt.title(f"True: {true_class}\nPred: {pred_class}\nConf: {confidence:.2f}", 
                  color=color)
        plt.axis('off')
    
    plt.suptitle(f'{model_name} - Predictions', fontsize=16)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(os.path.join(os.path.dirname(os.path.abspath(__file__)), f'{model_name}_predictions.png'))
    plt.close()

def plot_training_history(history, model_name="model"):
    """Plot training history for accuracy and loss."""
    # Accuracy plot
    plt.figure(figsize=(12, 5))
    
    plt.subplot(1, 2, 1)
    plt.plot(history['accuracy'], label='Training Accuracy')
    plt.plot(history['val_accuracy'], label='Validation Accuracy')
    plt.title(f'{model_name} - Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.grid(True)
    
    # Loss plot
    plt.subplot(1, 2, 2)
    plt.plot(history['loss'], label='Training Loss')
    plt.plot(history['val_loss'], label='Validation Loss')
    plt.title(f'{model_name} - Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig(os.path.join(os.path.dirname(os.path.abspath(__file__)), f'{model_name}_history.png'))
    plt.close()

def compare_models(custom_results, transfer_results):
    """Compare performance of custom and transfer learning models."""
    print("Comparing models...")
    
    models = ['Custom CNN', 'Transfer Learning']
    accuracy = [custom_results['accuracy'], transfer_results['accuracy']]
    f1_score = [custom_results['macro avg']['f1-score'], transfer_results['macro avg']['f1-score']]
    
    plt.figure(figsize=(10, 6))
    
    x = np.arange(len(models))
    width = 0.35
    
    plt.bar(x - width/2, accuracy, width, label='Accuracy')
    plt.bar(x + width/2, f1_score, width, label='Macro F1-Score')
    
    plt.xlabel('Model')
    plt.ylabel('Score')
    plt.title('Model Comparison')
    plt.xticks(x, models)
    plt.ylim(0, 1)
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    for i, v in enumerate(accuracy):
        plt.text(i - width/2, v + 0.02, f'{v:.4f}', ha='center')
    
    for i, v in enumerate(f1_score):
        plt.text(i + width/2, v + 0.02, f'{v:.4f}', ha='center')
    
    plt.tight_layout()
    plt.savefig(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'model_comparison.png'))
    plt.close()
    
    # Print comparison results
    print("\n--- Model Comparison ---")
    print(f"Custom CNN Accuracy: {accuracy[0]:.4f}, F1-Score: {f1_score[0]:.4f}")
    print(f"Transfer Learning Accuracy: {accuracy[1]:.4f}, F1-Score: {f1_score[1]:.4f}")
    
    if accuracy[1] > accuracy[0]:
        print("Transfer Learning model performed better on accuracy.")
    elif accuracy[0] > accuracy[1]:
        print("Custom CNN model performed better on accuracy.")
    else:
        print("Both models had the same accuracy.")
    
    if f1_score[1] > f1_score[0]:
        print("Transfer Learning model performed better on F1-Score.")
    elif f1_score[0] > f1_score[1]:
        print("Custom CNN model performed better on F1-Score.")
    else:
        print("Both models had the same F1-Score.")

def main():
    """Main function to run the entire pipeline."""
    print("Starting the CNN lab workflow...")
    
    # Download and prepare dataset
    extracted_dir, labels_path = download_and_extract_dataset()
    dataset_dir = prepare_dataset(extracted_dir, labels_path)
    train_dir, val_dir, test_dir = split_dataset(dataset_dir)
    
    # Create data generators
    train_generator, validation_generator, test_generator = create_data_generators(train_dir, val_dir, test_dir)
    
    # Get the number of classes from the generator
    num_classes = len(train_generator.class_indices)
    input_shape = (IMG_SIZE, IMG_SIZE, 3)
    
    # Part 1: Custom CNN
    custom_model = create_custom_cnn_model(input_shape, num_classes)
    print(custom_model.summary())
    custom_history = train_custom_model(custom_model, train_generator, validation_generator)
    plot_training_history(custom_history.history, "Custom CNN")
    custom_results = evaluate_model(custom_model, test_generator, "Custom CNN")
    
    # Part 2: Transfer Learning
    transfer_model, base_model = create_transfer_learning_model(input_shape, num_classes)
    print(transfer_model.summary())
    transfer_history = train_transfer_learning_model(transfer_model, base_model, train_generator, validation_generator)
    plot_training_history(transfer_history, "Transfer Learning")
    transfer_results = evaluate_model(transfer_model, test_generator, "Transfer Learning")
    
    # Compare models
    compare_models(custom_results, transfer_results)
    
    print("CNN lab workflow completed successfully.")

if __name__ == "__main__":
    main()
