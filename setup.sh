#!/bin/bash

# Plant Disease AI - Setup Script
# This script sets up the entire development environment

set -e

echo "🌱 Plant Disease AI - Setup Script"
echo "=================================="

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python
echo -e "${BLUE}Checking Python installation...${NC}"
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo -e "${GREEN}✓ Python ${PYTHON_VERSION} found${NC}"

# Check Node.js
echo -e "${BLUE}Checking Node.js installation...${NC}"
if ! command -v node &> /dev/null; then
    echo "Node.js is not installed. Please install Node.js 14 or higher."
    exit 1
fi
NODE_VERSION=$(node --version)
echo -e "${GREEN}✓ Node.js ${NODE_VERSION} found${NC}"

# Setup Python environment
echo -e "${BLUE}Setting up Python virtual environment...${NC}"
python3 -m venv venv
source venv/bin/activate
echo -e "${GREEN}✓ Virtual environment created${NC}"

# Install Python dependencies
echo -e "${BLUE}Installing Python dependencies...${NC}"
pip install --upgrade pip
pip install -r requirements.txt
echo -e "${GREEN}✓ Dependencies installed${NC}"

# Create backend directories
echo -e "${BLUE}Creating backend directories...${NC}"
mkdir -p backend/model
mkdir -p backend/uploads
mkdir -p backend/database
mkdir -p backend/logs
echo -e "${GREEN}✓ Backend directories created${NC}"

# Copy environment files
echo -e "${BLUE}Setting up environment files...${NC}"
if [ ! -f backend/.env ]; then
    cp backend/.env.example backend/.env
    echo -e "${GREEN}✓ Backend .env created${NC}"
else
    echo -e "${YELLOW}! Backend .env already exists${NC}"
fi

if [ ! -f frontend/.env ]; then
    cp frontend/.env.example frontend/.env
    echo -e "${GREEN}✓ Frontend .env created${NC}"
else
    echo -e "${YELLOW}! Frontend .env already exists${NC}"
fi

# Install frontend dependencies
echo -e "${BLUE}Installing frontend dependencies...${NC}"
cd frontend
npm install
echo -e "${GREEN}✓ Frontend dependencies installed${NC}"
cd ..

# Check PlantVillage dataset
echo -e "${BLUE}Checking PlantVillage dataset...${NC}"
if [ -d "ml/PlantVillage/PlantVillage" ]; then
    DATASET_COUNT=$(find ml/PlantVillage/PlantVillage -type f \( -name "*.jpg" -o -name "*.jpeg" -o -name "*.png" \) | wc -l)
    echo -e "${GREEN}✓ Dataset found with ${DATASET_COUNT} images${NC}"
else
    echo -e "${YELLOW}! PlantVillage dataset not found${NC}"
    echo "Please ensure the dataset is in: ml/PlantVillage/PlantVillage/"
fi

echo ""
echo -e "${GREEN}=================================="
echo "Setup Complete! 🎉"
echo "==================================${NC}"
echo ""
echo "Next steps:"
echo "1. Train the model (optional, if not already trained):"
echo -e "   ${BLUE}cd ml && python train.py${NC}"
echo ""
echo "2. Start the backend server:"
echo -e "   ${BLUE}cd backend && python app.py${NC}"
echo ""
echo "3. In a new terminal, start the frontend:"
echo -e "   ${BLUE}cd frontend && npm start${NC}"
echo ""
echo "4. Open browser to: http://localhost:3000"
echo ""
echo "For more information, see README.md"
