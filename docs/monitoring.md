# Workshop Monitoring and Analytics

## Overview

This guide explains how to monitor workshop participation and system performance using Prometheus and Grafana.

## Setup Monitoring Stack

### 1. Start Monitoring Services
```bash
cd monitoring
docker-compose up -d
```

### 2. Access Dashboards
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000

## Available Metrics

### Workshop Metrics
```python
# Participant tracking
workshop_participants_total

# Lab completion
workshop_lab_completions{lab="lab1"}
workshop_lab_completions{lab="lab2"}
workshop_lab_completions{lab="lab3"}

# Time spent per lab
workshop_lab_duration_seconds{lab="lab1"}
```

### System Metrics
```python
# CPU Usage
node_cpu_seconds_total

# Memory Usage
node_memory_MemTotal_bytes
node_memory_MemFree_bytes

# Disk Usage
node_filesystem_avail_bytes
```

## Grafana Dashboards

### Main Dashboard
- Workshop participation
- Lab completion rates
- System resource usage

### Performance Dashboard
- Model inference times
- Memory utilization
- GPU metrics

## Alerting

### Configure Alerts
```yaml
groups:
  - name: workshop_alerts
    rules:
      - alert: HighResourceUsage
        expr: node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes * 100 < 20
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: High memory usage
```

### Alert Channels
- Email notifications
- Slack integration
- Discord webhooks

## Usage Analytics

### Track Workshop Progress
```python
def track_progress(user_id, lab_id, status):
    """Track user progress through labs"""
    metrics.inc_counter(
        'workshop_lab_completions',
        labels={'lab': lab_id}
    )
```

### Resource Usage
```python
def monitor_resources():
    """Monitor system resources"""
    metrics.gauge(
        'workshop_system_memory',
        psutil.virtual_memory().percent
    )
```

## Reports

### Generate Workshop Report
```python
def generate_report():
    """Generate workshop analytics report"""
    data = {
        'participants': get_metric('workshop_participants_total'),
        'completion_rates': get_metric('workshop_lab_completions'),
        'avg_duration': get_metric('workshop_lab_duration_seconds')
    }
    
    return create_report(data)
```

## Best Practices

1. Regular Monitoring
   - Check dashboards daily
   - Review alerts promptly
   - Track trends

2. Data Retention
   - Configure retention policies
   - Archive historical data
   - Backup important metrics

3. Performance Optimization
   - Monitor resource usage
   - Optimize query performance
   - Scale as needed