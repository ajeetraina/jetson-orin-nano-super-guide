# Data Collection with BME680

## Basic Data Collection

### Reading Sensor Data
```python
def read_sensor_data(sensor):
    """Read all sensor values"""
    if sensor.get_sensor_data():
        return {
            'temperature': sensor.data.temperature,
            'humidity': sensor.data.humidity,
            'pressure': sensor.data.pressure,
            'gas_resistance': sensor.data.gas_resistance
        }
    return None

# Example Usage
sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
configure_sensor(sensor)
data = read_sensor_data(sensor)
```

## Data Storage in Neo4j

### Setup Neo4j Connection
```python
from neo4j import GraphDatabase

class Neo4jConnection:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(
            uri, 
            auth=(user, password)
        )
    
    def close(self):
        self.driver.close()
```

### Store Sensor Data
```python
def store_reading(tx, reading):
    query = """
    CREATE (r:Reading {
        timestamp: datetime(),
        temperature: $temperature,
        humidity: $humidity,
        pressure: $pressure,
        gas_resistance: $gas_resistance
    })
    """
    tx.run(query, **reading)
```

## Continuous Monitoring

### Data Collection Loop
```python
import time
from datetime import datetime

def monitor_environment(sensor, db, interval=60):
    """Collect data at specified interval"""
    while True:
        try:
            # Read sensor
            reading = read_sensor_data(sensor)
            
            # Store in database
            if reading:
                with db.driver.session() as session:
                    session.write_transaction(
                        store_reading, 
                        reading
                    )
                print(f"Stored reading: {reading}")
            
            # Wait for next interval
            time.sleep(interval)
            
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)  # Wait before retry
```

## Data Validation

### Validate Readings
```python
def validate_reading(reading):
    """Validate sensor readings"""
    valid_ranges = {
        'temperature': (-40, 85),    # °C
        'humidity': (0, 100),         # %
        'pressure': (300, 1100),      # hPa
        'gas_resistance': (0, 50000)  # Ω
    }
    
    for key, (min_val, max_val) in valid_ranges.items():
        if key in reading:
            value = reading[key]
            if not min_val <= value <= max_val:
                return False
    return True
```

## Data Processing

### Calculate Air Quality
```python
def calculate_air_quality(gas_resistance):
    """Convert gas resistance to air quality score"""
    # Baseline calibration needed
    baseline = 50000  # Example baseline
    
    # Calculate air quality percentage
    quality = min(100, (gas_resistance / baseline) * 100)
    
    return quality
```

### Process Historical Data
```python
def get_historical_data(db, hours=24):
    query = """
    MATCH (r:Reading)
    WHERE r.timestamp > datetime() - duration('PT24H')
    RETURN r
    ORDER BY r.timestamp
    """
    
    with db.driver.session() as session:
        result = session.run(query)
        return [dict(record['r']) for record in result]
```

## Next Steps

Proceed to [AI Integration](ai-integration.md) to learn how to analyze this data using TensorRT-LLM.
