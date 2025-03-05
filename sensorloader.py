from neo4j import GraphDatabase
import bme680
import smbus2
import time

# Set up the Neo4j driver
uri = "neo4j+s://bXXX8.databases.neo4j.io"
driver = GraphDatabase.driver(uri, auth=("neo4j", "_eM6sXXXXXX85G1koVAzc"))

# Set up the BME680 sensor on bus 7
i2c_bus = smbus2.SMBus(7)
sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY, i2c_device=i2c_bus)

# Configure the sensor
sensor.set_humidity_oversample(bme680.OS_2X)
sensor.set_pressure_oversample(bme680.OS_4X)
sensor.set_temperature_oversample(bme680.OS_8X)
sensor.set_filter(bme680.FILTER_SIZE_3)
sensor.set_gas_heater_temperature(320)
sensor.set_gas_heater_duration(150)
sensor.select_gas_heater_profile(0)

# Define a function to create a sensor reading node in Neo4j
def create_sensor_reading(tx, temperature, humidity, pressure, gas):
    tx.run("CREATE (:SensorReading {temperature: $temperature, humidity: $humidity, pressure: $pressure, gas: $gas, timestamp: $timestamp})",
           temperature=temperature, humidity=humidity, pressure=pressure, gas=gas, timestamp=int(time.time()))

# Generate and insert sensor readings into Neo4j every 5 seconds
try:
    print("Starting BME680 sensor monitoring...")

    # Allow sensor to stabilize
    time.sleep(2)

    while True:
        # Force reading of sensor data
        sensor.get_sensor_data()

        # Get readings
        temperature = round(sensor.data.temperature, 2)
        humidity = round(sensor.data.humidity, 2)
        pressure = round(sensor.data.pressure, 2)

        # Check if gas data is available
        if sensor.data.heat_stable:
            gas = round(sensor.data.gas_resistance, 2)
        else:
            gas = None

        print(f"Reading - Temp: {temperature}°C, Humidity: {humidity}%, Pressure: {pressure}hPa, Gas: {gas} Ohms")

        # Store in Neo4j
        with driver.session() as session:
            session.execute_write(create_sensor_reading, temperature, humidity, pressure, gas)
            print("Data inserted into Neo4j")

        time.sleep(5)

except KeyboardInterrupt:
    print("\nStopping sensor monitoring")
except Exception as e:
    print(f"Error: {e}")
finally:
    driver.close()
    print("Neo4j connection closed")
