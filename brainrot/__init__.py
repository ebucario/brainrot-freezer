"""starts and orchestrates the brainrot service"""

print("initializing brainrot...")

from . import queue
from . import sound
from . import signal
from . import button

print("brainrot initialized.")

queue.spin()