"""
Model evaluation and metrics
"""

import numpy as np
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, roc_auc_score
)
import matplotlib.pyplot as plt

class ModelEvaluator:
    """Evaluate model performance"""
    
    def __init__(self):
        self.results = {}
    
    def evaluate(self, y_true, y_pred, y_pred_proba=None, class_names=None):
        """Evaluate model predictions"""
        y_pred_labels = np.argmax(y_pred, axis=1) if len(y_pred.shape) > 1 else y_pred
        y_true_labels = np.argmax(y_true, axis=1) if len(y_true.shape) > 1 else y_true
        
        self.results = {
            'accuracy': accuracy_score(y_true_labels, y_pred_labels),
            'precision': precision_score(y_true_labels, y_pred_labels, average='weighted', zero_division=0),
            'recall': recall_score(y_true_labels, y_pred_labels, average='weighted', zero_division=0),
            'f1': f1_score(y_true_labels, y_pred_labels, average='weighted', zero_division=0),
            'confusion_matrix': confusion_matrix(y_true_labels, y_pred_labels)
        }
        
        if class_names:
            self.results['classification_report'] = classification_report(
                y_true_labels, y_pred_labels, target_names=class_names
            )
        
        return self.results
    
    def print_report(self):
        """Print evaluation report"""
        if not self.results:
            print("No results to report. Run evaluate() first.")
            return
        
        print("=" * 50)
        print("MODEL EVALUATION REPORT")
        print("=" * 50)
        print(f"Accuracy:  {self.results['accuracy']:.4f}")
        print(f"Precision: {self.results['precision']:.4f}")
        print(f"Recall:    {self.results['recall']:.4f}")
        print(f"F1-Score:  {self.results['f1']:.4f}")
        print("=" * 50)
        
        if 'classification_report' in self.results:
            print("\nDetailed Classification Report:")
            print(self.results['classification_report'])

class ConfidenceAnalyzer:
    """Analyze model confidence"""
    
    @staticmethod
    def get_calibration_metrics(y_true, y_pred_proba, n_bins=10):
        """Calculate calibration metrics"""
        predictions = np.max(y_pred_proba, axis=1)
        correct = (np.argmax(y_pred_proba, axis=1) == np.argmax(y_true, axis=1))
        
        reliability_diagram = {}
        bin_edges = np.linspace(0, 1, n_bins + 1)
        
        for i in range(n_bins):
            bin_mask = (predictions >= bin_edges[i]) & (predictions < bin_edges[i + 1])
            if bin_mask.sum() > 0:
                bin_confidence = predictions[bin_mask].mean()
                bin_accuracy = correct[bin_mask].mean()
                reliability_diagram[f"{bin_edges[i]:.1f}-{bin_edges[i+1]:.1f}"] = {
                    'confidence': bin_confidence,
                    'accuracy': bin_accuracy,
                    'count': bin_mask.sum()
                }
        
        return reliability_diagram
