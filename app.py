from pathlib import Path
import gpiozero
import random
import pygame
from time import sleep
import signal
import sys

exiting = False
def handler(_signal_number, _stack_frame):
    global exiting
    exiting = True
    sys.exit(0)

signal.signal(signal.SIGTERM, handler)

random.seed()

# pygame.mixer.init(buffer=16384)
pygame.mixer.init(buffer=4096)

print("loading sounds...")
sounds = [{"sound": pygame.mixer.Sound(s), "name": s.stem} for s in Path("./sounds").glob("*.ogg")]
print("sounds loaded.")

button = gpiozero.Button(2, bounce_time=0.1)

def when_released():
	sound = random.choice(sounds)
	sound["sound"].play()
	print(f"random sound: {sound['name']}")

button.when_released = when_released

while not exiting:
    sleep(0.1)

print("goodnight.")
