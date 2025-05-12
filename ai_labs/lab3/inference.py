import os
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import argparse
from config import *
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix
import json

def load_and_preprocess_image(img_path, target_size=(IMG_SIZE, IMG_SIZE)):
    """Load and preprocess an image for inference."""
    img = image.load_img(img_path, target_size=target_size)
    img_array = image.img_to_array(img)
    img_array = img_array / 255.0  # Normalize to [0,1]
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    return img, img_array

def predict_image(model, img_path, class_indices):
    """Make a prediction for an image."""
    # Load and preprocess the image
    original_img, processed_img = load_and_preprocess_image(img_path)
    
    # Make prediction
    predictions = model.predict(processed_img)
    predicted_class_idx = np.argmax(predictions[0])
    confidence = predictions[0][predicted_class_idx]
    
    # Get class name from index
    class_names = {v: k for k, v in class_indices.items()}
    predicted_class = class_names[predicted_class_idx]
    
    return original_img, predicted_class, confidence, predictions[0]

def evaluate_model(model, test_generator, model_name="model"):
    """Evaluate model on the test dataset and return metrics."""
    print(f"Evaluating {model_name}...")
    
    # Get predictions
    predictions = model.predict(test_generator, verbose=1)
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
    plt.savefig(os.path.join(RESULTS_DIR, f'{model_name}_confusion_matrix.png'))
    plt.close()
    
    return report

def compare_models(custom_results, transfer_results):
    """Compare performance of custom and transfer learning models."""
    print("\nComparing models...")
    
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
    plt.savefig(os.path.join(RESULTS_DIR, 'model_comparison.png'))
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

def get_test_generator():
    """Create a test data generator."""
    test_dir = os.path.join(BASE_DIR, "test")
    if not os.path.exists(test_dir):
        print(f"Error: Test directory not found at {test_dir}")
        return None

    # Create test data generator
    from tensorflow.keras.preprocessing.image import ImageDataGenerator
    test_datagen = ImageDataGenerator(rescale=1./255)
    
    test_generator = test_datagen.flow_from_directory(
        test_dir,
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        shuffle=False
    )
    
    return test_generator

def visualize_sample_predictions(custom_model, transfer_model, test_generator):
    """Visualize sample predictions from both models."""
    # Reset generator to start
    test_generator.reset()
    
    # Get a batch of test images
    x_batch, y_batch = next(test_generator)
    
    # Make predictions
    custom_preds = custom_model.predict(x_batch)
    transfer_preds = transfer_model.predict(x_batch)
    
    # Plot images with predictions
    plt.figure(figsize=(15, 10))
    class_names = list(test_generator.class_indices.keys())
    
    # Display 6 images
    for i in range(min(6, len(x_batch))):
        plt.subplot(2, 3, i+1)
        plt.imshow(x_batch[i])
        
        true_class_idx = np.argmax(y_batch[i])
        custom_pred_idx = np.argmax(custom_preds[i])
        transfer_pred_idx = np.argmax(transfer_preds[i])
        
        true_class = class_names[true_class_idx]
        custom_pred = class_names[custom_pred_idx]
        transfer_pred = class_names[transfer_pred_idx]
        
        custom_conf = custom_preds[i][custom_pred_idx]
        transfer_conf = transfer_preds[i][transfer_pred_idx]
        
        # Set title colors based on correctness
        custom_color = 'green' if true_class_idx == custom_pred_idx else 'red'
        transfer_color = 'green' if true_class_idx == transfer_pred_idx else 'red'
        
        plt.title(f"True: {true_class}\n"
                  f"Custom: {custom_pred} ({custom_conf:.2f})\n"
                  f"Transfer: {transfer_pred} ({transfer_conf:.2f})",
                  fontsize=10)
        
        plt.axis('off')
    
    plt.suptitle('Sample Predictions Comparison', fontsize=16)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(os.path.join(RESULTS_DIR, 'sample_predictions_comparison.png'))
    plt.close()
    
    print(f"Sample predictions comparison saved to {os.path.join(RESULTS_DIR, 'sample_predictions_comparison.png')}")

def run_model_comparison():
    """Run evaluation on both models and compare their performance."""
    # Create test generator
    test_generator = get_test_generator()
    if test_generator is None:
        return
    
    # Load models
    custom_model_path = os.path.join(MODEL_DIR, 'best_custom_model.keras')
    transfer_model_path = os.path.join(MODEL_DIR, 'best_transfer_model_phase2.keras')
    
    if not os.path.exists(custom_model_path):
        print(f"Error: Custom model not found at {custom_model_path}")
        return
    
    if not os.path.exists(transfer_model_path):
        print(f"Error: Transfer learning model not found at {transfer_model_path}")
        return
    
    print("Loading models...")
    custom_model = load_model(custom_model_path)
    transfer_model = load_model(transfer_model_path)
    
    # Evaluate models
    custom_results = evaluate_model(custom_model, test_generator, "Custom CNN")
    transfer_results = evaluate_model(transfer_model, test_generator, "Transfer Learning")
    
    # Compare models
    compare_models(custom_results, transfer_results)
    
    # Visualize sample predictions
    visualize_sample_predictions(custom_model, transfer_model, test_generator)
    
    print("\nModel comparison completed successfully.")

def main():
    parser = argparse.ArgumentParser(description='Flower Image Classification Inference')
    parser.add_argument('--model', type=str, choices=['custom', 'transfer'], 
                        help='Model to use for inference: custom or transfer')
    parser.add_argument('--image', type=str, 
                        help='Path to the image file')
    
    args = parser.parse_args()
    
    # Check if we should run model comparison (no args provided)
    if args.model is None and args.image is None:
        print("Running full model comparison and evaluation...")
        run_model_comparison()
        return
    
    # If only one arg is provided, show error message
    if (args.model is None and args.image is not None) or (args.model is not None and args.image is None):
        print("Error: Both --model and --image arguments must be provided for single-image inference.")
        print("Run without arguments to perform full model evaluation and comparison.")
        return
    
    # Load model for single image inference
    if args.model == 'custom':
        model_path = os.path.join(MODEL_DIR, 'best_custom_model.keras')
        model_name = "Custom CNN"
    else:  # transfer
        model_path = os.path.join(MODEL_DIR, 'best_transfer_model_phase2.keras')
        model_name = "Transfer Learning"
    
    if not os.path.exists(model_path):
        print(f"Error: Model file not found at {model_path}")
        return
    
    print(f"Loading {model_name} model...")
    model = load_model(model_path)
    
    # Load class mapping from a file
    class_mapping_file = os.path.join(BASE_DIR, 'class_indices.json')
    
    if os.path.exists(class_mapping_file):
        with open(class_mapping_file, 'r') as f:
            class_indices = json.load(f)
    else:
        # Fallback to using folder names if mapping file doesn't exist
        print("Warning: Class mapping file not found. Using folder names as fallback.")
        train_dir = os.path.join(BASE_DIR, "train")
        class_indices = {}
        for i, class_name in enumerate(sorted(os.listdir(train_dir))):
            if os.path.isdir(os.path.join(train_dir, class_name)):
                class_indices[class_name] = i
    
    # Make prediction on single image
    try:
        img, predicted_class, confidence, all_probs = predict_image(model, args.image, class_indices)
        
        # Display result
        plt.figure(figsize=(8, 6))
        plt.imshow(img)
        plt.title(f"Prediction: {predicted_class}\nConfidence: {confidence:.2f}")
        plt.axis('off')
        
        # Show top 3 predictions
        top_indices = np.argsort(all_probs)[-3:][::-1]
        class_names = {v: k for k, v in class_indices.items()}
        
        plt.figtext(0.5, 0.01, 
                   f"Top predictions:\n" + 
                   "\n".join([f"{class_names[idx]}: {all_probs[idx]:.2f}" for idx in top_indices]),
                   ha="center", fontsize=12, bbox={"facecolor":"white", "alpha":0.8, "pad":5})
        
        plt.tight_layout()
        
        # Save and show result
        os.makedirs(RESULTS_DIR, exist_ok=True)
        result_path = os.path.join(RESULTS_DIR, f"inference_result_{os.path.basename(args.image)}")
        plt.savefig(result_path)
        print(f"Result saved as {result_path}")
        plt.show()
        
    except Exception as e:
        print(f"Error during inference: {e}")

if __name__ == "__main__":
    main()
