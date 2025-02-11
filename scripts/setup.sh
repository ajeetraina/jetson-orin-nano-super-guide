#!/bin/bash

# Script to setup Jetson Orin Nano Super development environment

echo "Setting up Jetson Orin Nano Super development environment..."

# Update system
echo "Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install essential packages
echo "Installing essential packages..."
sudo apt install -y \
    python3-pip \
    git \
    cmake \
    python3-tensorrt \
    i2c-tools \
    python3-numpy

# Enable maximum performance mode
echo "Setting maximum performance mode..."
sudo nvpmodel -m 0
sudo jetson_clocks

# Clone TensorRT-LLM
echo "Setting up TensorRT-LLM..."
git clone https://github.com/NVIDIA/TensorRT-LLM.git
cd TensorRT-LLM

# Build and install TensorRT-LLM
python3 scripts/build_wheel.py --cuda_version 11.4
pip3 install ./build/tensorrt_llm*.whl

# Create Python virtual environment
echo "Creating Python virtual environment..."
python3 -m venv trt_env
source trt_env/bin/activate

# Verify installation
echo "Verifying installation..."
nvcc --version
tegrastats

echo "Setup complete! Please reboot your system."
