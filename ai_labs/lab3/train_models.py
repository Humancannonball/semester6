import os
import sys
import tensorflow as tf
from config import *
from data_utils import prepare_data
from model_utils import create_custom_cnn_model, create_transfer_learning_model
from training_utils import train_custom_model, train_transfer_learning_model, plot_training_history
from evaluation_utils import evaluate_model, compare_models

def main():
    """Main function to train and evaluate models."""
    print("Starting the CNN lab training workflow...")
    
    # Check for GPU
    gpus = tf.config.list_physical_devices('GPU')
    if gpus:
        print(f"Training on GPU: {gpus}")
        # Set memory growth to avoid allocating all GPU memory
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
    else:
        print("No GPU found. Training on CPU.")
        
    # Prepare data
    train_generator, validation_generator, test_generator = prepare_data()
    
    # Get the number of classes from the generator
    num_classes = len(train_generator.class_indices)
    input_shape = (IMG_SIZE, IMG_SIZE, 3)
    
    # Train custom CNN
    print("\n=== Training Custom CNN Model ===")
    custom_model = create_custom_cnn_model(input_shape, num_classes)
    print(custom_model.summary())
    custom_history = train_custom_model(custom_model, train_generator, validation_generator)
    plot_training_history(custom_history.history, "Custom CNN")
    custom_results = evaluate_model(custom_model, test_generator, "Custom CNN")
    
    # Train transfer learning model
    print("\n=== Training Transfer Learning Model ===")
    transfer_model, base_model = create_transfer_learning_model(input_shape, num_classes)
    print(transfer_model.summary())
    transfer_history = train_transfer_learning_model(transfer_model, base_model, train_generator, validation_generator)
    plot_training_history(transfer_history, "Transfer Learning")
    transfer_results = evaluate_model(transfer_model, test_generator, "Transfer Learning")
    
    # Compare models
    compare_models(custom_results, transfer_results)
    
    print("\nTraining and evaluation completed successfully.")
    print(f"Models saved in: {MODEL_DIR}")
    print(f"Results saved in: {RESULTS_DIR}")

if __name__ == "__main__":
    main()
