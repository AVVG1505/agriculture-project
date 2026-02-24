"""
Plant Disease Detection Model Training Pipeline
Fast training on balanced 400-image dataset (70% train, 30% test)
"""

import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import json
import pickle
from pathlib import Path
import ssl

# Fix SSL certificate issue on macOS
ssl._create_default_https_context = ssl._create_unverified_context

# Model configuration - OPTIMIZED FOR SMALL DATASET
MODEL_CONFIG = {
    "image_size": (224, 224),
    "batch_size": 32,
    "epochs": 15,
    "learning_rate": 0.001,
    "model_type": "MobileNetV2",
    "data_augmentation": True
}

class PlantDiseaseModel:
    def __init__(self, config=None):
        self.config = config or MODEL_CONFIG
        self.model = None
        self.class_indices = None
        self.class_names = None
        
    def load_data(self, data_path):
        """
        Load images from organized directory structure using ImageDataGenerator
        Expected structure: data_path/disease_name/*.jpg
        """
        print(f"Loading data from {data_path}...")
        images = []
        labels = []
        class_indices = {}
        class_names = []
        
        disease_folders = sorted([d for d in os.listdir(data_path) 
                                 if os.path.isdir(os.path.join(data_path, d))])
        
        print(f"Found {len(disease_folders)} disease classes")
        
        for idx, disease in enumerate(disease_folders):
            class_indices[disease] = idx
            class_names.append(disease)
            disease_path = os.path.join(data_path, disease)
            
            image_files = [f for f in os.listdir(disease_path) 
                          if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
            
            print(f"  Loading {disease}: {len(image_files)} images...")
            
            for image_file in image_files:
                image_path = os.path.join(disease_path, image_file)
                try:
                    img = keras.preprocessing.image.load_img(
                        image_path, 
                        target_size=self.config["image_size"]
                    )
                    img_array = keras.preprocessing.image.img_to_array(img)
                    img_array = img_array / 255.0  # Normalize to 0-1
                    images.append(img_array)
                    labels.append(idx)
                except Exception as e:
                    pass  # Skip corrupted images silently
        
        self.class_indices = class_indices
        self.class_names = class_names
        
        X = np.array(images, dtype=np.float32)
        y = keras.utils.to_categorical(labels, len(class_names))
        
        print(f"\n✓ Successfully loaded {len(images)} images with {len(class_names)} classes")
        print(f"  Dataset shape: {X.shape}")
        print(f"  Labels shape: {y.shape}")
        return X, y
    
    def build_model(self):
        """Build MobileNetV2 model with transfer learning (lightweight for quick training)"""
        print("Building MobileNetV2 model (lightweight)...")
        
        # Load pre-trained MobileNetV2
        base_model = keras.applications.MobileNetV2(
            weights='imagenet',
            include_top=False,
            input_shape=(224, 224, 3)
        )
        
        # Freeze base model layers
        base_model.trainable = False
        
        # Add custom layers
        model = models.Sequential([
            base_model,
            layers.GlobalAveragePooling2D(),
            layers.Dense(256, activation='relu'),
            layers.BatchNormalization(),
            layers.Dropout(0.4),
            layers.Dense(128, activation='relu'),
            layers.BatchNormalization(),
            layers.Dropout(0.3),
            layers.Dense(len(self.class_names), activation='softmax')
        ])
        
        # Compile model
        optimizer = keras.optimizers.Adam(learning_rate=self.config["learning_rate"])
        model.compile(
            optimizer=optimizer,
            loss='categorical_crossentropy',
            metrics=['accuracy', keras.metrics.TopKCategoricalAccuracy(k=3, name='top_3_accuracy')]
        )
        
        self.model = model
        return model
    
    def train(self, X_train, y_train, X_val, y_val):
        """Train the model with improved callbacks"""
        print("\nStarting training...")
        print(f"Training samples: {X_train.shape[0]}, Validation samples: {X_val.shape[0]}")
        
        # Data augmentation
        if self.config["data_augmentation"]:
            train_datagen = ImageDataGenerator(
                rotation_range=20,
                width_shift_range=0.2,
                height_shift_range=0.2,
                shear_range=0.2,
                zoom_range=0.2,
                horizontal_flip=True,
                fill_mode='nearest'
            )
        
        # Callbacks with better early stopping
        callbacks = [
            keras.callbacks.EarlyStopping(
                monitor='val_accuracy',
                patience=5,
                restore_best_weights=True,
                verbose=1
            ),
            keras.callbacks.ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.5,
                patience=3,
                min_lr=1e-7,
                verbose=1
            ),
            keras.callbacks.ModelCheckpoint(
                'model_checkpoint.h5',
                monitor='val_accuracy',
                save_best_only=True,
                verbose=0
            )
        ]
        
        # Calculate class weights for imbalanced data
        class_counts = np.sum(y_train, axis=0)
        class_weights = len(y_train) / (len(self.class_names) * class_counts)
        class_weights_dict = {i: class_weights[i] for i in range(len(self.class_names))}
        
        # Train
        if self.config["data_augmentation"]:
            history = self.model.fit(
                train_datagen.flow(X_train, y_train, batch_size=self.config["batch_size"]),
                epochs=self.config["epochs"],
                validation_data=(X_val, y_val),
                callbacks=callbacks,
                class_weight=class_weights_dict,
                verbose=1,
                steps_per_epoch=len(X_train) // self.config["batch_size"]
            )
        else:
            history = self.model.fit(
                X_train, y_train,
                batch_size=self.config["batch_size"],
                epochs=self.config["epochs"],
                validation_data=(X_val, y_val),
                callbacks=callbacks,
                class_weight=class_weights_dict,
                verbose=1
            )
        
        return history
    
    def save_model(self, model_path='plant_disease_model.h5'):
        """Save trained model"""
        if self.model is None:
            raise ValueError("No model to save. Train a model first.")
        
        self.model.save(model_path)
        
        # Save class indices
        metadata = {
            'class_indices': self.class_indices,
            'class_names': self.class_names,
            'config': self.config
        }
        
        with open(model_path.replace('.h5', '_metadata.pkl'), 'wb') as f:
            pickle.dump(metadata, f)
        
        print(f"Model saved to {model_path}")
    
    def load_model(self, model_path='plant_disease_model.h5'):
        """Load trained model"""
        self.model = keras.models.load_model(model_path)
        
        # Load metadata
        with open(model_path.replace('.h5', '_metadata.pkl'), 'rb') as f:
            metadata = pickle.load(f)
        
        self.class_indices = metadata['class_indices']
        self.class_names = metadata['class_names']
        self.config = metadata['config']
        
        print(f"Model loaded from {model_path}")
    
    def predict(self, image_path):
        """Predict disease for an image"""
        if self.model is None:
            raise ValueError("No model loaded. Load or train a model first.")
        
        img = keras.preprocessing.image.load_img(
            image_path, 
            target_size=self.config["image_size"]
        )
        img_array = keras.preprocessing.image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = img_array / 255.0
        
        predictions = self.model.predict(img_array)
        predicted_class_idx = np.argmax(predictions[0])
        confidence = predictions[0][predicted_class_idx]
        disease_name = self.class_names[predicted_class_idx]
        
        # Get top 3 predictions
        top_3_indices = np.argsort(predictions[0])[-3:][::-1]
        top_3_predictions = [
            {
                'disease': self.class_names[idx],
                'confidence': float(predictions[0][idx])
            }
            for idx in top_3_indices
        ]
        
        return {
            'predicted_disease': disease_name,
            'confidence': float(confidence),
            'top_3_predictions': top_3_predictions
        }

def train_plant_disease_model():
    """Main training function using small balanced dataset"""
    
    train_dir = './balanced_dataset_400/train'
    test_dir = './balanced_dataset_400/test'
    
    if not os.path.exists(train_dir) or not os.path.exists(test_dir):
        print(f"❌ Dataset directories not found!")
        print(f"   Run 'python create_dataset.py' first to create balanced 400-image dataset")
        return
    
    print(f"\n{'='*60}")
    print("🌱 PLANT DISEASE DETECTION - FAST TRAINING (400 images)")
    print(f"{'='*60}")
    
    # Initialize model
    model = PlantDiseaseModel()
    
    # Get class names from train directory
    model.class_names = sorted(os.listdir(train_dir))
    model.class_indices = {name: idx for idx, name in enumerate(model.class_names)}
    
    print(f"\n📊 Dataset Configuration:")
    print(f"  Classes: {len(model.class_names)}")
    print(f"  Model: MobileNetV2 (lightweight)")
    print(f"  Training: {train_dir}")
    print(f"  Testing: {test_dir}")
    
    # Build model
    model.build_model()
    
    # Create data generators
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
    
    print(f"  ✓ Training samples: {train_samples} ({train_samples/(train_samples+test_samples)*100:.1f}%)")
    print(f"  ✓ Test samples: {test_samples} ({test_samples/(train_samples+test_samples)*100:.1f}%)")
    
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
            verbose=1
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
    
    # Evaluate
    print(f"\n{'='*60}")
    print("📊 EVALUATION RESULTS")
    print(f"{'='*60}")
    test_loss, test_acc, test_top3_acc = model.model.evaluate(test_generator, verbose=0)
    print(f"\n✓ Test Accuracy: {test_acc:.4f} ({test_acc*100:.2f}%)")
    print(f"✓ Test Top-3 Accuracy: {test_top3_acc:.4f}")
    print(f"✓ Test Loss: {test_loss:.4f}")
    
    # Save model
    print(f"\n💾 Saving model to backend/model/plant_disease_model.h5...")
    model.save_model('../backend/model/plant_disease_model.h5')
    
    print(f"\n✅ Training complete!")
    print(f"{'='*60}\n")
    
    return model

if __name__ == '__main__':
    train_plant_disease_model()
