"""
Fast Plant Disease Model Training on 400-image balanced dataset
Uses MobileNetV2 for quick training (5-10 minutes)
"""

import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import pickle
from sklearn.metrics import classification_report, confusion_matrix

MODEL_CONFIG = {
    "image_size": (224, 224),
    "batch_size": 32,
    "epochs": 15,
    "learning_rate": 0.001,
    "model_type": "MobileNetV2"
}

class FastPlantDiseaseModel:
    def __init__(self, config=None):
        self.config = config or MODEL_CONFIG
        self.model = None
        self.class_indices = None
        self.class_names = None
        
    def build_model(self, num_classes):
        """Build lightweight MobileNetV2 model"""
        print("Building MobileNetV2 model...")
        
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
            layers.BatchNormalization(),
            layers.Dropout(0.3),
            layers.Dense(128, activation='relu'),
            layers.Dropout(0.2),
            layers.Dense(num_classes, activation='softmax')
        ])
        
        optimizer = keras.optimizers.Adam(learning_rate=self.config["learning_rate"])
        model.compile(
            optimizer=optimizer,
            loss='categorical_crossentropy',
            metrics=['accuracy', keras.metrics.TopKCategoricalAccuracy(k=3, name='top_3_accuracy')]
        )
        
        print(f"✓ Model built with {num_classes} output classes")
        self.model = model
        return model
    
    def save_model(self, model_path='plant_disease_model.h5'):
        """Save trained model"""
        if self.model is None:
            raise ValueError("No model to save.")
        
        self.model.save(model_path)
        
        metadata = {
            'class_indices': self.class_indices,
            'class_names': self.class_names,
            'config': self.config
        }
        
        with open(model_path.replace('.h5', '_metadata.pkl'), 'wb') as f:
            pickle.dump(metadata, f)
        
        print(f"✅ Model saved to {model_path}")

def train_fast_model():
    """Train on 400-image balanced dataset"""
    
    train_dir = './balanced_dataset_400/train'
    test_dir = './balanced_dataset_400/test'
    
    if not os.path.exists(train_dir) or not os.path.exists(test_dir):
        print(f"❌ Dataset directories not found!")
        print(f"   Run 'python create_dataset.py' first")
        return
    
    print(f"\n{'='*60}")
    print("🌱 PLANT DISEASE DETECTION MODEL - FAST TRAINING")
    print(f"{'='*60}")
    
    # Initialize model
    model = FastPlantDiseaseModel()
    
    # Get class names
    model.class_names = sorted(os.listdir(train_dir))
    model.class_indices = {name: idx for idx, name in enumerate(model.class_names)}
    
    print(f"\n📊 Dataset Configuration:")
    print(f"  Classes: {len(model.class_names)}")
    print(f"  Model: MobileNetV2 (lightweight)")
    print(f"  Image size: 224x224")
    print(f"  Batch size: 32")
    print(f"  Epochs: 15")
    
    # Build model
    model.build_model(len(model.class_names))
    
    # Create data generators with augmentation
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest'
    )
    
    test_datagen = ImageDataGenerator(rescale=1./255)
    
    print(f"\n📂 Loading data generators...")
    
    # Training generator
    train_generator = train_datagen.flow_from_directory(
        train_dir,
        target_size=model.config["image_size"],
        batch_size=model.config["batch_size"],
        class_mode='categorical',
        shuffle=True
    )
    
    # Test generator
    test_generator = test_datagen.flow_from_directory(
        test_dir,
        target_size=model.config["image_size"],
        batch_size=model.config["batch_size"],
        class_mode='categorical',
        shuffle=False
    )
    
    train_samples = train_generator.samples
    test_samples = test_generator.samples
    
    print(f"  ✓ Training samples: {train_samples}")
    print(f"  ✓ Test samples: {test_samples}")
    print(f"  ✓ Train/Test split: {train_samples/(train_samples+test_samples)*100:.1f}% / {test_samples/(train_samples+test_samples)*100:.1f}%")
    
    # Callbacks
    callbacks = [
        keras.callbacks.EarlyStopping(
            monitor='val_accuracy',
            patience=3,
            restore_best_weights=True,
            verbose=1
        ),
        keras.callbacks.ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=2,
            min_lr=1e-7,
            verbose=0
        )
    ]
    
    # Train
    print(f"\n🎯 Starting training...")
    history = model.model.fit(
        train_generator,
        epochs=model.config["epochs"],
        validation_data=test_generator,
        callbacks=callbacks,
        verbose=1
    )
    
    # Evaluate on test set
    print(f"\n{'='*60}")
    print("📊 EVALUATION RESULTS")
    print(f"{'='*60}")
    
    test_loss, test_acc, test_top3_acc = model.model.evaluate(test_generator, verbose=0)
    print(f"\n✓ Test Accuracy: {test_acc:.4f} ({test_acc*100:.2f}%)")
    print(f"✓ Test Top-3 Accuracy: {test_top3_acc:.4f}")
    print(f"✓ Test Loss: {test_loss:.4f}")
    
    # Per-class accuracy
    print(f"\n📋 Per-Class Performance:")
    print("-" * 60)
    
    predictions = model.model.predict(test_generator, verbose=0)
    pred_labels = np.argmax(predictions, axis=1)
    true_labels = test_generator.classes
    
    report = classification_report(
        true_labels, 
        pred_labels,
        target_names=model.class_names,
        digits=3
    )
    print(report)
    
    # Save model
    print(f"\n💾 Saving model...")
    model.save_model('../backend/model/plant_disease_model.h5')
    
    print(f"\n✅ Training complete!")
    print(f"{'='*60}")
    
    return model

if __name__ == '__main__':
    train_fast_model()
