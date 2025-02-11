#!/usr/bin/env python3

import subprocess
import argparse
import json
import time
import os

class JetsonOptimizer:
    def __init__(self):
        self.current_mode = self._get_current_mode()
        self.temperature = self._get_temperature()
        
    def _get_current_mode(self):
        """Get current power mode"""
        result = subprocess.run(['nvpmodel', '-q'], capture_output=True, text=True)
        return result.stdout
    
    def _get_temperature(self):
        """Get current temperature"""
        try:
            temp = subprocess.run(['cat', '/sys/devices/virtual/thermal/thermal_zone0/temp'],
                                capture_output=True, text=True)
            return float(temp.stdout) / 1000
        except:
            return None

    def set_max_performance(self):
        """Set maximum performance mode"""
        subprocess.run(['sudo', 'nvpmodel', '-m', '0'])
        subprocess.run(['sudo', 'jetson_clocks'])
        
    def optimize_gpu_clocks(self):
        """Optimize GPU clock settings"""
        # Set maximum GPU frequency
        subprocess.run(['sudo', 'sh', '-c', 'echo 1 > /sys/devices/gpu.0/force_idle'])
        subprocess.run(['sudo', 'sh', '-c', 'echo 1000 > /sys/devices/gpu.0/gpu_rate'])

    def optimize_cpu_clocks(self):
        """Optimize CPU clock settings"""
        # Set CPU governor to performance
        for i in range(6):  # 6-core CPU
            subprocess.run(['sudo', 'sh', '-c', f'echo performance > /sys/devices/system/cpu/cpu{i}/cpufreq/scaling_governor'])

    def optimize_memory(self):
        """Optimize memory settings"""
        # Set VM swappiness
        subprocess.run(['sudo', 'sysctl', 'vm.swappiness=10'])
        
        # Set cache pressure
        subprocess.run(['sudo', 'sysctl', 'vm.vfs_cache_pressure=50'])

    def optimize_thermal(self):
        """Optimize thermal settings"""
        if self.temperature and self.temperature > 80:
            print("Warning: High temperature detected. Adjusting fan settings...")
            # Increase fan speed
            subprocess.run(['sudo', 'sh', '-c', 'echo 255 > /sys/devices/pwm-fan/target_pwm'])

    def apply_all_optimizations(self):
        """Apply all optimizations"""
        print("Applying performance optimizations...")
        
        self.set_max_performance()
        time.sleep(1)
        
        self.optimize_gpu_clocks()
        time.sleep(1)
        
        self.optimize_cpu_clocks()
        time.sleep(1)
        
        self.optimize_memory()
        time.sleep(1)
        
        self.optimize_thermal()
        
        print("\nOptimizations applied. Current status:")
        self.print_status()

    def print_status(self):
        """Print current system status"""
        print("\nSystem Status:")
        print(f"Power Mode: {self._get_current_mode()}")
        print(f"Temperature: {self._get_temperature()}°C")
        
        # Get CPU frequencies
        cpu_freqs = []
        for i in range(6):
            try:
                with open(f'/sys/devices/system/cpu/cpu{i}/cpufreq/scaling_cur_freq') as f:
                    freq = int(f.read().strip()) / 1000
                    cpu_freqs.append(freq)
            except:
                cpu_freqs.append(None)
        
        print("\nCPU Frequencies (MHz):")
        for i, freq in enumerate(cpu_freqs):
            if freq:
                print(f"CPU{i}: {freq}")

def main():
    parser = argparse.ArgumentParser(description='Optimize Jetson Orin Nano Super performance')
    parser.add_argument('--max-perf', action='store_true', help='Set maximum performance mode')
    parser.add_argument('--optimize-all', action='store_true', help='Apply all optimizations')
    parser.add_argument('--status', action='store_true', help='Print current status')
    
    args = parser.parse_args()
    optimizer = JetsonOptimizer()
    
    if args.max_perf:
        optimizer.set_max_performance()
    elif args.optimize_all:
        optimizer.apply_all_optimizations()
    elif args.status:
        optimizer.print_status()
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
