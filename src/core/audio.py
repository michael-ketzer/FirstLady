import sys
import platform
import subprocess
from .logging import app_logger

def play_beep(frequency: int = 200, duration: int = 500):
    """Play a system beep sound
    
    Args:
        frequency: Beep frequency in Hz (Windows only)
        duration: Beep duration in milliseconds (Windows only)
    """
    try:
        system = platform.system()

        if system == "Windows":
            import winsound
            winsound.Beep(frequency, duration)

        elif system == "Darwin":  # macOS
            subprocess.run(["afplay", "/System/Library/Sounds/Ping.aiff"])  # Play default beep sound

        elif system == "Linux":
            try:
                subprocess.run(["aplay", "/usr/share/sounds/alsa/Front_Center.wav"], check=True)
            except FileNotFoundError:
                try:
                    subprocess.run(["play", "-nq", "-t", "alsa", "synth", str(duration / 1000), "sin", str(frequency)], check=True)
                except FileNotFoundError:
                    sys.stdout.write('\a')
                    sys.stdout.flush()

        else:
            sys.stdout.write('\a')
            sys.stdout.flush()

    except Exception as e:
        app_logger.error(f"Error playing beep: {e}")