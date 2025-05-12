# AI Labs Collection

This repository contains a collection of lab work focused on various Artificial Intelligence and Machine Learning concepts.

## Labs

*   **[Lab 2: Object Detection with SentiSight.ai](./lab2/README.md)**
    *   Focuses on using the SentiSight.ai API via a Flask web application for object detection in user-uploaded images. See the [Lab 2 Report](./lab2/report.md) for details on setup and performance.
*   **[Lab 3: CNN Development and Training](./lab3/README.md)**
    *   Involves building and training Convolutional Neural Networks (CNNs) using TensorFlow/Keras for image classification, including custom models and transfer learning. See the [Lab 3 README](./lab3/README.md) for setup and execution instructions.

## General Setup Notes

*   Each lab directory may contain its own specific setup instructions (e.g., `requirements.txt`, virtual environment details). Please refer to the README within each lab's folder.
*   A general `.gitignore` file is included at the root level to exclude common Python artifacts, virtual environments, and sensitive data.
```
# CNN Development and Training

This repository contains the implementation of Lab Work 3 focused on developing and training Convolutional Neural Networks (CNNs) for image classification. The lab includes building a custom CNN from scratch and applying transfer learning with a pre-trained model to classify flower species from the Oxford 102 Flowers dataset.

## Project Structure

- `lab3.py` - Main Python script containing all the code needed to download data, prepare it, train models, and evaluate results
- `task.md` - Detailed description of the lab work requirements
- `models/` - Directory where trained models are saved
- `dataset/` - Directory where the dataset is downloaded and organized

## Features

- Download and prepare the Oxford 102 Flowers dataset
- Data preprocessing and augmentation
- Custom CNN architecture development
- Transfer learning with MobileNetV2
- Comprehensive model evaluation and comparison
- Visualization of results (confusion matrices, predictions, training metrics)

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

1. Clone this repository:
    ```bash
    git clone https://github.com/yourusername/cnn-development.git
    cd cnn-development
    ```

2. Install Python 3.11 on Fedora (if not already installed):
    ```bash
    sudo dnf install python3.11 python3.11-devel python3.11-pip
    ```

3. Create and activate a virtual environment using Python 3.11:
    ```bash
    # Create a Python 3.11 virtual environment
    python3.11 -m venv venv_py311

    # Activate the virtual environment
    source venv_py311/bin/activate
    ```
    *(Note: Your shell prompt should change to indicate the active environment, e.g., `(venv_py311) ...`)*

4. Install the required dependencies:
    ```bash
    pip install --upgrade pip
    pip install tensorflow numpy matplotlib scikit-learn scipy seaborn requests
    ```

5. Verify TensorFlow installation and GPU detection:
    ```bash
    python -c "import tensorflow as tf; print('TensorFlow Version:', tf.__version__); print('Num GPUs Available: ', len(tf.config.list_physical_devices('GPU')))"
    ```

### Understanding TensorFlow Output

- **GPU Available:** If the output shows `Num GPUs Available: 1` (or more), TensorFlow is detecting your GPU.
- **GPU Not Available:** If it shows `Num GPUs Available: 0`, TensorFlow will use the CPU. This might be due to missing NVIDIA drivers, CUDA toolkit, or cuDNN library, or incompatible versions. Warnings about CUDA/cuDNN libraries not being found are common in this case.

## Running the Code

To run the full pipeline (download data, train and evaluate models):

```bash
python lab3.py
```

This script will:
1. Download and prepare the Oxford 102 Flowers dataset
2. Create and train a custom CNN model
3. Create and train a transfer learning model using MobileNetV2
4. Evaluate and compare both models
5. Generate visualization files in the project directory

## Fedora-Specific Notes

- Fedora may require additional system packages for TensorFlow:
```bash
sudo dnf install gcc-c++ atlas-devel
```

- For GPU support on Fedora (NVIDIA GPUs only):
```bash
# Check if NVIDIA drivers are already installed
nvidia-smi

# If not installed or need updating, install NVIDIA drivers
sudo dnf install akmod-nvidia

# Add CUDA repository (if not already added)
sudo dnf config-manager --add-repo https://developer.download.nvidia.com/compute/cuda/repos/fedora$(rpm -E %fedora)/x86_64/cuda-fedora$(rpm -E %fedora).repo

# Install CUDA toolkit (correct package names for Fedora)
sudo dnf install cuda

# If you need development files, look for the specific package 
sudo dnf search cuda | grep devel

# Reboot after installation
sudo reboot
```

- After installation, verify your NVIDIA setup:
```bash
# Check if NVIDIA driver is loaded
nvidia-smi

# Check CUDA installation
nvcc --version
```

- TensorFlow GPU troubleshooting:
  - Ensure the LD_LIBRARY_PATH environment variable includes CUDA paths:
    ```bash
    export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda/lib64
    ```
  - Install cuDNN library (required for TensorFlow GPU):
    Download from [NVIDIA Developer website](https://developer.nvidia.com/cudnn) and follow installation instructions
  - If TensorFlow still doesn't detect your GPU, verify compatible versions:
    ```bash
    python -c "import tensorflow as tf; print('TensorFlow version:', tf.__version__); print('CUDA available:', tf.test.is_built_with_cuda()); print('GPU devices:', tf.config.list_physical_devices('GPU'))"
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

4. **Install cuDNN:** This library is crucial for GPU acceleration in deep learning frameworks. Download the cuDNN archive compatible with your CUDA version (e.g., cuDNN for CUDA 12.x) from the NVIDIA Developer website or use wget. The example below uses cuDNN 9.8.0 for CUDA 12.x as previously mentioned in the file. **Verify compatibility with your TensorFlow version.**

    a. Download cuDNN (Example for 9.8.0 for CUDA 12.x):
        ```bash
        # Adjust version/link if needed for compatibility
        wget https://developer.download.nvidia.com/compute/cudnn/redist/cudnn/linux-x86_64/cudnn-linux-x86_64-9.8.0.87_cuda12-archive.tar.xz
        ```

    b. Extract the archive:
        ```bash
        mkdir -p cudnn_extract
        tar -xf cudnn-linux-x86_64-9.8.0.87_cuda12-archive.tar.xz -C cudnn_extract
        ```

    c. Copy cuDNN files to your CUDA Toolkit directories:
        ```bash
        # Use sudo if CUDA is installed in a system location like /usr/local/cuda
        sudo cp cudnn_extract/cudnn-linux-x86_64-9.8.0.87_cuda12-archive/include/cudnn*.h /usr/local/cuda/include/
        sudo cp cudnn_extract/cudnn-linux-x86_64-9.8.0.87_cuda12-archive/lib/libcudnn* /usr/local/cuda/lib64/
        sudo chmod a+r /usr/local/cuda/include/cudnn*.h /usr/local/cuda/lib64/libcudnn*
        ```

    d. Update library cache:
        ```bash
        sudo ldconfig
        ```

    e. Clean up:
        ```bash
        rm cudnn-linux-x86_64-9.8.0.87_cuda12-archive.tar.xz
        rm -rf cudnn_extract
        ```

5. **Re-verify GPU Detection:** Activate your virtual environment (`source venv_py311/bin/activate`) and run the verification command again:
    ```bash
    python -c "import tensorflow as tf; print('TensorFlow Version:', tf.__version__); print('Num GPUs Available: ', len(tf.config.list_physical_devices('GPU')))"
    ```
    If successful, you should see `Num GPUs Available: 1` (or more).

## Results

After running the script, you'll get several output files:
- `augmented_images.png`: Visualization of augmented training images
- `Custom CNN_history.png`: Training and validation accuracy/loss curves for the custom model
- `Transfer Learning_history.png`: Training and validation accuracy/loss curves for the transfer learning model
- `Custom CNN_confusion_matrix.png`: Confusion matrix for the custom model
- `Transfer Learning_confusion_matrix.png`: Confusion matrix for the transfer learning model
- `Custom CNN_predictions.png`: Sample predictions from the custom model
- `Transfer Learning_predictions.png`: Sample predictions from the transfer learning model
- `model_comparison.png`: Comparison of both models' performance metrics

The best models will be saved in the `models/` directory.

## Notes

- The first run will download the dataset (~330MB) and may take some time
- Training may take considerable time depending on your hardware
- If using CPU only, training could be very slow - consider reducing the number of epochs or using a smaller subset of classes
- For Linux users, you can check your GPU status using `nvidia-smi` command
- On CPU-only systems, expected training times:
  - Custom CNN: ~1-2 hours (10 classes, 20 epochs)
  - Transfer Learning: ~2-3 hours (10 classes, 20 epochs)
  - Consider setting environment variable for optimal CPU performance: `export TF_ENABLE_ONEDNN_OPTS=1`
