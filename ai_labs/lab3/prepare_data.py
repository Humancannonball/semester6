import os
import json
from data_utils import prepare_data
from config import BASE_DIR

def main():
    """Standalone script to just prepare the data."""
    print("Starting data preparation...")
    
    # Prepare data
    train_generator, validation_generator, test_generator = prepare_data()
    
    # Save class indices to a file for later use with inference
    class_indices = train_generator.class_indices
    with open(os.path.join(BASE_DIR, 'class_indices.json'), 'w') as f:
        json.dump(class_indices, f)
    
    print("\nData preparation completed successfully.")
    print(f"Class mapping saved to: {os.path.join(BASE_DIR, 'class_indices.json')}")
    print(f"Classes found: {list(class_indices.keys())}")

if __name__ == "__main__":
    main()
