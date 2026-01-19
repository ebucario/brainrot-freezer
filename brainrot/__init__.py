from pathlib import Path
import gpiozero
import random
import signal
import sys
import os
from .  import queue

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame

SOUND_PATH = "./sounds"

class Brainrot:
    loaded_sounds = {}

    def __init__(self):
        queue.enqueue(0, self.initialize)
        queue.spin()
    
    def initialize(self):
        print("initializing brainrot...")
        random.seed()
        signal.signal(signal.SIGTERM, Brainrot.handle_sigterm)
        pygame.mixer.init(buffer=4096)
        self.button = gpiozero.Button(2, bounce_time=0.1)
        self.button.when_released = self.handle_button
        print("brainrot initialized.")
        queue.enqueue(200, self.load_sounds)
    
    def load_sounds(self):
        glob = Path(SOUND_PATH).glob("*.ogg")
        def load_sound(path):
            if path not in self.loaded_sounds:
                sound = {"sound": pygame.mixer.Sound(path), "name": path.stem}
                self.loaded_sounds[path] = sound
                print(f"loaded sound: {sound['name']}")
        for s in glob:
            queue.enqueue(200, lambda s=s: load_sound(s))
    
    def handle_sigterm(_signal_number, _stack_frame):
        sys.exit(0)
    
    def handle_button(self):
        def play_sound():
            try:
                sound = random.choice(list(self.loaded_sounds.values()))
                sound["sound"].play()
                print(f"played {sound['name']}")
            except IndexError:
                print("[error]: tried to play a sound, but no sounds loaded!", file=sys.stderr)
        queue.enqueue(100, play_sound)

Brainrot()