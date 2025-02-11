# Jetson Orin Nano Labs

Welcome to the hands-on laboratory exercises for the NVIDIA Jetson Orin Nano. These labs will help you gain practical experience with edge AI development.

## Lab Categories

- [Getting Started Labs](getting-started.md) - Basic setup and configuration
- [Computer Vision Labs](computer-vision.md) - Image processing and object detection
- [TensorRT Labs](tensorrt.md) - Model optimization and inference
- [Edge AI Labs](edge-ai.md) - Real-world edge computing applications
- [Performance Labs](performance.md) - System monitoring and optimization

## Prerequisites

Before starting the labs, ensure you have:

1. Jetson Orin Nano Developer Kit
2. Power supply
3. microSD card (32GB+ recommended)
4. Display with DisplayPort input
5. USB keyboard and mouse
6. Internet connection

## Lab Environment Setup

```bash
# Update the system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y python3-pip git cmake
sudo apt install -y python3-opencv
sudo apt install -y python3-tensorrt
sudo apt install -y jtop

# Install Python dependencies
pip3 install torch torchvision torchaudio
pip3 install numpy matplotlib jupyter
```

## Lab Structure

Each lab follows this structure:

1. **Objectives** - What you'll learn
2. **Prerequisites** - Required setup and knowledge
3. **Steps** - Detailed instructions
4. **Validation** - How to verify success
5. **Troubleshooting** - Common issues and solutions
6. **Next Steps** - Additional resources and advanced topics