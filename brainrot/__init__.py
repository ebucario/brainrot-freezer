"""starts and orchestrates the brainrot service"""

from pathlib import Path
import gpiozero

import sys

print("initializing brainrot...")

from . import queue
from . import sound
from . import signal

print("brainrot initialized.")

queue.spin()