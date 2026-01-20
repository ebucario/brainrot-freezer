"""initializes sound engine and provides methods to play sounds"""

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
import random
from pathlib import Path

from . import queue

pygame.mixer.init(buffer=4096)
random.seed()

SOUND_PATH = "./sounds"

loaded_sounds = {}

def _load_sounds():
	glob = list(Path(SOUND_PATH).glob("*.ogg"))
	total = len(glob)
	print(f"loading {total} sounds...")
	def load_one_sound():
		path = glob.pop()
		if path not in loaded_sounds:
			sound = {"sound": pygame.mixer.Sound(path), "name": path.stem}
			loaded_sounds[path] = sound
			# print(f"loaded sound: {sound['name']}")
		current = len(glob)
		if (total - current) % 100 == 0:
			print(f"{total - current} sounds loaded...")
		if current == 0:
			print(f"all sounds loaded!")
		else:
			queue.enqueue(200, load_one_sound)
	queue.enqueue(200, load_one_sound)

queue.enqueue(200, _load_sounds)

def queue_random_sound():
	def play_sound():
		try:
			sound = random.choice(list(loaded_sounds.values()))
			sound["sound"].play()
			print(f"played {sound['name']}")
		except IndexError:
			print("[error]: tried to play a sound, but no sounds loaded!", file=sys.stderr)
	queue.enqueue(100, play_sound)