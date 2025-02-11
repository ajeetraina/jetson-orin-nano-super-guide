# Workshop Deployment Guide

## Local Development

### Setup Environment
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Run Development Server
```bash
# Start mkdocs server
mkdocs serve
```

## Vercel Deployment

### 1. Configure vercel.json
```json
{
    "buildCommand": "mkdocs build",
    "outputDirectory": "site",
    "framework": "mkdocs",
    "installCommand": "pip install -r requirements.txt"
}
```

### 2. Deploy to Vercel
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel deploy
```

## Workshop Environment Setup

### Prerequisites for Participants
1. Jetson Orin Nano Super Developer Kit
2. BME680 sensor
3. Basic Python knowledge
4. Linux/Ubuntu familiarity

### Software Requirements
```bash
# System packages
sudo apt update && sudo apt install -y \
    python3-pip \
    git \
    cmake \
    python3-tensorrt \
    i2c-tools

# Python packages
pip install -r workshop-requirements.txt
```

## Lab Setup Instructions

### Lab 1: Basic Setup
- Hardware connections
- Software installation
- System verification

### Lab 2: AI Model Setup
- Model download
- TensorRT optimization
- Performance testing

### Lab 3: Sensor Integration
- BME680 connection
- Data collection
- AI integration

## Troubleshooting Guide

### Common Issues
1. TensorRT-LLM Installation
2. I2C Connection
3. Model Optimization
4. Memory Management

## Support Resources

### Documentation
- [Jetson Documentation](https://docs.nvidia.com/jetson/)
- [TensorRT-LLM Guide](https://github.com/NVIDIA/TensorRT-LLM)
- [BME680 Datasheet](https://www.bosch-sensortec.com/products/environmental-sensors/gas-sensors/bme680/)

### Community
- [NVIDIA Developer Forums](https://forums.developer.nvidia.com/)
- [GitHub Issues](https://github.com/your-repo/issues)

## Feedback Collection

### Workshop Feedback Form
```html
<form action="/submit-feedback" method="POST">
    <label>Lab Quality (1-5):</label>
    <input type="number" min="1" max="5" name="quality" required>
    
    <label>Difficulty Level (1-5):</label>
    <input type="number" min="1" max="5" name="difficulty" required>
    
    <label>Comments:</label>
    <textarea name="comments"></textarea>
    
    <button type="submit">Submit Feedback</button>
</form>
```

## Workshop Updates

### Version Control
```bash
# Get latest updates
git pull origin main

# Update dependencies
pip install -r requirements.txt --upgrade
```

### Content Updates
1. Check workshop repository for updates
2. Pull latest changes
3. Rebuild documentation
4. Deploy updates