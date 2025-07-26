# Pi QLED OLED Stats

Display real-time IP address, CPU usage, and disk usage on a 128x32 OLED display connected to a Raspberry Pi 5.

## Features
- Shows local IP address
- Displays CPU and disk usage
- Designed for SSD1306-based 128x32 OLED via I2C
- Runs as a Python script or in a Docker container


## Hardware Requirements
- Raspberry Pi (any model with I2C support)
- 128x32 OLED display (SSD1306, I2C interface)
- I2C enabled on the Pi (`raspi-config` > Interface Options > I2C)

## Pinout Connection (SSD1306 128x32 OLED I2C)

| OLED Pin | Raspberry Pi Pin | Physical Pin | Notes           |
|----------|------------------|--------------|-----------------|
| GND      | GND              | 6            | Ground          |
| VCC      | 3.3V or 5V       | 1 or 2       | Power           |
| SCL      | SCL (GPIO 3)     | 5            | I2C Clock       |
| SDA      | SDA (GPIO 2)     | 3            | I2C Data        |

> **Note:** Most SSD1306 OLEDs work with 3.3V or 5V, but check your display specs.

## Software Requirements
- Raspberry Pi OS (or compatible Linux)
- Python 3.8+
- Docker & Docker Compose (for containerized usage)

## Setup (Native Python)

1. **Clone the repository:**
   ```sh
   git clone https://github.com/peiminggu/pi5-oled-stats.git
   cd pi5-oled-stats
   ```
2. **Enable I2C on your Pi:**
   ```sh
   sudo raspi-config
   # Interface Options > I2C > Enable
   sudo reboot
   ```
3. **Install dependencies:**
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
4. **Run the script:**
   ```sh
   python pi_oled_stats.py
   ```

## Setup (Docker)

1. **Enable I2C on your Pi:**
   ```sh
   sudo raspi-config
   # Interface Options > I2C > Enable
   sudo reboot
   ```
2. **Install Docker and Docker Compose:**
   ```sh
   sudo apt-get update
   sudo apt-get install -y docker.io docker-compose
   sudo usermod -aG docker $USER
   # Log out and back in for group changes to take effect
   ```
3. **Build and run with Docker Compose:**
   ```sh
   cd pi-qled
   docker-compose up --build
   ```
   - The container will access the I2C device and display stats on the OLED.
   - To run in the background:
     ```sh
     docker-compose up -d
     ```

## Notes
- The container must be run with `--device=/dev/i2c-1` and `--privileged` to access the OLED hardware.
- If you see permission errors, ensure your user is in the `docker` group and I2C is enabled.
- The script logs errors to the console for troubleshooting.

## Stopping the Application
- **Native:** Press `Ctrl+C` in the terminal.
- **Docker:**
  ```sh
  docker-compose down
  ```

## License
MIT
