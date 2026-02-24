"""
Quick Plant Disease Model Training - MobileNetV2
Trains in 5-10 minutes instead of 2 hours using a lighter architecture
"""

import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import pickle

MODEL_CONFIG = {
    "image_size": (224, 224),
    "batch_size": 128,
    "epochs": 10,  # Quick training
    "learning_rate": 0.001,
    "model_type": "MobileNetV2",
    "data_augmentation": True
}

class QuickPlantDiseaseModel:
    def __init__(self, config=None):
        self.config = config or MODEL_CONFIG
        self.model = None
        self.class_indices = None
        self.class_names = None
        
    def build_model(self, num_classes):
        """Build lightweight MobileNetV2 model"""
        print("Building MobileNetV2 model (lightweight)...")
        
        # Load pre-trained MobileNetV2
        base_model = keras.applications.MobileNetV2(
            weights='imagenet',
            include_top=False,
            input_shape=(224, 224, 3)
        )
        
        # Freeze base model
        base_model.trainable = False
        
        # Add lightweight custom layers
        model = models.Sequential([
            base_model,
            layers.GlobalAveragePooling2D(),
            layers.Dense(256, activation='relu'),
            layers.Dropout(0.3),
            layers.Dense(128, activation='relu'),
            layers.Dropout(0.2),
            layers.Dense(num_classes, activation='softmax')
        ])
        
        optimizer = keras.optimizers.Adam(learning_rate=self.config["learning_rate"])
        model.compile(
            optimizer=optimizer,
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        self.model = model
        return model
    
    def save_model(self, model_path='plant_disease_model.h5'):
        """Save trained model"""
        if self.model is None:
            raise ValueError("No model to save. Train a model first.")
        
        self.model.save(model_path)
        
        # Save metadata
        metadata = {
            'class_indices': self.class_indices,
            'class_names': self.class_names,
            'config': self.config
        }
        
        with open(model_path.replace('.h5', '_metadata.pkl'), 'wb') as f:
            pickle.dump(metadata, f)
        
        print(f"✅ Model saved to {model_path}")

def train_quick_model():
    """Train quickly using data generators"""
    data_path = './PlantVillage/PlantVillage'
    
    if not os.path.exists(data_path):
        print(f"❌ Data path not found: {data_path}")
        return
    
    # Get class names
    class_names = sorted([d for d in os.listdir(data_path) 
                         if os.path.isdir(os.path.join(data_path, d))])
    
    print(f"\n📊 Quick Training Setup:")
    print(f"  Classes: {len(class_names)}")
    print(f"  Model: MobileNetV2 (lightweight)")
    print(f"  Epochs: 10 (expected time: 5-10 minutes)")
    
    # Initialize model
    model = QuickPlantDiseaseModel()
    model.class_names = class_names
    model.class_indices = {name: idx for idx, name in enumerate(class_names)}
    
    # Build model
    model.build_model(len(class_names))
    
    # Create data generators
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=15,
        width_shift_range=0.15,
        height_shift_range=0.15,
        zoom_range=0.15,
        horizontal_flip=True,
        validation_split=0.2
    )
    
    val_datagen = ImageDataGenerator(rescale=1./255)
    
    print("\n📂 Loading data with generators...")
    
    # Training generator
    train_generator = train_datagen.flow_from_directory(
        data_path,
        target_size=model.config["image_size"],
        batch_size=model.config["batch_size"],
        class_mode='categorical',
        subset='training',
        shuffle=True
    )
    
    # Validation generator
    val_generator = val_datagen.flow_from_directory(
        data_path,
        target_size=model.config["image_size"],
        batch_size=model.config["batch_size"],
        class_mode='categorical',
        subset='validation'
    )
    
    print(f"  Training samples: {train_generator.samples}")
    print(f"  Validation samples: {val_generator.samples}")
    
    # Callbacks
    callbacks = [
        keras.callbacks.EarlyStopping(
            monitor='val_accuracy',
            patience=2,
            restore_best_weights=True,
            verbose=1
        ),
        keras.callbacks.ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=1,
            min_lr=1e-7,
            verbose=1
        )
    ]
    
    # Train
    print("\n🎯 Starting quick training...\n")
    history = model.model.fit(
        train_generator,
        epochs=model.config["epochs"],
        validation_data=val_generator,
        callbacks=callbacks,
        verbose=1,
        steps_per_epoch=min(len(train_generator), 100)  # Limit steps
    )
    
    # Evaluate
    print("\n" + "="*50)
    print("TRAINING COMPLETE")
    print("="*50)
    val_loss, val_acc = model.model.evaluate(val_generator, verbose=0)
    print(f"✓ Validation Accuracy: {val_acc:.4f} ({val_acc*100:.2f}%)")
    print(f"✓ Validation Loss: {val_loss:.4f}")
    
    # Save model
    print("\n💾 Saving model...")
    model.save_model('../backend/model/plant_disease_model.h5')
    
    return model

if __name__ == '__main__':
    train_quick_model()
