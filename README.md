
# Plant Disease Detection - Using Machine Learning

##  Project Overview

This is an AI-powered plant disease detection system that combines deep learning with practical agricultural insights. The system includes:

- **Real-time Disease Detection**: Upload leaf images for instant analysis
- **Detailed Treatment Recommendations**: Plant-specific remedies with dosages
- **Weather-based Risk Assessment**: Predict disease risk using environmental conditions
- **Patient History Tracking**: Monitor plant health over time
- **Explainable AI**: Visual indicators showing what the model detected
- **Crop Care Reminders**: Personalized maintenance reminders
- **Offline Capability**: Download models for offline detection

##  Supported Plants & Diseases

### Tomato
- Bacterial Spot
- Early Blight
- Late Blight
- Leaf Mold
- Septoria Leaf Spot
- Spider Mites
- Mosaic Virus
- Target Spot
- Yellow Leaf Curl Virus
- Healthy

### Potato
- Early Blight
- Late Blight
- Healthy

### Pepper
- Bacterial Spot
- Healthy

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js 14+
- Git
- Virtual environment tool (venv or conda)

### Backend Setup

1. **Create and activate Python virtual environment:**
```bash
cd /Users/avvg/Desktop/plant-disease-ai
python3 -m venv venv
source venv/bin/activate
```

2. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

3. **Download PlantVillage Dataset** (Already in your project)
   - Dataset structure: `ml/PlantVillage/PlantVillage/[disease_name]/[images]`

4. **Train the model:**
```bash
cd ml
python train.py
```

This will:
- Load images from PlantVillage dataset
- Train a ResNet50 model with transfer learning
- Save model to `backend/model/plant_disease_model.h5`
- Generate class indices and metadata

5. **Start the Flask backend:**
```bash
cd backend
python app.py
```

Backend will be running at `http://localhost:5000`

### Frontend Setup

1. **Install Node.js dependencies:**
```bash
cd frontend
npm install
```

2. **Start the React development server:**
```bash
npm start
```

Frontend will open at `http://localhost:3000`

##  API Endpoints

### Disease Detection
```
POST /api/detect
- Upload image and get disease prediction
- Parameters: image (file), location (optional), user_id (optional)
- Returns: disease_name, confidence, severity, treatments, etc.
```

### Disease Information
```
GET /api/disease/<disease_name>
- Get detailed info about specific disease

GET /api/diseases
- Get list of all detectable diseases

GET /api/diseases/by-plant/<plant_name>
- Get diseases for specific plant
```

### User History
```
GET /api/history/<user_id>
- Get detection history

GET /api/stats/<user_id>
- Get user statistics
```

### Weather Risk Assessment
```
POST /api/weather-risk
- Calculate disease risk based on weather
```

### Crop Care Reminders
```
GET /api/reminders/<user_id>
POST /api/reminders
- Manage crop care reminders
```

### Offline Model
```
GET /api/offline-model
- Download model for offline use
```

## Frontend Features

### 1. Disease Detector Page
- Drag-and-drop image upload
- Real-time disease detection
- Confidence scores
- Top 3 alternative predictions
- Severity assessment
- Treatment recommendations

### 2. Detection History
- View all past detections
- Timestamp tracking
- Detection confidence
- Personal notes

### 3. Risk Calculator
- Input weather conditions
- Calculate disease risk
- Get weather-based recommendations
- Risk level indicators

### 4. Crop Care Reminders
- Create custom reminders
- Set reminder frequency
- Track reminder history
- Filter by plant type

## Project Structure

```
plant-disease-ai/
├── backend/
│   ├── app.py                 # Flask API
│   ├── utils.py               # Utility functions
│   ├── evaluation.py          # Model evaluation
│   ├── model/                 # Trained models
│   ├── uploads/               # User uploads
│   ├── database/              # SQLite DB
│   └── .env.example           # Environment template
├── frontend/
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── App.jsx            # Main app
│   │   └── index.jsx          # Entry point
│   ├── package.json           # Dependencies
│   └── .env.example           # Environment template
├── ml/
│   ├── train.py               # Model training
│   ├── disease_db.py          # Disease database
│   └── PlantVillage/          # Dataset
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Configuration

### Backend Configuration (.env)
```
FLASK_ENV=development
FLASK_PORT=5000
MODEL_PATH=model/plant_disease_model.h5
UPLOAD_FOLDER=uploads
```

### Frontend Configuration (.env)
```
REACT_APP_API_URL=http://localhost:5000
```

## How It Works

### 1. Image Upload
- User uploads leaf image
- Image is validated and stored

### 2. Preprocessing
- Image resized to 224x224
- Normalized to 0-1 range

### 3. Disease Detection
- ResNet50 model predicts disease
- Returns confidence scores
- Provides top 3 predictions

### 4. Risk Assessment
- Combines multiple factors:
  - Model confidence (35%)
  - Weather conditions (40%)
  - Disease severity (25%)

### 5. Recommendations
- Retrieves disease-specific treatments
- Filters by effectiveness and cost
- Provides prevention measures

## Model Details

- **Architecture**: ResNet50 with transfer learning
- **Pre-trained on**: ImageNet
- **Fine-tuned on**: PlantVillage dataset
- **Input Size**: 224x224 RGB images
- **Output**: Disease classification + confidence scores
- **Data Augmentation**: Yes (rotation, zoom, flip, etc.)
- **Accuracy**: ~95% on test set

## Monitoring & Analytics

The system tracks:
- Detection accuracy
- User engagement
- Disease prevalence
- Risk levels
- Treatment effectiveness

View logs in `backend/logs/`:
- `detections.log`: All detection events
- `errors.log`: Error tracking


## Future Enhancements

- [ ] Multi-language support
- [ ] Mobile app (React Native)
- [ ] Advanced image analysis (zoom, enhance)
- [ ] Real weather API integration
- [ ] Farmer community heatmap
- [ ] Voice assistance
- [ ] Batch image analysis
- [ ] Export reports



---

**Made for Farmers, Powered by AI
