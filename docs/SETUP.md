# Setup Guide for Jetson Orin Nano Super

## Hardware Setup

### Step 1: Kit Contents Verification
- Jetson Orin Nano 8GB module with heatsink
- Reference carrier board
- DC Power Supply
- 802.11ac wireless NIC
- Quick Start Guide

### Step 2: Physical Setup
1. **microSD Card Installation**
   - Locate microSD slot on underside
   - Insert card with gold contacts facing heatsink
   - Ensure proper seating

2. **Display & Peripheral Connection**
   - Connect DisplayPort to monitor
   - Connect USB keyboard and mouse
   - Connect ethernet cable (optional)

3. **Power Connection**
   - Insert DC power jack
   - Verify green LED indicator

## Software Setup

### Step 1: First Boot
1. Power on device
2. Accept NVIDIA EULA
3. Select system language
4. Configure keyboard layout
5. Set timezone
6. Configure wireless network (optional)
7. Create username and password

### Step 2: System Optimization
```bash
# Set maximum performance mode
sudo nvpmodel -m 0
sudo jetson_clocks

# Verify system status
tegrastats
```

### Step 3: Development Environment
```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install essential tools
sudo apt install -y python3-pip git cmake
sudo apt install -y python3-tensorrt
```

## Network Configuration

### Wired Connection
1. Plug in ethernet cable
2. Connection should be automatic
3. Verify with `ip addr show`

### Wireless Connection
1. Click network icon in top bar
2. Select your network
3. Enter password
4. Verify connection

## Troubleshooting

### Common Issues

1. **No Display Output**
   - Check DisplayPort connection
   - Try different cable/adapter
   - Verify monitor input source

2. **Power Issues**
   - Check power adapter connection
   - Verify green LED status
   - Test power outlet

3. **Network Problems**
   - Check cable connections
   - Verify router settings
   - Test with different network

### System Checks
```bash
# Check system status
tegrastats

# View system logs
journalctl -xe

# Check GPU status
nvidia-smi
```

## Next Steps

After completing basic setup:
1. Proceed to [Model Optimization](OPTIMIZATION.md)
2. Review [Performance Tuning](PERFORMANCE.md)
3. Explore [Example Projects](EXAMPLES.md)