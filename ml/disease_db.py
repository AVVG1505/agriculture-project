"""
Disease Database with Treatment Information
Contains disease names, causes, severity levels, treatments, and preventive measures
"""

DISEASE_DATABASE = {
    # Tomato diseases
    "Tomato_Bacterial_spot": {
        "name": "Tomato Bacterial Spot",
        "plant": "Tomato",
        "description": "Bacterial infection causing dark, greasy spots on leaves, stems, and fruits",
        "causes": ["Bacterial pathogen Xanthomonas", "High humidity", "Water splash", "Overcrowding"],
        "severity_levels": {
            "mild": "Small spots on lower leaves only",
            "moderate": "Multiple spots spreading to upper canopy",
            "severe": "Extensive leaf destruction, fruit affected, significant yield loss"
        },
        "treatments": [
            {
                "name": "Copper-based fungicide",
                "dosage": "20-25 g/L",
                "frequency": "Every 7-10 days",
                "cost": "Low",
                "effectiveness": "High"
            },
            {
                "name": "Streptomycin sulfate",
                "dosage": "100-200 ppm",
                "frequency": "Every 10-14 days",
                "cost": "Medium",
                "effectiveness": "Very High"
            },
            {
                "name": "Chlorothalonil",
                "dosage": "1-2 kg/ha",
                "frequency": "Every 7-10 days",
                "cost": "Low",
                "effectiveness": "High"
            }
        ],
        "prevention": [
            "Use disease-resistant varieties",
            "Maintain proper plant spacing for air circulation",
            "Avoid overhead watering; use drip irrigation",
            "Remove infected leaves and plant debris",
            "Sanitize tools between plants",
            "Practice crop rotation (2-3 years)"
        ],
        "weather_risk_factors": {
            "high_humidity": 0.8,
            "high_temperature": 0.6,
            "leaf_wetness": 0.9,
            "rainfall": 0.7
        }
    },
    "Tomato_Early_blight": {
        "name": "Tomato Early Blight",
        "plant": "Tomato",
        "description": "Fungal disease causing concentric rings on lower leaves, gradually moving upward",
        "causes": ["Fungus Alternaria solani", "High humidity", "Warm temperatures (24-30°C)", "Infected debris"],
        "severity_levels": {
            "mild": "Small spots on lower leaves with concentric rings",
            "moderate": "Multiple leaves affected, defoliation starting",
            "severe": "Severe defoliation, fruits exposed to sunscald, significant yield loss"
        },
        "treatments": [
            {
                "name": "Mancozeb",
                "dosage": "2-2.5 kg/ha",
                "frequency": "Every 10-14 days",
                "cost": "Low",
                "effectiveness": "High"
            },
            {
                "name": "Chlorothalonil",
                "dosage": "1-2 kg/ha",
                "frequency": "Every 7-10 days",
                "cost": "Low",
                "effectiveness": "Very High"
            },
            {
                "name": "Azoxystrobin",
                "dosage": "250ml/ha",
                "frequency": "Every 14 days",
                "cost": "Medium",
                "effectiveness": "Very High"
            }
        ],
        "prevention": [
            "Remove lower leaves (up to 12 inches) on young plants",
            "Maintain good air circulation through pruning",
            "Use drip irrigation to keep foliage dry",
            "Apply mulch to prevent soil splash",
            "Destroy infected plant material",
            "Practice crop rotation with non-solanaceous crops"
        ],
        "weather_risk_factors": {
            "high_humidity": 0.85,
            "high_temperature": 0.7,
            "leaf_wetness": 0.9,
            "rainfall": 0.75
        }
    },
    "Tomato_Late_blight": {
        "name": "Tomato Late Blight",
        "plant": "Tomato",
        "description": "Severe fungal disease causing water-soaked spots on leaves and fruits, leading to rapid plant collapse",
        "causes": ["Oomycete Phytophthora infestans", "Cool, wet conditions", "High humidity", "Poor air circulation"],
        "severity_levels": {
            "mild": "Small water-soaked spots on leaf margins",
            "moderate": "Large necrotic patches, white mold on undersides, fruit spotting",
            "severe": "Rapid plant death, complete crop loss if untreated"
        },
        "treatments": [
            {
                "name": "Metalaxyl + Mancozeb",
                "dosage": "2.5 kg/ha",
                "frequency": "Every 10-14 days",
                "cost": "Medium",
                "effectiveness": "Very High"
            },
            {
                "name": "Ridomil Gold",
                "dosage": "2-2.5 kg/ha",
                "frequency": "Every 7-10 days",
                "cost": "High",
                "effectiveness": "Very High"
            },
            {
                "name": "Copper hydroxide",
                "dosage": "20-25 g/L",
                "frequency": "Every 7-10 days",
                "cost": "Low",
                "effectiveness": "High"
            }
        ],
        "prevention": [
            "Use resistant varieties when possible",
            "Ensure excellent air circulation",
            "Avoid overhead watering",
            "Space plants adequately",
            "Monitor weather closely during cool, wet periods",
            "Remove and destroy infected plant parts immediately",
            "Sanitize greenhouse/field equipment"
        ],
        "weather_risk_factors": {
            "high_humidity": 0.95,
            "cool_temperature": 0.9,
            "leaf_wetness": 0.95,
            "rainfall": 0.9
        }
    },
    "Tomato_Leaf_Mold": {
        "name": "Tomato Leaf Mold",
        "plant": "Tomato",
        "description": "Fungal disease causing yellowing on upper leaf surface and olive-brown mold on lower surface",
        "causes": ["Fungus Fulvia fulva", "High humidity (> 85%)", "Warm temperatures (18-27°C)", "Poor ventilation"],
        "severity_levels": {
            "mild": "Small yellowish patches on leaves",
            "moderate": "Multiple leaves affected, mold visible on undersides, some leaf drop",
            "severe": "Severe defoliation, reduced photosynthesis, fruit ripening problems"
        },
        "treatments": [
            {
                "name": "Sulfur powder",
                "dosage": "5-6 kg/ha",
                "frequency": "Every 7-10 days",
                "cost": "Low",
                "effectiveness": "Medium"
            },
            {
                "name": "Chlorothalonil",
                "dosage": "1-2 kg/ha",
                "frequency": "Every 7-10 days",
                "cost": "Low",
                "effectiveness": "High"
            },
            {
                "name": "Difconazole",
                "dosage": "200ml/ha",
                "frequency": "Every 14 days",
                "cost": "Medium",
                "effectiveness": "Very High"
            }
        ],
        "prevention": [
            "Reduce humidity through better ventilation",
            "Space plants for air circulation",
            "Avoid overhead watering",
            "Remove lower leaves as plants grow",
            "Prune suckers and lower foliage",
            "Keep greenhouse/field clean from plant debris",
            "Use resistant varieties in greenhouses"
        ],
        "weather_risk_factors": {
            "high_humidity": 0.95,
            "warm_temperature": 0.7,
            "leaf_wetness": 0.85,
            "rainfall": 0.6
        }
    },
    "Tomato_Septoria_leaf_spot": {
        "name": "Tomato Septoria Leaf Spot",
        "plant": "Tomato",
        "description": "Fungal disease causing small circular spots with dark borders and grayish centers with dark pycnidia",
        "causes": ["Fungus Septoria lycopersici", "Water splash", "High humidity", "Warm temperatures"],
        "severity_levels": {
            "mild": "Few spots on lower leaves",
            "moderate": "Multiple affected leaves, some yellowing, moderate defoliation",
            "severe": "Extensive leaf loss, exposed fruits, significant yield reduction"
        },
        "treatments": [
            {
                "name": "Mancozeb",
                "dosage": "2-2.5 kg/ha",
                "frequency": "Every 10-14 days",
                "cost": "Low",
                "effectiveness": "High"
            },
            {
                "name": "Chlorothalonil",
                "dosage": "1-2 kg/ha",
                "frequency": "Every 7-10 days",
                "cost": "Low",
                "effectiveness": "High"
            },
            {
                "name": "Benomyl",
                "dosage": "500-750ml/ha",
                "frequency": "Every 14 days",
                "cost": "Medium",
                "effectiveness": "High"
            }
        ],
        "prevention": [
            "Avoid overhead watering; use drip irrigation",
            "Space plants adequately for air flow",
            "Remove infected leaves and debris",
            "Disinfect tools with bleach solution",
            "Practice 2-3 year crop rotation",
            "Use certified disease-free seeds",
            "Keep field free from weeds and volunteering plants"
        ],
        "weather_risk_factors": {
            "high_humidity": 0.8,
            "warm_temperature": 0.6,
            "leaf_wetness": 0.85,
            "rainfall": 0.75
        }
    },
    "Tomato_Spider_mites_Two_spotted_spider_mite": {
        "name": "Tomato Spider Mites (Two-spotted)",
        "plant": "Tomato",
        "description": "Pest causing stippling and yellowing of leaves, eventually turning brown and dropping",
        "causes": ["Tetranychus urticae mite", "Hot, dry conditions", "High temperatures (>25°C)", "Low humidity"],
        "severity_levels": {
            "mild": "Slight stippling on leaves, webbing visible",
            "moderate": "Significant yellowing, some leaf drop, reduced plant vigor",
            "severe": "Severe defoliation, stunted growth, reduced fruit quality and size"
        },
        "treatments": [
            {
                "name": "Sulfur dust",
                "dosage": "5-6 kg/ha",
                "frequency": "Every 7-10 days",
                "cost": "Low",
                "effectiveness": "Medium"
            },
            {
                "name": "Neem oil",
                "dosage": "30-50 ml/L",
                "frequency": "Every 7 days",
                "cost": "Medium",
                "effectiveness": "Medium"
            },
            {
                "name": "Dicofol",
                "dosage": "500ml/ha",
                "frequency": "Every 14 days",
                "cost": "Medium",
                "effectiveness": "High"
            }
        ],
        "prevention": [
            "Maintain adequate soil moisture to increase humidity",
            "Remove heavily infested leaves",
            "Use reflective mulches to confuse mites",
            "Introduce predatory mites (Phytoseiulus persimilis)",
            "Spray water on plants to remove mites and increase humidity",
            "Monitor plants regularly for early detection",
            "Avoid excessive nitrogen fertilization"
        ],
        "weather_risk_factors": {
            "high_temperature": 0.9,
            "low_humidity": 0.85,
            "dry_conditions": 0.8,
            "rainfall": -0.5
        }
    },
    "Tomato_Tomato_mosaic_virus": {
        "name": "Tomato Mosaic Virus",
        "plant": "Tomato",
        "description": "Viral disease causing mottling, mosaic patterns, and leaf distortion",
        "causes": ["Tobacco Mosaic Virus (TMV)", "Contaminated touch", "Tools", "Infected seed/soil"],
        "severity_levels": {
            "mild": "Light mosaic, slight leaf distortion",
            "moderate": "Clear mosaic pattern, moderate leaf distortion, stunted growth",
            "severe": "Severe distortion, color break in fruits, significant yield loss"
        },
        "treatments": [
            {
                "name": "Neem oil spray",
                "dosage": "30-50 ml/L",
                "frequency": "Every 7-10 days",
                "cost": "Low",
                "effectiveness": "Low"
            },
            {
                "name": "Remove infected plants",
                "dosage": "N/A",
                "frequency": "Immediate",
                "cost": "N/A",
                "effectiveness": "Very High"
            }
        ],
        "prevention": [
            "Use resistant varieties",
            "Use certified disease-free seeds",
            "Sanitize hands and tools before handling plants",
            "Do not smoke near plants (tobacco carries TMV)",
            "Remove and destroy infected plants immediately",
            "Wash hands frequently during field work",
            "Monitor for early symptoms",
            "Avoid planting near other solanaceous crops"
        ],
        "weather_risk_factors": {
            "high_temperature": 0.5,
            "high_humidity": 0.4,
            "temperature_fluctuation": 0.6
        }
    },
    "Tomato__Target_Spot": {
        "name": "Tomato Target Spot",
        "plant": "Tomato",
        "description": "Fungal disease causing concentric target-like rings with yellow halo on leaves",
        "causes": ["Fungus Corynespora cassiicola", "High humidity", "Warm, wet conditions", "Overhead watering"],
        "severity_levels": {
            "mild": "Few target-shaped spots on lower leaves",
            "moderate": "Multiple affected leaves, progressive spread upward",
            "severe": "Extensive defoliation, fruit damage, significant yield loss"
        },
        "treatments": [
            {
                "name": "Chlorothalonil",
                "dosage": "1-2 kg/ha",
                "frequency": "Every 7-10 days",
                "cost": "Low",
                "effectiveness": "High"
            },
            {
                "name": "Azoxystrobin",
                "dosage": "250ml/ha",
                "frequency": "Every 14 days",
                "cost": "Medium",
                "effectiveness": "Very High"
            }
        ],
        "prevention": [
            "Avoid overhead watering",
            "Ensure good plant spacing and air circulation",
            "Remove infected leaves regularly",
            "Apply copper-sulfur sprays preventatively",
            "Practice crop rotation with non-solanaceous crops",
            "Sanitize tools and equipment"
        ],
        "weather_risk_factors": {
            "high_humidity": 0.85,
            "warm_temperature": 0.7,
            "leaf_wetness": 0.9,
            "rainfall": 0.75
        }
    },
    "Tomato__Tomato_YellowLeaf__Curl_Virus": {
        "name": "Tomato Yellow Leaf Curl Virus",
        "plant": "Tomato",
        "description": "Severe viral disease transmitted by whiteflies causing leaf curling, yellowing, and stunted growth",
        "causes": ["Whitefly-transmitted virus (TYLCV)", "Whitefly vector Bemisia tabaci", "Contaminated weeds"],
        "severity_levels": {
            "mild": "Slight yellowing and leaf curling on upper leaves",
            "moderate": "Obvious curling, chlorotic leaves, stunted plant growth",
            "severe": "Complete leaf deformation, severe stunting, plant death, zero fruit set"
        },
        "treatments": [
            {
                "name": "Insecticides for whitefly control",
                "dosage": "As per label",
                "frequency": "Every 7-14 days",
                "cost": "Medium",
                "effectiveness": "Medium"
            }
        ],
        "prevention": [
            "Use resistant varieties when available",
            "Use reflective silver mulches to repel whiteflies",
            "Install yellow sticky traps for monitoring",
            "Control weeds where virus overwinters",
            "Spray oil to disrupt whitefly reproduction",
            "Use insecticidal soaps or neem oil",
            "Monitor closely for whitefly presence",
            "Avoid planting near previously infected areas"
        ],
        "weather_risk_factors": {
            "warm_temperature": 0.8,
            "low_rainfall": 0.6,
            "hot_season": 0.85
        }
    },
    "Tomato_healthy": {
        "name": "Healthy Tomato",
        "plant": "Tomato",
        "description": "Plant is healthy with no visible disease symptoms",
        "causes": [],
        "severity_levels": {},
        "treatments": [],
        "prevention": [
            "Maintain proper watering schedule",
            "Use balanced fertilization",
            "Monitor plants regularly",
            "Remove any diseased leaves immediately",
            "Practice good garden hygiene"
        ],
        "weather_risk_factors": {}
    },
    # Potato diseases
    "Potato___Early_blight": {
        "name": "Potato Early Blight",
        "plant": "Potato",
        "description": "Fungal disease causing concentric rings on lower leaves, gradually moving upward",
        "causes": ["Fungus Alternaria solani", "High humidity", "Warm temperatures (20-25°C)", "Infected debris"],
        "severity_levels": {
            "mild": "Few spots on lower leaves",
            "moderate": "Progressive leaf damage, some defoliation",
            "severe": "Severe defoliation, tuber yield significantly reduced"
        },
        "treatments": [
            {
                "name": "Mancozeb",
                "dosage": "2-2.5 kg/ha",
                "frequency": "Every 10-14 days",
                "cost": "Low",
                "effectiveness": "High"
            },
            {
                "name": "Chlorothalonil",
                "dosage": "1-2 kg/ha",
                "frequency": "Every 7-10 days",
                "cost": "Low",
                "effectiveness": "High"
            }
        ],
        "prevention": [
            "Use certified seed potatoes",
            "Space plants adequately",
            "Apply mulch to reduce soil splash",
            "Remove infected leaves and debris",
            "Avoid overhead watering",
            "Practice crop rotation",
            "Destroy cull piles far from fields"
        ],
        "weather_risk_factors": {
            "high_humidity": 0.8,
            "warm_temperature": 0.7,
            "leaf_wetness": 0.85,
            "rainfall": 0.75
        }
    },
    "Potato___Late_blight": {
        "name": "Potato Late Blight",
        "plant": "Potato",
        "description": "Severe oomycete disease causing rapid destruction of foliage and tuber rot",
        "causes": ["Oomycete Phytophthora infestans", "Cool, wet conditions", "High humidity", "Poor ventilation"],
        "severity_levels": {
            "mild": "Small water-soaked spots on leaf margins",
            "moderate": "Large necrotic areas, white mold on undersides, some tuber spotting",
            "severe": "Complete plant collapse, extensive tuber rot, total crop loss"
        },
        "treatments": [
            {
                "name": "Metalaxyl + Mancozeb",
                "dosage": "2.5 kg/ha",
                "frequency": "Every 7-10 days",
                "cost": "Medium",
                "effectiveness": "Very High"
            },
            {
                "name": "Ridomil Gold",
                "dosage": "2-2.5 kg/ha",
                "frequency": "Every 7-10 days",
                "cost": "High",
                "effectiveness": "Very High"
            }
        ],
        "prevention": [
            "Use resistant varieties",
            "Use certified disease-free seed",
            "Ensure good air circulation and drainage",
            "Monitor weather closely during cool, wet periods",
            "Remove infected plants immediately",
            "Apply preventive sprays during high-risk weather",
            "Hill soil over tubers to prevent infection",
            "Harvest at maturity and allow vines to dry"
        ],
        "weather_risk_factors": {
            "high_humidity": 0.95,
            "cool_temperature": 0.85,
            "leaf_wetness": 0.9,
            "rainfall": 0.85
        }
    },
    "Potato___healthy": {
        "name": "Healthy Potato",
        "plant": "Potato",
        "description": "Plant is healthy with no visible disease symptoms",
        "causes": [],
        "severity_levels": {},
        "treatments": [],
        "prevention": [
            "Use certified seed potatoes",
            "Maintain proper watering",
            "Use balanced fertilization",
            "Monitor plants regularly",
            "Practice crop rotation"
        ],
        "weather_risk_factors": {}
    },
    # Pepper diseases
    "Pepper__bell___Bacterial_spot": {
        "name": "Pepper Bacterial Spot",
        "plant": "Pepper",
        "description": "Bacterial disease causing dark, greasy spots on leaves, stems, and fruits",
        "causes": ["Xanthomonas bacteria", "High humidity", "Water splash", "Temperature 25-30°C"],
        "severity_levels": {
            "mild": "Small spots on lower leaves",
            "moderate": "Multiple spots on multiple leaves, fruit spotting",
            "severe": "Extensive leaf damage, unmarketable fruits, defoliation"
        },
        "treatments": [
            {
                "name": "Copper-based fungicide",
                "dosage": "20-25 g/L",
                "frequency": "Every 7-10 days",
                "cost": "Low",
                "effectiveness": "High"
            },
            {
                "name": "Streptomycin sulfate",
                "dosage": "100-200 ppm",
                "frequency": "Every 10-14 days",
                "cost": "Medium",
                "effectiveness": "Very High"
            }
        ],
        "prevention": [
            "Use disease-resistant varieties",
            "Maintain proper spacing",
            "Avoid overhead watering",
            "Remove infected leaves",
            "Sanitize tools between plants",
            "Practice crop rotation (3 years minimum)"
        ],
        "weather_risk_factors": {
            "high_humidity": 0.8,
            "warm_temperature": 0.7,
            "leaf_wetness": 0.85,
            "rainfall": 0.7
        }
    },
    "Pepper__bell___healthy": {
        "name": "Healthy Pepper",
        "plant": "Pepper",
        "description": "Plant is healthy with no visible disease symptoms",
        "causes": [],
        "severity_levels": {},
        "treatments": [],
        "prevention": [
            "Ensure proper watering",
            "Monitor for pest and disease",
            "Use balanced fertilization",
            "Maintain good plant spacing"
        ],
        "weather_risk_factors": {}
    }
}

def get_disease_info(disease_name):
    """Retrieve disease information by name"""
    return DISEASE_DATABASE.get(disease_name, None)

def get_all_disease_names():
    """Get list of all disease names"""
    return list(DISEASE_DATABASE.keys())

def get_plant_diseases(plant_name):
    """Get all diseases for a specific plant"""
    return {name: info for name, info in DISEASE_DATABASE.items() if info["plant"] == plant_name}
