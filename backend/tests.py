"""
Test suite for plant disease detection system
"""

import unittest
import json
import os
import sys

# Add ml folder to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../ml'))

from disease_db import get_disease_info, get_all_disease_names, get_plant_diseases

class TestDiseaseDatabase(unittest.TestCase):
    """Test disease database functionality"""
    
    def test_get_disease_info(self):
        """Test retrieving disease information"""
        disease = get_disease_info('Tomato_Bacterial_spot')
        self.assertIsNotNone(disease)
        self.assertEqual(disease['plant'], 'Tomato')
        self.assertIn('causes', disease)
        self.assertIn('treatments', disease)
    
    def test_get_all_diseases(self):
        """Test getting all disease names"""
        diseases = get_all_disease_names()
        self.assertGreater(len(diseases), 0)
        self.assertIn('Tomato_Bacterial_spot', diseases)
    
    def test_get_plant_diseases(self):
        """Test getting diseases by plant"""
        tomato_diseases = get_plant_diseases('Tomato')
        self.assertGreater(len(tomato_diseases), 0)
        
        for name, info in tomato_diseases.items():
            self.assertEqual(info['plant'], 'Tomato')
    
    def test_disease_structure(self):
        """Test disease info structure"""
        disease = get_disease_info('Tomato_Late_blight')
        
        required_fields = ['name', 'plant', 'description', 'causes', 
                          'severity_levels', 'treatments', 'prevention']
        
        for field in required_fields:
            self.assertIn(field, disease, f"Missing field: {field}")
    
    def test_treatments_structure(self):
        """Test treatment structure"""
        disease = get_disease_info('Tomato_Early_blight')
        treatments = disease['treatments']
        
        self.assertGreater(len(treatments), 0)
        
        required_treatment_fields = ['name', 'dosage', 'frequency', 'cost', 'effectiveness']
        
        for treatment in treatments:
            for field in required_treatment_fields:
                self.assertIn(field, treatment, f"Missing treatment field: {field}")

class TestRiskAssessment(unittest.TestCase):
    """Test risk assessment functionality"""
    
    def test_risk_calculation(self):
        """Test risk calculation"""
        from utils import RiskAssessment
        
        # Test high risk
        risk = RiskAssessment.calculate_overall_risk(
            disease_risk=0.8,
            confidence=0.9,
            severity_score=0.85
        )
        self.assertGreater(risk, 0.7)
        
        # Test low risk
        risk = RiskAssessment.calculate_overall_risk(
            disease_risk=0.2,
            confidence=0.3,
            severity_score=0.1
        )
        self.assertLess(risk, 0.4)
    
    def test_risk_level_classification(self):
        """Test risk level classification"""
        from utils import RiskAssessment
        
        self.assertEqual(RiskAssessment.get_risk_level(0.8), "HIGH")
        self.assertEqual(RiskAssessment.get_risk_level(0.5), "MEDIUM")
        self.assertEqual(RiskAssessment.get_risk_level(0.2), "LOW")
    
    def test_recommendations_generation(self):
        """Test recommendations generation"""
        from utils import RiskAssessment
        
        high_risk_recs = RiskAssessment.get_recommendations("HIGH", "Tomato_Early_blight")
        self.assertGreater(len(high_risk_recs), 0)
        self.assertIn("Immediate", high_risk_recs[0])

class TestImageProcessor(unittest.TestCase):
    """Test image processing functionality"""
    
    def test_allowed_formats(self):
        """Test allowed image formats"""
        from utils import ImageProcessor
        
        self.assertIn('png', ImageProcessor.ALLOWED_FORMATS)
        self.assertIn('jpg', ImageProcessor.ALLOWED_FORMATS)
        self.assertIn('jpeg', ImageProcessor.ALLOWED_FORMATS)

def run_tests():
    """Run all tests"""
    unittest.main()

if __name__ == '__main__':
    run_tests()
