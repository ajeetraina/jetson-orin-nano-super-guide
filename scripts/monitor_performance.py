#!/usr/bin/env python3

import time
import psutil
import subprocess
import argparse
import json
from datetime import datetime

class JetsonMonitor:
    def __init__(self, log_file=None):
        self.log_file = log_file
        self.start_time = datetime.now()
        
    def get_cpu_usage(self):
        """Get CPU usage percentage"""
        return psutil.cpu_percent(interval=1, percpu=True)
    
    def get_memory_usage(self):
        """Get memory usage statistics"""
        return dict(psutil.virtual_memory()._asdict())
    
    def get_temperature(self):
        """Get temperature readings"""
        try:
            temps = {}
            for i in range(4):  # Check multiple thermal zones
                try:
                    with open(f'/sys/devices/virtual/thermal/thermal_zone{i}/temp') as f:
                        temps[f'zone{i}'] = float(f.read().strip()) / 1000
                except:
                    continue
            return temps
        except:
            return None
    
    def get_gpu_info(self):
        """Get GPU information using tegrastats"""
        try:
            result = subprocess.run(['tegrastats', '--interval', '1000', '--count', '1'],
                                  capture_output=True, text=True)
            return result.stdout
        except:
            return None
    
    def monitor(self, interval=1, duration=None):
        """Monitor system performance
        
        Args:
            interval: Sampling interval in seconds
            duration: Monitoring duration in seconds (None for continuous)
        """
        try:
            while True:
                stats = {
                    'timestamp': datetime.now().isoformat(),
                    'cpu_usage': self.get_cpu_usage(),
                    'memory': self.get_memory_usage(),
                    'temperature': self.get_temperature(),
                    'gpu': self.get_gpu_info()
                }
                
                self._print_stats(stats)
                
                if self.log_file:
                    with open(self.log_file, 'a') as f:
                        json.dump(stats, f)
                        f.write('\n')
                
                if duration and (datetime.now() - self.start_time).seconds >= duration:
                    break
                    
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\nMonitoring stopped by user")
    
    def _print_stats(self, stats):
        """Print formatted statistics"""
        print("\033[2J\033[H")  # Clear screen
        print(f"=== System Monitor === {stats['timestamp']}")
        
        print("\nCPU Usage (%)")
        for i, usage in enumerate(stats['cpu_usage']):
            print(f"Core {i}: {usage:5.1f}%")
        
        mem = stats['memory']
        print(f"\nMemory Usage:\n"
              f"Total: {mem['total']/1024/1024:,.0f} MB\n"
              f"Used:  {mem['used']/1024/1024:,.0f} MB ({mem['percent']}%)")
        
        if stats['temperature']:
            print("\nTemperatures:")
            for zone, temp in stats['temperature'].items():
                print(f"{zone}: {temp:5.1f}°C")
        
        if stats['gpu']:
            print(f"\nGPU Info:\n{stats['gpu']}")

def main():
    parser = argparse.ArgumentParser(description='Monitor Jetson Orin Nano Super performance')
    parser.add_argument('--interval', type=int, default=1, help='Sampling interval in seconds')
    parser.add_argument('--duration', type=int, help='Monitoring duration in seconds')
    parser.add_argument('--log', help='Log file to save statistics')
    
    args = parser.parse_args()
    
    monitor = JetsonMonitor(args.log)
    monitor.monitor(args.interval, args.duration)

if __name__ == '__main__':
    main()
