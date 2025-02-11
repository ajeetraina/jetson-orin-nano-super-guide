# Performance Optimization Labs

## Lab 1: System Monitoring

### Objectives
- Monitor system resources
- Understand performance metrics
- Optimize system settings

### Prerequisites
- jtop installed
- Basic understanding of Linux
- Sample workloads

### Steps

1. **Resource Monitoring**
   ```bash
   # Monitor CPU, GPU, memory
   sudo jtop
   
   # Monitor power usage
   sudo tegrastats
   ```

2. **Performance Profiling**
   ```bash
   # Profile application
   sudo perf record -a -g
   
   # Analyze bottlenecks
   sudo perf report
   ```

3. **Temperature Monitoring**
   ```bash
   # Monitor thermal zones
   watch -n 1 cat /sys/devices/virtual/thermal/thermal_zone*/temp
   ```

### Validation
- Resource usage tracked
- Bottlenecks identified
- Temperature monitored

## Lab 2: Power Optimization

### Objectives
- Understand power modes
- Optimize power consumption
- Balance performance and power

### Steps

1. **Power Mode Configuration**
   ```bash
   # List available power modes
   sudo nvpmodel -q --verbose
   
   # Set power mode
   sudo nvpmodel -m [MODE]
   ```

2. **Clock Management**
   ```bash
   # Set maximum clocks
   sudo jetson_clocks
   
   # Reset clocks
   sudo jetson_clocks --restore
   ```

3. **Power Monitoring**
   ```bash
   # Monitor power consumption
   sudo tegrastats | grep 'RAM'
   ```

### Validation
- Power modes work
- Clocks configured
- Power consumption reduced

## Lab 3: Memory Optimization

### Objectives
- Optimize memory usage
- Manage swap space
- Monitor memory performance

### Steps

1. **Memory Analysis**
   ```bash
   # Monitor memory usage
   free -h
   vmstat 1
   ```

2. **Swap Configuration**
   ```bash
   # Create swap file
   sudo fallocate -l 4G /swapfile
   sudo chmod 600 /swapfile
   sudo mkswap /swapfile
   sudo swapon /swapfile
   ```

3. **Memory Tuning**
   ```bash
   # Adjust kernel parameters
   sudo sysctl -w vm.swappiness=10
   sudo sysctl -w vm.vfs_cache_pressure=50
   ```

### Validation
- Memory usage optimized
- Swap configured
- System performance improved

## Next Steps
- Advanced profiling techniques
- Custom power modes
- Thermal management strategies