import os
import matplotlib.pyplot as plt
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping
from tensorflow.keras.optimizers import Adam  # Add this import for the Adam optimizer
from config import *

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
        optimizer=Adam(learning_rate=0.0001),  # Now Adam will be properly recognized
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
    plt.savefig(os.path.join(RESULTS_DIR, f'{model_name}_history.png'))
    plt.close()
