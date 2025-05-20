# CNN Development and Training

This repository contains the implementation of Lab Work 3, focusing on developing and training Convolutional Neural Networks (CNNs) for image classification. The project uses a modular structure to build, train, and evaluate a custom CNN and a transfer learning model (MobileNetV2) on a subset of the Oxford 102 Flowers dataset.

## Project Structure

The code is organized into several Python modules for clarity and reusability:

- `config.py`: Contains shared configuration parameters like image dimensions, batch size, dataset URLs, number of classes, and directory paths. Initializes random seeds for reproducibility.
- `data_utils.py`: Includes functions for downloading the Oxford 102 Flowers dataset, extracting images and labels, selecting top N classes, splitting data into training/validation/test sets, and creating augmented data generators.
- `model_utils.py`: Defines the architectures for both the custom CNN model and the transfer learning model (using MobileNetV2 as a base).
- `training_utils.py`: Provides functions for compiling and training the models, including setting up callbacks like `ModelCheckpoint` and `EarlyStopping`, and plotting training history (accuracy and loss curves).
- `evaluation_utils.py`: Contains functions for evaluating the trained models on the test set, generating and plotting confusion matrices, calculating classification reports (precision, recall, F1-score), and visualizing sample predictions.
- `prepare_data.py`: A standalone script that utilizes `data_utils.py` to download, process, and split the dataset. This can be run once to set up the data.
- `train_models.py`: The main script to train both the custom CNN and the transfer learning model. It uses functions from `model_utils.py`, `training_utils.py`, and `evaluation_utils.py`.
- `inference.py`: A script to load a trained model and perform inference on new, unseen images. It demonstrates how to use the saved models.
- `models/`: Directory where trained Keras models (`.keras` files) are saved.
- `dataset/`: Directory where the Oxford 102 Flowers dataset is downloaded, extracted, and organized into `train`, `validation`, and `test` subdirectories. It also stores `class_indices.json`.
- `results/`: Directory for saving output visualizations like training history plots, confusion matrices, and sample prediction images.
- `task.md`: Detailed description of the lab work requirements.
- `report.md`: The detailed report summarizing the methodology, results, and conclusions of the lab.

## File Descriptions
The roles of `config.py`, `data_utils.py`, `model_utils.py`, `training_utils.py`, `evaluation_utils.py`, `prepare_data.py`, `train_models.py`, and `inference.py` are detailed in the "Project Structure" section.

## Detailed Running Instructions

### Setup Environment

1.  **Clone this repository:**
    ```bash
    git clone https://github.com/your-username/your-repo-name.git # Replace with your actual repo URL
    cd your-repo-name # Or your project directory name
    ```

2.  **Create and activate a Python 3.11 virtual environment:**
    ```bash
    python3.11 -m venv venv_py311
    source venv_py311/bin/activate
    ```

3.  **Install required packages:**
    ```bash
    pip install --upgrade pip
    pip install tensorflow numpy matplotlib scikit-learn scipy seaborn requests
    ```

### Modular Pipeline (Recommended)

#### Step 1: Configure Parameters (Optional)
Review and modify parameters in `config.py` if needed (e.g., `NUM_CLASSES`, `IMAGE_SIZE`, `BATCH_SIZE`).

#### Step 2: Prepare Data
This script downloads the dataset, selects the top N classes, splits the data, and organizes it into `train`, `validation`, and `test` directories. Run this once.
```bash
python prepare_data.py
```

#### Step 3: Train Models
This script trains both the custom CNN and the transfer learning model. It saves the best models and generates evaluation plots. This is computationally intensive and benefits from a GPU.
```bash
python train_models.py
```
You can monitor GPU usage with `nvidia-smi -l 1`.

#### Step 4: Run Inference (Optional)
After training, use this script to make predictions on new images.
```bash
# For the custom CNN model:
python inference.py --model_type custom --model_path models/best_custom_model.keras --image_path path/to/your/flower_image.jpg

# For the transfer learning model:
python inference.py --model_type transfer --model_path models/best_transfer_model_phase2.keras --image_path path/to/your/flower_image.jpg
```

### Workflow for Different Machines
(This section remains largely the same as in the original, ensure paths in `scp` commands are correct if used)

#### On a Powerful Machine (for training):
1.  Prepare the data: `python prepare_data.py`
2.  Train the models: `python train_models.py`
3.  Copy the `models/` directory and `dataset/class_indices.json` to your inference machine.

#### On a Less Powerful Machine (for inference):
1.  Ensure you have the trained models and `class_indices.json`.
2.  Run inference: `python inference.py --model_type transfer --model_path models/best_transfer_model_phase2.keras --image_path path/to/your/flower_image.jpg`


### Expected Output

After running `prepare_data.py` and `train_models.py`, you will find:

- **Dataset**: Organized in `dataset/` with `train`, `validation`, `test` folders, and `class_indices.json`.
- **Trained Models** (in `models/` directory):
    - `best_custom_model.keras`
    - `final_custom_model.keras`
    - `best_transfer_model_phase1.keras`
    - `best_transfer_model_phase2.keras` (best fine-tuned model)
    - `final_transfer_model_phase2.keras`
- **Results & Visualizations** (in `results/` directory):
    - `dataset_sample_images.png` (if generated by `prepare_data.py`)
    - `augmented_images.png` (visualization of augmented training images)
    - `Custom CNN_training_history.png` (accuracy and loss curves)
    - `Transfer Learning_training_history.png` (accuracy and loss curves for both phases)
    - `Custom CNN_confusion_matrix.png`
    - `Transfer Learning_confusion_matrix.png`
    - `Custom CNN_sample_predictions.png`
    - `Transfer Learning_sample_predictions.png`
    - `model_performance_comparison.png` (bar chart comparing model metrics)

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
