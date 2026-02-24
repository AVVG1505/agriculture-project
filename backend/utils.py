"""
Utility functions for the Plant Disease Detection system
"""

import os
import json
from datetime import datetime, timedelta
import numpy as np
from pathlib import Path

class ConfigManager:
    """Manage application configuration"""
    
    @staticmethod
    def load_config(env_file='.env'):
        """Load environment configuration"""
        config = {}
        if os.path.exists(env_file):
            with open(env_file) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        config[key.strip()] = value.strip()
        return config

    @staticmethod
    def get_config(key, default=None):
        """Get configuration value"""
        return os.getenv(key, default)

class ImageProcessor:
    """Process and validate images"""
    
    ALLOWED_FORMATS = {'png', 'jpg', 'jpeg', 'gif'}
    MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB
    
    @staticmethod
    def validate_image(file):
        """Validate uploaded image"""
        if file is None:
            return False, "No file provided"
        
        # Check file extension
        if '.' not in file.filename:
            return False, "File has no extension"
        
        ext = file.filename.rsplit('.', 1)[1].lower()
        if ext not in ImageProcessor.ALLOWED_FORMATS:
            return False, f"File type {ext} not allowed"
        
        # Check file size
        file.seek(0, os.SEEK_END)
        size = file.tell()
        file.seek(0)
        
        if size > ImageProcessor.MAX_FILE_SIZE:
            return False, f"File too large. Maximum size: {ImageProcessor.MAX_FILE_SIZE / 1024 / 1024}MB"
        
        return True, "Valid"

class RiskAssessment:
    """Assess disease risk based on multiple factors"""
    
    @staticmethod
    def calculate_overall_risk(disease_risk, confidence, severity_score):
        """
        Calculate overall risk score
        disease_risk: 0-1 based on weather
        confidence: 0-1 model confidence
        severity_score: 0-1 based on disease severity
        """
        weights = {
            'disease_risk': 0.4,
            'confidence': 0.35,
            'severity': 0.25
        }
        
        overall = (
            disease_risk * weights['disease_risk'] +
            confidence * weights['confidence'] +
            severity_score * weights['severity']
        )
        
        return min(max(overall, 0), 1)
    
    @staticmethod
    def get_risk_level(score):
        """Convert risk score to risk level"""
        if score > 0.7:
            return "HIGH"
        elif score > 0.4:
            return "MEDIUM"
        else:
            return "LOW"
    
    @staticmethod
    def get_recommendations(risk_level, disease_name):
        """Get recommendations based on risk level"""
        recommendations = {
            'HIGH': [
                f"Immediate action required for {disease_name}",
                "Apply preventive/curative fungicides immediately",
                "Increase monitoring frequency to daily",
                "Consider isolating affected plants",
                "Optimize field conditions (humidity, ventilation)"
            ],
            'MEDIUM': [
                f"Monitor {disease_name} closely",
                "Apply preventive treatments within 3-5 days",
                "Increase monitoring to every 2-3 days",
                "Maintain optimal field conditions",
                "Prepare treatment equipment"
            ],
            'LOW': [
                f"Standard monitoring for {disease_name}",
                "Maintain regular preventive practices",
                "Continue weekly monitoring",
                "Apply preventive treatments if conditions change",
                "Keep field hygiene optimal"
            ]
        }
        
        return recommendations.get(risk_level, recommendations['LOW'])

class DataLogger:
    """Log data for analytics and debugging"""
    
    def __init__(self, log_dir='logs'):
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)
    
    def log_detection(self, user_id, disease_name, confidence, location=None):
        """Log detection event"""
        log_file = os.path.join(self.log_dir, 'detections.log')
        
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'user_id': user_id,
            'disease': disease_name,
            'confidence': confidence,
            'location': location
        }
        
        with open(log_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
    
    def log_error(self, error_type, error_message, context=None):
        """Log error"""
        log_file = os.path.join(self.log_dir, 'errors.log')
        
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'error_type': error_type,
            'message': error_message,
            'context': context
        }
        
        with open(log_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
    
    def get_statistics(self, days=7):
        """Get statistics for last N days"""
        log_file = os.path.join(self.log_dir, 'detections.log')
        
        if not os.path.exists(log_file):
            return {}
        
        cutoff_time = datetime.now() - timedelta(days=days)
        stats = {}
        
        with open(log_file, 'r') as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    entry_time = datetime.fromisoformat(entry['timestamp'])
                    
                    if entry_time > cutoff_time:
                        disease = entry['disease']
                        stats[disease] = stats.get(disease, 0) + 1
                except:
                    pass
        
        return stats

class NotificationHandler:
    """Handle notifications and alerts"""
    
    @staticmethod
    def create_alert(disease_name, risk_level, affected_plants):
        """Create an alert for users"""
        alert = {
            'timestamp': datetime.now().isoformat(),
            'disease': disease_name,
            'risk_level': risk_level,
            'affected_plants': affected_plants,
            'message': f"Alert: {disease_name} detected with {risk_level} risk level"
        }
        return alert
    
    @staticmethod
    def should_notify(last_notification_time, notification_frequency_hours=24):
        """Check if enough time has passed since last notification"""
        if last_notification_time is None:
            return True
        
        time_diff = datetime.now() - last_notification_time
        return time_diff.total_seconds() > (notification_frequency_hours * 3600)

class OfflineModelManager:
    """Manage offline model capabilities"""
    
    @staticmethod
    def export_to_onnx(keras_model, output_path='model.onnx'):
        """Convert Keras model to ONNX for offline use"""
        try:
            # Optional: Install onnx and keras2onnx for this feature
            # pip install onnx keras2onnx
            import onnx
            import keras2onnx
            
            onnx_model = keras2onnx.convert_keras(keras_model)
            onnx.save_model(onnx_model, output_path)
            return True, f"Model exported to {output_path}"
        except ImportError:
            return False, "Install onnx and keras2onnx: pip install onnx keras2onnx"
        except Exception as e:
            return False, str(e)
    
    @staticmethod
    def get_model_size(model_path):
        """Get model file size"""
        if os.path.exists(model_path):
            size_bytes = os.path.getsize(model_path)
            size_mb = size_bytes / (1024 * 1024)
            return size_mb
        return None

class PerformanceMonitor:
    """Monitor system performance"""
    
    def __init__(self):
        self.detection_times = []
        self.error_count = 0
        self.total_requests = 0
    
    def record_detection_time(self, time_seconds):
        """Record detection time"""
        self.detection_times.append(time_seconds)
    
    def record_request(self, success=True):
        """Record request"""
        self.total_requests += 1
        if not success:
            self.error_count += 1
    
    def get_stats(self):
        """Get performance statistics"""
        if not self.detection_times:
            return {}
        
        return {
            'avg_detection_time': np.mean(self.detection_times),
            'min_detection_time': np.min(self.detection_times),
            'max_detection_time': np.max(self.detection_times),
            'total_requests': self.total_requests,
            'error_count': self.error_count,
            'success_rate': (self.total_requests - self.error_count) / self.total_requests
        }
