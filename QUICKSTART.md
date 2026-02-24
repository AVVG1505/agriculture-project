# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Option 1: Automated Setup (Recommended)

```bash
chmod +x setup.sh
./setup.sh
```

This will automatically:
- Create Python virtual environment
- Install all dependencies
- Create necessary directories
- Set up environment files
- Install frontend packages

### Option 2: Manual Setup

#### 1. Backend Setup

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create directories
mkdir -p backend/model backend/uploads backend/database backend/logs

# Copy environment file
cp backend/.env.example backend/.env
```

#### 2. Train the Model (First Time Only)

```bash
cd ml
python train.py
```

This will train on PlantVillage dataset and save the model to `backend/model/`

#### 3. Start Backend

```bash
cd backend
python app.py
```

API running at: `http://localhost:5000`

#### 4. Frontend Setup (New Terminal)

```bash
cd frontend
npm install
npm start
```

Frontend running at: `http://localhost:3000`

## 🧪 Testing

### Test Backend API

```bash
# Health check
curl http://localhost:5000/api/health

# Get all diseases
curl http://localhost:5000/api/diseases

# Get specific disease info
curl http://localhost:5000/api/disease/Tomato_Early_blight
```

### Test Disease Detection

```bash
# Upload image for detection
curl -F "image=@your_image.jpg" \
     -F "location=New York" \
     http://localhost:5000/api/detect
```

## 📁 File Structure After Setup

```
plant-disease-ai/
├── backend/
│   ├── model/                  # Trained model files
│   ├── uploads/                # User uploaded images
│   ├── database/               # SQLite database
│   ├── logs/                   # Application logs
│   ├── app.py                  # Flask API
│   └── .env                    # Environment config
├── frontend/
│   ├── node_modules/           # Dependencies
│   ├── public/                 # Static files
│   └── src/                    # React components
└── ml/
    ├── PlantVillage/           # Dataset
    └── train.py                # Training script
```

## 🔧 Troubleshooting

### Python version issue
```bash
# Use python3
source venv/bin/activate
```

### Port already in use
```bash
# Change port in backend/app.py
# In frontend/.env: REACT_APP_API_URL=http://localhost:PORT
```

### Model not found
```bash
# Train the model first
cd ml
python train.py
```

### Frontend not connecting to backend
- Check backend is running on `http://localhost:5000`
- Check `frontend/.env` has correct API URL
- Browser console (F12) for errors

## 📊 Expected Output

### Backend Startup
```
✓ Model loaded successfully
 * Running on http://0.0.0.0:5000
```

### Frontend Startup
```
Compiled successfully!
Local: http://localhost:3000
```

### First Detection
```json
{
  "detected_disease": "Tomato_Early_blight",
  "confidence": 0.92,
  "severity": "Moderate",
  "top_3_predictions": [...],
  "treatments": [...],
  "disease_info": {...}
}
```

## 🎯 Next Steps

1. **Upload a plant leaf image** to test detection
2. **View treatment recommendations**
3. **Set crop care reminders**
4. **Check your detection history**
5. **Calculate disease risk** with weather data

## 📚 Documentation

- Full documentation: `README.md`
- API reference: `README.md#-api-endpoints`
- Model details: `README.md#-model-details`
- Deployment guide: `README.md#-deployment`

## 🆘 Need Help?

1. Check README.md for detailed documentation
2. Review logs in `backend/logs/`
3. Check browser console for frontend errors
4. Verify all dependencies installed: `pip list`

---

**Happy farming with AI! 🌱**
