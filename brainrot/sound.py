"""initializes sound engine and provides methods to play sounds"""

import sys
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
import random
from pathlib import Path
from typing import Dict

from brainrot.db.models import QueuedSound, Sound
from brainrot import queue

pygame.mixer.init(buffer=4096)
random.seed()

SOUND_PATH = "sounds"

_sound_cache: Dict[Sound, pygame.mixer.Sound] = {}

def _load_sounds_from_db():
	total_db = Sound.select().count()
	print(f"loading {total_db} sounds from database...")
	sounds = [s for s in Sound.select()]
	def task():
		try:
			sound = sounds.pop()
			_sound_cache[sound] = pygame.mixer.Sound(sound.path)
			queue.enqueue(200, task)
		except IndexError:
			print(f"finished loading sounds from database!")
	queue.enqueue(200, task)

def _scan_for_new_sounds():
	print(f"scanning for new sounds...")
	glob = list(Path(SOUND_PATH).glob("*.ogg"))
	total_files = len(glob)
	print(f"found {total_files} files...")
	def task():
		path = glob.pop()
		if Sound.get_or_none(Sound.path == path) is None:
			sound = Sound.create(path=path)
			_sound_cache[sound] = pygame.mixer.Sound(sound.path)
			print(f"saved new sound: {sound}")
		current = len(glob)
		if (total_files - current) % 100 == 0:
			print(f"{total_files - current} files scanned...")
		if current != 0:
			queue.enqueue(200, task)
		else:
			print(f"all files scanned!")
	queue.enqueue(200, task)

queue.enqueue(200, _load_sounds_from_db)
queue.enqueue(200, _scan_for_new_sounds)

def play_sound():
	sound = (QueuedSound.select().order_by(QueuedSound.id.desc())).first()
	if sound is None:
		sound = random.choice(list(_sound_cache.keys()))
	_sound_cache[sound].play()
	sound.playcount += 1
	sound.save()
	print(f"played {sound}")