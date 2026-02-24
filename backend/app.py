"""
Plant Disease Detection Backend API
Flask application with disease detection, treatment recommendations, and analytics
"""

import os
import json
import pickle
import numpy as np
from datetime import datetime, timedelta
from functools import wraps
import sys
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
import tensorflow as tf
from tensorflow import keras
import cv2
from PIL import Image
import requests
from io import BytesIO
import sqlite3

# Add ml folder to path for disease_db import
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../ml'))
from disease_db import get_disease_info, get_all_disease_names, get_plant_diseases

# Flask app setup
app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Create directories
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs('database', exist_ok=True)

# Global model variable
model = None
class_names = None
class_indices = None

# ==================== Database Setup ====================

def init_database():
    """Initialize SQLite database for user data"""
    conn = sqlite3.connect('database/plant_app.db')
    c = conn.cursor()
    
    # User images history
    c.execute('''CREATE TABLE IF NOT EXISTS image_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        image_path TEXT,
        detected_disease TEXT,
        confidence REAL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        notes TEXT
    )''')
    
    # Crop care reminders
    c.execute('''CREATE TABLE IF NOT EXISTS reminders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        plant_type TEXT,
        reminder_text TEXT,
        frequency TEXT,
        last_sent DATETIME,
        is_active BOOLEAN DEFAULT 1
    )''')
    
    # Weather alerts
    c.execute('''CREATE TABLE IF NOT EXISTS weather_alerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        location TEXT,
        disease_risk TEXT,
        risk_level REAL,
        weather_conditions TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')
    
    conn.commit()
    conn.close()

# ==================== Model Loading ====================

def load_model_on_startup():
    """Load pre-trained model"""
    global model, class_names, class_indices
    
    model_path = 'model/plant_disease_model.h5'
    metadata_path = 'model/plant_disease_model_metadata.pkl'
    
    if os.path.exists(model_path) and os.path.exists(metadata_path):
        try:
            model = keras.models.load_model(model_path)
            with open(metadata_path, 'rb') as f:
                metadata = pickle.load(f)
            class_names = metadata['class_names']
            class_indices = metadata['class_indices']
            print("✓ Model loaded successfully")
            return True
        except Exception as e:
            print(f"Error loading model: {e}")
            return False
    else:
        print("⚠ Model files not found. Please train the model first.")
        return False

# ==================== Helper Functions ====================

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def crop_to_gray(image_path):
    """Convert image to grayscale for explanation"""
    if isinstance(image_path, str):
        img = cv2.imread(image_path)
    else:
        img = image_path
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def generate_saliency_map(image_path, model_obj=None):
    """
    Generate saliency map for explainability
    Shows which parts of the leaf the model focused on
    """
    try:
        img = keras.preprocessing.image.load_img(image_path, target_size=(224, 224))
        img_array = keras.preprocessing.image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = img_array / 255.0
        
        # Compute gradients
        img_tensor = tf.convert_to_tensor(img_array)
        with tf.GradientTape() as tape:
            tape.watch(img_tensor)
            predictions = model(img_tensor)
        
        gradients = tape.gradient(predictions, img_tensor)
        gradients = tf.reduce_max(tf.abs(gradients), axis=-1)
        saliency_map = gradients.numpy()[0]
        
        return saliency_map
    except Exception as e:
        print(f"Error generating saliency map: {e}")
        return None

def assess_disease_severity(predictions, disease_name, weather_data=None):
    """
    Assess disease severity based on model confidence and weather conditions
    """
    confidence = predictions['confidence']
    
    if confidence > 0.9:
        base_severity = "Severe"
    elif confidence > 0.75:
        base_severity = "Moderate"
    elif confidence > 0.5:
        base_severity = "Mild"
    else:
        base_severity = "Unknown"
    
    # Adjust based on weather if available
    if weather_data:
        risk_level = calculate_disease_risk(disease_name, weather_data)
        if risk_level > 0.7:
            base_severity = "Severe"
        elif risk_level > 0.4:
            base_severity = "Moderate"
    
    return base_severity

def calculate_disease_risk(disease_name, weather_data):
    """
    Calculate risk level based on weather conditions and disease characteristics
    Returns risk level 0-1
    """
    disease_info = get_disease_info(disease_name)
    if not disease_info or 'weather_risk_factors' not in disease_info:
        return 0.5
    
    risk_factors = disease_info['weather_risk_factors']
    total_risk = 0
    weight_sum = 0
    
    if 'humidity' in weather_data and 'high_humidity' in risk_factors:
        if weather_data['humidity'] > 80:
            total_risk += risk_factors['high_humidity']
            weight_sum += 1
    
    if 'temperature' in weather_data:
        temp = weather_data['temperature']
        if 'high_temperature' in risk_factors and temp > 28:
            total_risk += risk_factors['high_temperature']
            weight_sum += 1
        if 'cool_temperature' in risk_factors and temp < 15:
            total_risk += risk_factors['cool_temperature']
            weight_sum += 1
    
    if 'rainfall' in weather_data and weather_data['rainfall'] > 5:
        if 'rainfall' in risk_factors:
            total_risk += risk_factors['rainfall']
            weight_sum += 1
    
    return total_risk / weight_sum if weight_sum > 0 else 0.5

def generate_treatment_recommendations(disease_name, severity):
    """Generate specific treatment recommendations"""
    disease_info = get_disease_info(disease_name)
    if not disease_info:
        return []
    
    treatments = disease_info.get('treatments', [])
    
    # Sort by effectiveness
    sorted_treatments = sorted(treatments, key=lambda x: {'Very High': 3, 'High': 2, 'Medium': 1, 'Low': 0}.get(x.get('effectiveness', 'Medium'), 0), reverse=True)
    
    return sorted_treatments[:3]  # Top 3 treatments

def get_weather_for_location(location):
    """
    Fetch weather data for a location (mock implementation)
    In production, integrate with real weather API like OpenWeatherMap
    """
    try:
        # This is a mock implementation. Replace with actual API call
        return {
            "temperature": 25,
            "humidity": 75,
            "rainfall": 0,
            "wind_speed": 10,
            "location": location
        }
    except Exception as e:
        print(f"Error fetching weather: {e}")
        return None

# ==================== API Endpoints ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/detect', methods=['POST'])
def detect_disease():
    """
    Main disease detection endpoint
    Accepts image upload and returns disease prediction with recommendations
    """
    if model is None:
        return jsonify({'error': 'Model not loaded'}), 503
    
    # Check if file is in request
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not allowed'}), 400
    
    try:
        # Save file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
        filename = timestamp + filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Load and preprocess image
        img = keras.preprocessing.image.load_img(filepath, target_size=(224, 224))
        img_array = keras.preprocessing.image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = img_array / 255.0
        
        # Make prediction
        predictions = model.predict(img_array)
        predicted_class_idx = np.argmax(predictions[0])
        confidence = predictions[0][predicted_class_idx]
        disease_name = class_names[predicted_class_idx]
        
        # Get top 3 predictions
        top_3_indices = np.argsort(predictions[0])[-3:][::-1]
        top_3_predictions = [
            {
                'disease': class_names[idx],
                'confidence': float(predictions[0][idx])
            }
            for idx in top_3_indices
        ]
        
        # Get weather data (optional - can be provided by client)
        location = request.form.get('location', 'default')
        weather_data = get_weather_for_location(location)
        
        # Get disease information
        disease_info = get_disease_info(disease_name)
        
        # Assess severity
        severity = assess_disease_severity(
            {'confidence': float(confidence)},
            disease_name,
            weather_data
        )
        
        # Generate recommendations
        treatments = generate_treatment_recommendations(disease_name, severity)
        
        # Calculate risk level
        risk_level = calculate_disease_risk(disease_name, weather_data) if weather_data else 0.5
        
        # Generate saliency map for explainability
        saliency_map = generate_saliency_map(filepath)
        saliency_path = filepath.replace('.', '_saliency.')
        if saliency_map is not None:
            # Save saliency map
            import matplotlib.pyplot as plt
            plt.imsave(saliency_path, saliency_map, cmap='hot')
        
        response = {
            'detected_disease': disease_name,
            'confidence': float(confidence),
            'severity': severity,
            'risk_level': float(risk_level),
            'top_3_predictions': top_3_predictions,
            'disease_info': {
                'name': disease_info['name'] if disease_info else disease_name,
                'description': disease_info.get('description', '') if disease_info else '',
                'causes': disease_info.get('causes', []) if disease_info else [],
                'prevention': disease_info.get('prevention', []) if disease_info else []
            },
            'treatments': treatments,
            'weather_conditions': weather_data,
            'image_path': filepath,
            'saliency_map_path': saliency_path if saliency_map is not None else None,
            'timestamp': datetime.now().isoformat()
        }
        
        # Save to history
        user_id = request.form.get('user_id', 'anonymous')
        save_to_history(user_id, filepath, disease_name, float(confidence))
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/disease/<disease_name>', methods=['GET'])
def get_disease_details(disease_name):
    """Get detailed information about a disease"""
    disease_info = get_disease_info(disease_name)
    
    if not disease_info:
        return jsonify({'error': 'Disease not found'}), 404
    
    return jsonify(disease_info), 200

@app.route('/api/diseases', methods=['GET'])
def get_all_diseases():
    """Get list of all detectable diseases"""
    diseases = get_all_disease_names()
    return jsonify({'diseases': diseases}), 200

@app.route('/api/diseases/by-plant/<plant_name>', methods=['GET'])
def get_diseases_by_plant(plant_name):
    """Get all diseases for a specific plant"""
    diseases = get_plant_diseases(plant_name)
    return jsonify(diseases), 200

@app.route('/api/history/<user_id>', methods=['GET'])
def get_user_history(user_id):
    """Get detection history for a user"""
    try:
        conn = sqlite3.connect('database/plant_app.db')
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        
        c.execute('''SELECT * FROM image_history 
                    WHERE user_id = ? 
                    ORDER BY timestamp DESC 
                    LIMIT 50''', (user_id,))
        
        rows = c.fetchall()
        conn.close()
        
        history = [dict(row) for row in rows]
        return jsonify({'history': history}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/weather-risk', methods=['POST'])
def calculate_weather_risk():
    """Calculate disease risk based on weather conditions"""
    try:
        data = request.json
        disease_name = data.get('disease_name')
        weather_data = data.get('weather_data')
        
        if not disease_name or not weather_data:
            return jsonify({'error': 'Missing parameters'}), 400
        
        risk_level = calculate_disease_risk(disease_name, weather_data)
        
        return jsonify({
            'disease': disease_name,
            'risk_level': float(risk_level),
            'risk_category': 'High' if risk_level > 0.7 else 'Medium' if risk_level > 0.4 else 'Low'
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/reminders/<user_id>', methods=['GET'])
def get_reminders(user_id):
    """Get crop care reminders for user"""
    try:
        conn = sqlite3.connect('database/plant_app.db')
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        
        c.execute('SELECT * FROM reminders WHERE user_id = ? AND is_active = 1', (user_id,))
        rows = c.fetchall()
        conn.close()
        
        reminders = [dict(row) for row in rows]
        return jsonify({'reminders': reminders}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/reminders', methods=['POST'])
def add_reminder():
    """Add a crop care reminder"""
    try:
        data = request.json
        user_id = data.get('user_id')
        plant_type = data.get('plant_type')
        reminder_text = data.get('reminder_text')
        frequency = data.get('frequency', 'weekly')
        
        conn = sqlite3.connect('database/plant_app.db')
        c = conn.cursor()
        c.execute('''INSERT INTO reminders (user_id, plant_type, reminder_text, frequency)
                    VALUES (?, ?, ?, ?)''',
                 (user_id, plant_type, reminder_text, frequency))
        conn.commit()
        conn.close()
        
        return jsonify({'message': 'Reminder added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/image/<filename>', methods=['GET'])
def get_image(filename):
    """Serve image from uploads"""
    try:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(filename))
        if os.path.exists(filepath):
            return send_file(filepath, mimetype='image/jpeg')
        return jsonify({'error': 'Image not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/offline-model', methods=['GET'])
def download_offline_model():
    """Download model for offline use"""
    try:
        model_path = 'model/plant_disease_model.h5'
        if os.path.exists(model_path):
            return send_file(model_path, as_attachment=True, download_name='plant_disease_model.h5')
        return jsonify({'error': 'Model not available'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats/<user_id>', methods=['GET'])
def get_user_stats(user_id):
    """Get user statistics"""
    try:
        conn = sqlite3.connect('database/plant_app.db')
        c = conn.cursor()
        
        # Total detections
        c.execute('SELECT COUNT(*) FROM image_history WHERE user_id = ?', (user_id,))
        total_detections = c.fetchone()[0]
        
        # Disease breakdown
        c.execute('''SELECT detected_disease, COUNT(*) as count 
                    FROM image_history 
                    WHERE user_id = ? 
                    GROUP BY detected_disease''', (user_id,))
        disease_breakdown = dict(c.fetchall())
        
        # Recent detections
        c.execute('''SELECT detected_disease, COUNT(*) as count 
                    FROM image_history 
                    WHERE user_id = ? AND timestamp > datetime('now', '-7 days')
                    GROUP BY detected_disease''', (user_id,))
        recent_detections = dict(c.fetchall())
        
        conn.close()
        
        return jsonify({
            'user_id': user_id,
            'total_detections': total_detections,
            'disease_breakdown': disease_breakdown,
            'recent_detections_7_days': recent_detections
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== Helper Functions ====================

def save_to_history(user_id, image_path, disease_name, confidence):
    """Save detection to history"""
    try:
        conn = sqlite3.connect('database/plant_app.db')
        c = conn.cursor()
        c.execute('''INSERT INTO image_history (user_id, image_path, detected_disease, confidence)
                    VALUES (?, ?, ?, ?)''',
                 (user_id, image_path, disease_name, confidence))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error saving to history: {e}")

# ==================== Startup ====================

if __name__ == '__main__':
    init_database()
    load_model_on_startup()
    app.run(debug=True, host='0.0.0.0', port=5001)
