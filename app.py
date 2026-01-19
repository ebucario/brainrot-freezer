from pathlib import Path
import gpiozero
import random
from time import sleep
import signal
import sys
import os
import threading
import queue
from dataclasses import dataclass, field
from typing import Any

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame

SOUND_PATH = "./sounds"

@dataclass(order=True)
class Task:
    priority: int
    task: Any=field(compare=False)

class Brainrot:
    loaded_sounds = {}
    queue = queue.PriorityQueue()
    # convention: items are (priority, callable)
    # p0 is critical
    # p100 is UI (e.g. button actions)
    # p200 is background (e.g. loading sounds)

    def __init__(self):
        self.queue.put(Task(0, self.initialize))
        while True:
            t = self.queue.get()
            t.task()
            self.queue.task_done()
    
    def initialize(self):
        print("initializing brainrot...")
        random.seed()
        signal.signal(signal.SIGTERM, Brainrot.handle_sigterm)
        pygame.mixer.init(buffer=4096)
        self.button = gpiozero.Button(2, bounce_time=0.1)
        self.button.when_released = self.handle_button
        print("brainrot initialized.")
        self.queue.put(Task(200, self.load_sounds))
    
    def load_sounds(self):
        glob = Path(SOUND_PATH).glob("*.ogg")
        def load_sound(path):
            if path not in self.loaded_sounds:
                sound = {"sound": pygame.mixer.Sound(path), "name": path.stem}
                self.loaded_sounds[path] = sound
                print(f"loaded sound: {sound['name']}")
        for s in glob:
            self.queue.put(Task(200, lambda s=s: load_sound(s)))
    
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
        self.queue.put(Task(100, play_sound))

Brainrot()

# print("loading sounds...")
# sounds = [ for s in Path(SOUND_PATH).glob("*.ogg")]
# print("sounds loaded.")

# print("goodnight.")
