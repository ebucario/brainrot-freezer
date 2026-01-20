"""initializes sound engine and provides methods to play sounds"""

import sys
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
import random
from pathlib import Path

from . import queue
from .db import db

pygame.mixer.init(buffer=4096)
random.seed()

SOUND_PATH = "./sounds"

loaded_sounds = {}

if not isinstance(db.get("soundplays"), dict):
	db["soundplays"] = {}

def _load_sounds():
	glob = list(Path(SOUND_PATH).glob("*.ogg"))
	total = len(glob)
	print(f"loading {total} sounds...")
	def load_one_sound():
		path = glob.pop()
		if path not in loaded_sounds:
			sound = {"sound": pygame.mixer.Sound(path), "name": path.stem}
			loaded_sounds[path] = sound
		current = len(glob)
		if (total - current) % 100 == 0:
			print(f"{total - current} sounds loaded...")
		if current == 0:
			print(f"all sounds loaded!")
		else:
			queue.enqueue(200, load_one_sound)
	queue.enqueue(200, load_one_sound)

queue.enqueue(200, _load_sounds)

_try_play_next_queue = []

def queue_random_sound():
	def play_sound():
		try:
			if len(_try_play_next_queue) > 0:
				stem = _try_play_next_queue.pop()
				sound = next((i for i in loaded_sounds.values() if i["name"] == stem), random.choice(list(loaded_sounds.values())))
			else:
				sound = random.choice(list(loaded_sounds.values()))
			sound["sound"].play()
			db["soundplays"][sound['name']] = db["soundplays"].get(sound['name'], 0) + 1
			db.save()
			print(f"played {sound['name']}")
		except IndexError:
			print("[error]: tried to play a sound, but no sounds loaded!", file=sys.stderr)
	queue.enqueue(100, play_sound)

def try_play_next(stem):
	_try_play_next_queue.append(stem)
	print(f"trying to play {stem} next...")