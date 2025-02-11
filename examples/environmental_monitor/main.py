#!/usr/bin/env python3

import bme680
import time
from neo4j import GraphDatabase
from datetime import datetime
from tensorrt_llm.runtime import ModelConfig, SamplingConfig
from tensorrt_llm.runtime import GenerationSession, Model

class EnvironmentalMonitor:
    def __init__(self, neo4j_uri, neo4j_user, neo4j_password, model_path):
        # Initialize BME680
        self.sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
        self.configure_sensor()
        
        # Initialize Neo4j
        self.driver = GraphDatabase.driver(
            neo4j_uri,
            auth=(neo4j_user, neo4j_password)
        )
        
        # Initialize TensorRT-LLM
        self.analyzer = self.setup_model(model_path)
        
    def configure_sensor(self):
        """Configure BME680 sensor"""
        self.sensor.set_humidity_oversample(bme680.OS_2X)
        self.sensor.set_pressure_oversample(bme680.OS_4X)
        self.sensor.set_temperature_oversample(bme680.OS_8X)
        self.sensor.set_filter(bme680.FILTER_SIZE_3)
        
    def setup_model(self, model_path):
        """Setup TensorRT-LLM model"""
        config = ModelConfig(
            max_batch_size=1,
            max_input_len=512,
            max_output_len=128
        )
        model = Model(model_path, config)
        return GenerationSession(model)
    
    def get_readings(self):
        """Get sensor readings"""
        if self.sensor.get_sensor_data():
            return {
                'temperature': self.sensor.data.temperature,
                'humidity': self.sensor.data.humidity,
                'pressure': self.sensor.data.pressure,
                'gas': self.sensor.data.gas_resistance,
                'timestamp': datetime.now()
            }
        return None
    
    def analyze_environment(self, readings):
        """Analyze environmental data using LLM"""
        prompt = f"""
        Analyze these environmental readings:
        Temperature: {readings['temperature']}°C
        Humidity: {readings['humidity']}%
        Pressure: {readings['pressure']}hPa
        Gas: {readings['gas']}Ω
        
        Provide:
        1. Current conditions assessment
        2. Health impact analysis
        3. Recommended actions
        """
        
        sampling_config = SamplingConfig(
            max_new_tokens=128,
            temperature=0.7
        )
        
        outputs = self.analyzer.generate(
            [prompt],
            sampling_config
        )
        
        return outputs[0]
    
    def store_data(self, readings, analysis):
        """Store data in Neo4j"""
        with self.driver.session() as session:
            session.run("""
            CREATE (r:Reading {
                temperature: $temperature,
                humidity: $humidity,
                pressure: $pressure,
                gas: $gas,
                timestamp: datetime($timestamp)
            })-[:HAS_ANALYSIS]->(a:Analysis {
                content: $analysis,
                timestamp: datetime($timestamp)
            })
            """, {
                **readings,
                'analysis': analysis
            })
    
    def run(self, interval=60):
        """Main monitoring loop"""
        try:
            while True:
                # Get readings
                readings = self.get_readings()
                if readings:
                    # Analyze data
                    analysis = self.analyze_environment(readings)
                    
                    # Store data
                    self.store_data(readings, analysis)
                    
                    print(f"Stored readings: {readings}")
                    print(f"Analysis: {analysis}\n")
                
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("Monitoring stopped")
            self.driver.close()

if __name__ == '__main__':
    monitor = EnvironmentalMonitor(
        neo4j_uri="bolt://localhost:7687",
        neo4j_user="neo4j",
        neo4j_password="password",
        model_path="optimized_model"
    )
    monitor.run()
