"""
Crop care recommendations based on plant type and season
"""

CROP_CARE_GUIDE = {
    "Tomato": {
        "watering": {
            "frequency": "Daily in hot seasons, every 2-3 days in cool seasons",
            "amount": "1-2 inches per week",
            "best_time": "Early morning",
            "method": "Drip irrigation preferred"
        },
        "fertilization": {
            "frequency": "Every 2-3 weeks",
            "npk_ratio": "5-20-20 or balanced 10-10-10",
            "amount": "1-2 tablespoons per plant"
        },
        "pruning": {
            "frequency": "Weekly",
            "tips": [
                "Remove suckers for determinate varieties",
                "Prune lower leaves for air circulation",
                "Remove diseased leaves immediately"
            ]
        },
        "support": {
            "type": "Stakes or cages",
            "timing": "Install at planting",
            "height": "4-6 feet"
        }
    },
    "Potato": {
        "watering": {
            "frequency": "2-3 times per week during growing season",
            "amount": "1-2 inches per week",
            "best_time": "Early morning or evening",
            "method": "Drip irrigation or soaker hose"
        },
        "fertilization": {
            "frequency": "At planting and 4 weeks later",
            "npk_ratio": "5-10-10",
            "amount": "Apply at side dressing"
        },
        "hilling": {
            "frequency": "2-3 times during growing season",
            "timing": "When plants are 6-8 inches tall",
            "tips": ["Protect developing tubers from sunlight"]
        },
        "harvest": {
            "timing": "70-90 days after planting",
            "method": "Dig carefully to avoid bruising",
            "storage": "Cool, dark place at 45-50°F"
        }
    },
    "Pepper": {
        "watering": {
            "frequency": "Daily in hot seasons",
            "amount": "1-2 inches per week",
            "best_time": "Early morning",
            "method": "Drip irrigation"
        },
        "fertilization": {
            "frequency": "Every 3-4 weeks",
            "npk_ratio": "5-10-10",
            "amount": "Follow label instructions"
        },
        "temperature": {
            "optimal_range": "70-85°F",
            "min_temperature": "50°F",
            "high_temperature_impact": "Flower drop above 90°F"
        },
        "spacing": {
            "between_plants": "18-24 inches",
            "between_rows": "24-36 inches"
        }
    }
}

SEASONAL_REMINDERS = {
    "Spring": {
        "month_range": "March-May",
        "tasks": [
            "Prepare soil with organic matter",
            "Start seeds indoors 6-8 weeks before last frost",
            "Transplant seedlings after frost danger passes",
            "Install support structures",
            "Begin pest monitoring"
        ]
    },
    "Summer": {
        "month_range": "June-August",
        "tasks": [
            "Water regularly and deeply",
            "Apply mulch to conserve moisture",
            "Provide afternoon shade in extreme heat",
            "Scout for diseases and pests",
            "Apply preventive fungicides"
        ]
    },
    "Fall": {
        "month_range": "September-November",
        "tasks": [
            "Reduce watering gradually",
            "Monitor for late season diseases",
            "Prepare for frost protection",
            "Harvest mature fruits",
            "Clean up fallen debris"
        ]
    },
    "Winter": {
        "month_range": "December-February",
        "tasks": [
            "Plan next season's crops",
            "Clean and maintain tools",
            "Remove diseased plants",
            "Improve soil in off-season",
            "Review past year's records"
        ]
    }
}

PREVENTIVE_PRACTICES = {
    "general": [
        "Rotate crops yearly",
        "Use disease-resistant varieties",
        "Maintain proper spacing",
        "Avoid overhead watering",
        "Sanitize tools between plants",
        "Remove infected material immediately",
        "Monitor plants regularly",
        "Maintain field cleanliness"
    ],
    "disease_specific": {
        "fungal": [
            "Improve air circulation",
            "Reduce humidity with ventilation",
            "Apply sulfur or copper sprays",
            "Remove infected leaves",
            "Avoid wetting foliage"
        ],
        "bacterial": [
            "Use copper-based fungicides",
            "Practice strict sanitation",
            "Use resistant varieties",
            "Avoid working in wet field",
            "Sterilize pruning tools"
        ],
        "viral": [
            "Control vector insects",
            "Remove infected plants",
            "Use resistant varieties",
            "Avoid handling plants when wet",
            "Clean equipment regularly"
        ],
        "pest": [
            "Scout regularly for pests",
            "Use beneficial insects",
            "Apply neem oil or insecticidal soap",
            "Remove affected leaves",
            "Maintain plant vigor"
        ]
    }
}

def get_crop_care_guide(plant_type):
    """Get care guide for specific plant"""
    return CROP_CARE_GUIDE.get(plant_type, {})

def get_seasonal_tasks(season):
    """Get seasonal reminder tasks"""
    return SEASONAL_REMINDERS.get(season, {})

def get_preventive_practices(disease_type=None):
    """Get preventive practices"""
    if disease_type:
        return PREVENTIVE_PRACTICES.get(disease_type, PREVENTIVE_PRACTICES.get('general', []))
    return PREVENTIVE_PRACTICES.get('general', [])
