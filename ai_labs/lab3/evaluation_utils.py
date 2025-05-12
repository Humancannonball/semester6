import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix
from config import *

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
    plt.savefig(os.path.join(RESULTS_DIR, f'{model_name}_confusion_matrix.png'))
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
    plt.savefig(os.path.join(RESULTS_DIR, f'{model_name}_predictions.png'))
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
