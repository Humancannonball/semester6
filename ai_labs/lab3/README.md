# CNN Development and Training

This repository contains the implementation of Lab Work 3 focused on developing and training Convolutional Neural Networks (CNNs) for image classification. The lab includes building a custom CNN from scratch and applying transfer learning with a pre-trained model to classify flower species from the Oxford 102 Flowers dataset.

## Project Structure

The code is organized in a modular structure to allow for training on a powerful machine and inference on a less powerful one:

- `config.py` - Contains shared configuration parameters
- `data_utils.py` - Functions for downloading, preparing, and augmenting data
- `model_utils.py` - Model architecture definitions
- `training_utils.py` - Model training functions
- `evaluation_utils.py` - Model evaluation and visualization functions
- `prepare_data.py` - Standalone script for just preparing the dataset
- `train_models.py` - Script for training and evaluating models
- `inference.py` - Script for performing inference on new images
- `models/` - Directory where trained models are saved
- `dataset/` - Directory where the dataset is downloaded and organized
- `results/` - Directory for saving visualizations and results

## File Descriptions

- **config.py**: Central configuration file that sets global parameters like image size, batch size, number of classes, dataset URLs, and directory paths. Also initializes random seeds for reproducibility.

- **data_utils.py**: Contains all data handling functions including downloading, extracting, preparing, and augmenting the Oxford 102 Flowers dataset. Functions create data generators with appropriate augmentation for training.

- **model_utils.py**: Defines the architectures for both the custom CNN and transfer learning models. The custom CNN has multiple convolutional blocks with different padding strategies, while the transfer learning model uses MobileNetV2 as a base.

- **training_utils.py**: Contains functions for training models, implementing callbacks for early stopping and model checkpointing, and plotting training history.

- **evaluation_utils.py**: Provides functions for evaluating trained models, including confusion matrix generation, sample prediction visualization, and model comparison.

- **prepare_data.py**: Standalone script that just handles data preparation without model training, useful when you want to prepare data once and reuse it.

- **train_models.py**: Main training script that uses functions from other modules to create and train both custom CNN and transfer learning models.

- **inference.py**: Script for running inference on new images using trained models, designed to work on less powerful machines.

- **lab3.py**: Original monolithic script that contains all functionality in one file (for reference).

## Detailed Running Instructions

### Setup Environment

1. Clone this repository and navigate to the project directory:
   ```bash
   git clone https://github.com/yourusername/cnn-development.git
   cd cnn-development
   ```

2. Create and activate a virtual environment:
   ```bash
   python3.11 -m venv venv_py311
   source venv_py311/bin/activate
   ```

3. Install required packages:
   ```bash
   pip install --upgrade pip
   pip install tensorflow numpy matplotlib scikit-learn scipy seaborn requests
   ```

### Option 1: Running the Original Full Script

If you prefer to run everything in one go (not recommended for machines with limited resources):
```bash
python lab3.py
```

### Option 2: Running the Modular Pipeline (Recommended)

#### Step 1: Configure Parameters (Optional)
Review and modify parameters in `config.py` if needed:
```bash
# View the configuration
cat config.py

# Edit if necessary
vim config.py  
```

#### Step 2: Prepare Data
This step downloads and prepares the dataset. Run once to set up your data:
```bash
python prepare_data.py
```
This creates the necessary directory structure, downloads the dataset, and prepares data generators.

#### Step 3: Train Models
This is the most computationally intensive step. Ideally run on a machine with a good GPU:
```bash
python train_models.py
```
The script will:
- Train a custom CNN model from scratch
- Train a transfer learning model using MobileNetV2
- Generate performance visualizations for both models
- Save the best models to the `models/` directory

You can monitor GPU usage while training with:
```bash
nvidia-smi -l 1  # Updates every 1 second
```

#### Step 4: Run Inference
Once models are trained, you can run inference on new images even on a less powerful machine:
```bash
# For the custom CNN model:
python inference.py --model custom --image path/to/flower_image.jpg

# For the transfer learning model (usually better performance):
python inference.py --model transfer --image path/to/flower_image.jpg
```

### Workflow for Different Machines

#### On a Powerful Machine (for training):
1. Prepare the data:
   ```bash
   python prepare_data.py
   ```
2. Train the models:
   ```bash
   python train_models.py
   ```
3. Copy the trained models and class indices to your less powerful machine:
   ```bash
   # Example: Copy using scp or other file transfer method
   scp -r models/ user@weak-pc:/path/to/lab3/
   scp dataset/class_indices.json user@weak-pc:/path/to/lab3/dataset/
   ```

#### On a Less Powerful Machine (for inference):
1. Make sure you have the pre-trained models and class indices file
2. Run inference on new images:
   ```bash
   python inference.py --model transfer --image path/to/your/flower_image.jpg
   ```

### Expected Output

After running the training script, you'll find several output files in the `results/` directory:

- **Dataset Visualization**:
  - `augmented_images.png`: Shows sample images after augmentation

- **Training Metrics**:
  - `Custom CNN_history.png`: Accuracy and loss curves for custom CNN
  - `Transfer Learning_history.png`: Accuracy and loss curves for transfer learning

- **Evaluation Results**:
  - `Custom CNN_confusion_matrix.png`: Confusion matrix for custom CNN
  - `Transfer Learning_confusion_matrix.png`: Confusion matrix for transfer learning
  - `Custom CNN_predictions.png`: Sample predictions from custom CNN
  - `Transfer Learning_predictions.png`: Sample predictions from transfer learning
  - `model_comparison.png`: Comparative bar chart of model performances

- **Trained Models** (in `models/` directory):
  - `best_custom_model.keras`: Best custom CNN model
  - `best_transfer_model_phase1.keras`: Best transfer model after first training phase
  - `best_transfer_model_phase2.keras`: Best transfer model after fine-tuning
  - `final_custom_model.keras`: Custom CNN after full training
  - `final_transfer_model.keras`: Transfer model after full training

## Features

- Download and prepare the Oxford 102 Flowers dataset
- Data preprocessing and augmentation
- Custom CNN architecture development
- Transfer learning with MobileNetV2
- Comprehensive model evaluation and comparison
- Visualization of results (confusion matrices, predictions, training metrics)
- Separate inference functionality for deployment on less powerful machines

## Implementation Choices

### Dataset Selection
- Using the top 10 classes from Oxford 102 Flowers dataset with the most images
- Split into 70% training, 15% validation, and 15% testing sets

### Data Augmentation
- Applied transformations: rotation, shift, zoom, flips, brightness adjustment
- Helps prevent overfitting and improves model generalization

### Custom CNN Architecture
- Multiple convolutional layers with different padding types
- Dropout layers for regularization
- Batch normalization to stabilize and accelerate training
- Multiple dense layers in the classification part

### Transfer Learning Approach
- Using MobileNetV2 as the base model (efficient and accurate)
- Two-phase training:
  1. Training only the new classification head
  2. Fine-tuning the last 15 layers of the base model
- Lower learning rate for fine-tuning to prevent catastrophic forgetting

## Requirements

- Python 3.11 (TensorFlow 2.x often has specific Python version compatibility, 3.11 is a good choice)
- TensorFlow 2.x (includes Keras)
- NumPy
- Matplotlib
- Scikit-learn
- SciPy (for loading `.mat` label file)
- Seaborn (for plotting confusion matrix)
- Requests (for downloading dataset)

## Installation and Setup on Fedora Linux

1. Install Python 3.11 on Fedora (if not already installed):
    ```bash
    sudo dnf install python3.11 python3.11-devel python3.11-pip
    ```

2. Create and activate a virtual environment using Python 3.11:
    ```bash
    # Create a Python 3.11 virtual environment
    python3.11 -m venv venv_py311

    # Activate the virtual environment
    source venv_py311/bin/activate
    ```
    *(Note: Your shell prompt should change to indicate the active environment, e.g., `(venv_py311) ...`)*

3. Install the required dependencies:
    ```bash
    pip install --upgrade pip
    pip install tensorflow numpy matplotlib scikit-learn scipy seaborn requests
    ```

4. Verify TensorFlow installation and GPU detection:
    ```bash
    python -c "import tensorflow as tf; print('TensorFlow Version:', tf.__version__); print('Num GPUs Available: ', len(tf.config.list_physical_devices('GPU')))"
    ```

## GPU Troubleshooting for Fedora

If you have an NVIDIA GPU (like the RTX 4060 Ti) but TensorFlow isn't detecting it (`Num GPUs Available: 0`), follow these steps carefully:

1. **Verify NVIDIA Driver:** Ensure the driver is installed and running.
    ```bash
    nvidia-smi
    ```
    *(You should see details about your GPU, driver version, and CUDA version supported by the driver).*

2. **Verify CUDA Toolkit:** Ensure the CUDA Toolkit is installed (TensorFlow requires a specific version range, check TensorFlow documentation for your TF version). Let's assume CUDA 12.x is needed.
    ```bash
    nvcc --version
    ```
    *(This should output the installed CUDA toolkit version, e.g., 12.8).*

3. **Set Environment Variables:** Make sure TensorFlow can find the CUDA libraries. Add these lines to your `~/.bashrc` (or `~/.zshrc`) file and restart your terminal or run `source ~/.bashrc`.
    ```bash
    # Add these lines to your shell configuration file (e.g., ~/.bashrc)
    export NVIDIA_VISIBLE_DEVICES=all
    export NVIDIA_DRIVER_CAPABILITIES=compute,utility
    export XLA_FLAGS=--xla_gpu_cuda_data_dir=/usr/local/cuda # Optional: Helps XLA find CUDA
    export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda/lib64:/usr/local/cuda/extras/CUPTI/lib64
    export PATH=$PATH:/usr/local/cuda/bin
    ```
    *(Run `source ~/.bashrc` after editing)*

4. **Install cuDNN:** This library is crucial for GPU acceleration in deep learning frameworks. Download the cuDNN archive compatible with your CUDA version (e.g., cuDNN for CUDA 12.x) from the NVIDIA Developer website.

5. **Re-verify GPU Detection:**
    ```bash
    python -c "import tensorflow as tf; print('TensorFlow Version:', tf.__version__); print('Num GPUs Available: ', len(tf.config.list_physical_devices('GPU')))"
    ```
    If successful, you should see `Num GPUs Available: 1` (or more).

## Results

After running the training script, you'll get several output files in the `results/` directory:
- `augmented_images.png`: Visualization of augmented 
2025-04-29 11:10:17.819973: I tensorflow/core/platform/cpu_feature_guard.cc:210] This Tenstraining images
- `Custom CNN_history.png`: Training and validation accuracy/loss curves for the custom model
- `Transfer Learning_history.png`: Training and validation accuracy/loss curves for the transfer learning model
- `Custom CNN_confusion_matrix.png`: Confusion matrix for the custom model
- `Transfer Learning_confusion_matrix.png`: Confusion matrix for the transfer learning model
- `Custom CNN_predictions.png`: Sample predictions from the custom model
- `Transfer Learning_predictions.png`: Sample predictions from the transfer learning model
- `model_comparison.png`: Comparison of both models' performance metrics

The best models will be saved in the `models/` directory.
