# Dockerfile for pi_qled_oled_stats.py
# This Dockerfile is intended for running on a Raspberry Pi (ARM architecture)
# and assumes the OLED display is connected to the host Pi via I2C.

FROM python:3.11-slim

# Install system dependencies for I2C and required libraries
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        python3-dev \
        libfreetype6-dev \
        libjpeg-dev \
        zlib1g-dev \
        libopenjp2-7 \
        libtiff5 \
        libatlas-base-dev \
        i2c-tools \
        libffi-dev \
        libssl-dev \
        git \
        && rm -rf /var/lib/apt/lists/*

# Enable I2C device access (the device must be available on the host)
# This is typically done by running the container with --device=/dev/i2c-1

# Set workdir
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the script
COPY pi_oled_stats.py .

# Set the entrypoint
ENTRYPOINT ["python", "pi_oled_stats.py"]
