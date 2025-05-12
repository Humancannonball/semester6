# Lab Work 3: CNN Development and Training Report

## 1. Introduction

This report details the implementation and results of Lab Work 3, focusing on image classification using Convolutional Neural Networks (CNNs). The primary goal was to compare the performance of a custom-built CNN against a model utilizing transfer learning on the Oxford 102 Flowers dataset.

## 2. Dataset and Preparation

*   **Dataset:** Oxford 102 Flowers.
*   **Class Selection:** To manage complexity and ensure sufficient data per class, the top 10 classes with the most images were selected from the original 102 classes. The selected class IDs were: [77, 73, 89, 51, 94, 74, 46, 81, 78, 88].
*   **Download and Organization:** The script automatically downloads the dataset images (`102flowers.tgz`) and labels (`imagelabels.mat`) if they are not present. Images corresponding to the selected top 10 classes are organized into separate folders named `class_<ID>`.
*   **Splitting:** The selected data was split into training (70%), validation (15%), and testing (15%) sets. This split is performed once and reused if the split directories exist.
*   **Image Preprocessing:**
    *   All images were resized to 224x224 pixels.
    *   Pixel values were normalized to the range [0, 1] by dividing by 255.
*   **Data Augmentation (Training Set Only):** To improve model generalization and prevent overfitting, the following augmentations were applied to the training data using `ImageDataGenerator`:
    *   Rotation (up to 20 degrees)
    *   Width and Height Shift (up to 20%)
    *   Shear Intensity (up to 20%)
    *   Zoom (up to 20%)
    *   Horizontal and Vertical Flipping
    *   Brightness Adjustment (range [0.8, 1.2])

## 3. Custom CNN Model

*   **Architecture:** A sequential CNN was designed with the following structure:
    *   Input Shape: (224, 224, 3)
    *   Block 1: Conv2D(32, kernel=3x3, padding='same', activation='relu') -> Conv2D(32, kernel=3x3, padding='same', activation='relu') -> BatchNormalization -> MaxPooling2D(2x2) -> Dropout(0.25)
    *   Block 2: Conv2D(64, kernel=3x3, padding='valid', activation='relu') -> Conv2D(64, kernel=3x3, padding='valid', activation='relu') -> BatchNormalization -> MaxPooling2D(2x2) -> Dropout(0.25)
    *   Block 3: Conv2D(128, kernel=3x3, padding='same', activation='relu') -> Conv2D(128, kernel=3x3, padding='same', activation='relu') -> Conv2D(128, kernel=3x3, padding='same', activation='relu') -> BatchNormalization -> MaxPooling2D(2x2) -> Dropout(0.3)
    *   Flatten Layer
    *   Dense(512, activation='relu') -> BatchNormalization -> Dropout(0.5)
    *   Dense(256, activation='relu') -> Dropout(0.3)
    *   Output Layer: Dense(10, activation='softmax')
*   **Training:**
    *   Optimizer: Adam (learning_rate=0.001)
    *   Loss Function: Categorical Crossentropy
    *   Epochs: 20 (with early stopping)
    *   Batch Size: 32
    *   Callbacks:
        *   `ModelCheckpoint`: Saved the model with the best validation loss (`best_custom_model.keras`).
        *   `EarlyStopping`: Monitored validation loss with a patience of 5 epochs. Restored best weights upon stopping.
*   **Results:**
    *   The best model was achieved at Epoch 16.
    *   Evaluation on Test Set:
        *   Accuracy: 0.6818 (68.18%)
        *   Macro Average F1-Score: 0.6681

## 4. Transfer Learning Model

*   **Base Model:** MobileNetV2 pre-trained on ImageNet was chosen for its balance of efficiency and accuracy.
*   **Architecture:**
    *   Input Shape: (224, 224, 3)
    *   MobileNetV2 base (with `include_top=False`)
    *   GlobalAveragePooling2D layer
    *   Dense(512, activation='relu') -> Dropout(0.5) -> BatchNormalization
    *   Dense(256, activation='relu') -> Dropout(0.3)
    *   Output Layer: Dense(10, activation='softmax')
*   **Training Strategy:** A two-phase approach was used:
    *   **Phase 1 (Feature Extraction):**
        *   The MobileNetV2 base layers were frozen (`base_model.trainable = False`).
        *   Only the newly added classification layers were trained.
        *   Optimizer: Adam (learning_rate=0.001)
        *   Loss Function: Categorical Crossentropy
        *   Epochs: 10 (with early stopping, patience=5)
        *   Callbacks: `ModelCheckpoint` (`best_transfer_model_phase1.keras`), `EarlyStopping`.
        *   Best model achieved at Epoch 10.
    *   **Phase 2 (Fine-Tuning):**
        *   The last 15 layers of the MobileNetV2 base were unfrozen (`base_model.trainable = True`, layers before `-15` kept frozen).
        *   The model was recompiled with a lower learning rate to avoid disrupting learned features.
        *   Optimizer: Adam (learning_rate=0.0001)
        *   Loss Function: Categorical Crossentropy
        *   Epochs: 10 (with early stopping, patience=5)
        *   Callbacks: `ModelCheckpoint` (`best_transfer_model_phase2.keras`), `EarlyStopping`.
        *   Training stopped early at Epoch 6, restoring weights from Epoch 1 (the best epoch in Phase 2).
*   **Results:**
    *   Evaluation on Test Set (using the best model from Phase 2, Epoch 1):
        *   Accuracy: 0.9615 (96.15%)
        *   Macro Average F1-Score: 0.9580

## 5. Model Comparison

| Model               | Test Accuracy | Test Macro F1-Score |
| :------------------ | :------------ | :------------------ |
| Custom CNN          | 0.6818        | 0.6681              |
| Transfer Learning   | 0.9615        | 0.9580              |

The Transfer Learning model significantly outperformed the Custom CNN model on both accuracy and F1-score.

## 6. Conclusion

The experiment demonstrated the effectiveness of transfer learning for image classification tasks, especially when the dataset size for training from scratch might be limited relative to the task complexity. The pre-trained MobileNetV2 model provided a strong feature extraction base, allowing the model to achieve high accuracy (96.15%) with relatively less training compared to the custom CNN (68.18%). The custom CNN, while showing learning progress, likely required more data, further architectural tuning, or longer training to reach comparable performance levels. The use of data augmentation was crucial for both models to improve generalization.

## 7. Environment

*   Python: 3.11
*   Libraries: TensorFlow 2.x, Keras (via TensorFlow), NumPy, Scikit-learn, Matplotlib, Seaborn, Requests, SciPy
*   Hardware: Training was performed utilizing an NVIDIA GeForce RTX 4060 Ti GPU with CUDA and cuDNN, accelerated by XLA compilation where applicable.