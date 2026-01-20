from pathlib import Path
import gpiozero
import random
import signal
import sys

from . import queue
from . import sound

def initialize():
	print("initializing brainrot...")
	random.seed()
	signal.signal(signal.SIGTERM, Brainrot.handle_sigterm)
	
	print("brainrot initialized.")
	queue.enqueue(200, sound.load_sounds)

def handle_sigterm(_signal_number, _stack_frame):
	sys.exit(0)

queue.enqueue(0, initialize)
queue.spin()