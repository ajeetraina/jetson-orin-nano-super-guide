FROM python:3.9-slim

WORKDIR /app

# Install required system dependencies
RUN apt-get update && apt-get install -y \
    i2c-tools \
    python3-smbus \
    libgpiod2 \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
RUN pip install --no-cache-dir \
    neo4j \
    bme680 \
    smbus2

# Copy your script
COPY sensorloader.py .

# Run the script
CMD ["python", "sensorloader.py"]
