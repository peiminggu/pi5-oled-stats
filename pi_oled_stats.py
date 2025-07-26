"""
Display IP address, CPU usage, and disk usage on a 128x32 OLED for Raspberry Pi.
"""
import time
import logging
import psutil
from PIL import Image, ImageDraw, ImageFont
import Adafruit_SSD1306
import socket


def get_ip_address() -> str:
    """Get the local IP address of the Raspberry Pi."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception as e:
        logging.error(f"Failed to get IP address: {e}")
        return "N/A"


def get_cpu_usage() -> float:
    """Get the current CPU usage percentage."""
    try:
        return psutil.cpu_percent(interval=1)
    except Exception as e:
        logging.error(f"Failed to get CPU usage: {e}")
        return 0.0


def get_disk_usage() -> float:
    """Get the current disk usage percentage for root."""
    try:
        return psutil.disk_usage("/").percent
    except Exception as e:
        logging.error(f"Failed to get disk usage: {e}")
        return 0.0


def setup_logging(level: str = "INFO") -> None:
    """Configure logging for the application."""
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )


def main() -> None:
    """Main loop to display stats on the OLED display."""
    setup_logging()
    RST = None  # on PiOLED this pin isn't used
    try:
        disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)
        disp.begin()
        disp.clear()
        disp.display()
    except Exception as e:
        logging.error(f"Failed to initialize OLED display: {e}")
        return

    width = disp.width
    height = disp.height
    image = Image.new("1", (width, height))
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()

    while True:
        try:
            draw.rectangle((0, 0, width, height), outline=0, fill=0)
            ip = get_ip_address()
            cpu = get_cpu_usage()
            disk = get_disk_usage()
            draw.text((0, 0), f"IP: {ip}", font=font, fill=255)
            draw.text((0, 10), f"CPU: {cpu:.1f}%", font=font, fill=255)
            draw.text((0, 20), f"Disk: {disk:.1f}%", font=font, fill=255)
            disp.image(image)
            disp.display()
            time.sleep(2)
        except KeyboardInterrupt:
            disp.clear()
            disp.display()
            break
        except Exception as e:
            logging.error(f"Error in main loop: {e}")
            time.sleep(2)


if __name__ == "__main__":
    main()
