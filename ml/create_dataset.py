"""
Create balanced 400-image dataset from PlantVillage
Takes samples from all disease classes for variety
"""

import os
import shutil
import random
from pathlib import Path

def create_balanced_dataset(source_dir, output_dir, total_images=400):
    """Create balanced dataset with samples from all disease classes"""
    
    # Clean output directory if exists
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    
    # Get all disease classes
    disease_folders = [d for d in os.listdir(source_dir) 
                      if os.path.isdir(os.path.join(source_dir, d))]
    
    num_classes = len(disease_folders)
    images_per_class = total_images // num_classes
    
    print(f"\n📊 Creating Balanced Dataset:")
    print(f"  Total images: {total_images}")
    print(f"  Classes: {num_classes}")
    print(f"  Images per class: {images_per_class}")
    print(f"  Train/Test split: 70/30")
    
    # Create dataset structure
    train_dir = os.path.join(output_dir, 'train')
    test_dir = os.path.join(output_dir, 'test')
    
    train_split = 0.7
    
    total_copied = 0
    
    print(f"\n📂 Copying images...\n")
    
    for disease in sorted(disease_folders):
        disease_path = os.path.join(source_dir, disease)
        
        # Get all images for this disease
        image_files = [f for f in os.listdir(disease_path) 
                      if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        
        # Randomly sample images_per_class images
        if len(image_files) > images_per_class:
            sampled_files = random.sample(image_files, images_per_class)
        else:
            sampled_files = image_files
        
        print(f"  {disease}: {len(sampled_files)} images")
        
        # Shuffle and split
        random.shuffle(sampled_files)
        split_idx = int(len(sampled_files) * train_split)
        
        train_files = sampled_files[:split_idx]
        test_files = sampled_files[split_idx:]
        
        # Create class directories
        train_class_dir = os.path.join(train_dir, disease)
        test_class_dir = os.path.join(test_dir, disease)
        os.makedirs(train_class_dir, exist_ok=True)
        os.makedirs(test_class_dir, exist_ok=True)
        
        # Copy train files
        for img_file in train_files:
            src = os.path.join(disease_path, img_file)
            dst = os.path.join(train_class_dir, img_file)
            try:
                shutil.copy2(src, dst)
                total_copied += 1
            except Exception as e:
                print(f"    Error copying {img_file}: {e}")
        
        # Copy test files
        for img_file in test_files:
            src = os.path.join(disease_path, img_file)
            dst = os.path.join(test_class_dir, img_file)
            try:
                shutil.copy2(src, dst)
                total_copied += 1
            except Exception as e:
                print(f"    Error copying {img_file}: {e}")
    
    # Get final counts
    train_count = sum([len(os.listdir(os.path.join(train_dir, d))) 
                      for d in os.listdir(train_dir)])
    test_count = sum([len(os.listdir(os.path.join(test_dir, d))) 
                     for d in os.listdir(test_dir)])
    
    print(f"\n✅ Dataset created successfully!")
    print(f"  Total images copied: {total_copied}")
    print(f"  Training images: {train_count}")
    print(f"  Test images: {test_count}")
    print(f"  Train/Test ratio: {train_count}/{test_count} ({train_count/(train_count+test_count)*100:.1f}% train)")

if __name__ == '__main__':
    source = './PlantVillage/PlantVillage'
    output = './balanced_dataset_400'
    
    if not os.path.exists(source):
        print(f"❌ Source directory not found: {source}")
    else:
        create_balanced_dataset(source, output, total_images=400)
