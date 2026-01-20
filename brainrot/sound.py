import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame

from . import queue

pygame.mixer.init(buffer=4096)

SOUND_PATH = "./sounds"

loaded_sounds = {}

def load_sounds():
	glob = Path(SOUND_PATH).glob("*.ogg")
	def load_sound(path):
		if path not in loaded_sounds:
				sound = {"sound": pygame.mixer.Sound(path), "name": path.stem}
				loaded_sounds[path] = sound
				print(f"loaded sound: {sound['name']}")
	for s in glob:
			queue.enqueue(200, lambda s=s: load_sound(s))

def queue_random_sound():
	def play_sound():
		try:
			sound = random.choice(list(loaded_sounds.values()))
			sound["sound"].play()
			print(f"played {sound['name']}")
		except IndexError:
			print("[error]: tried to play a sound, but no sounds loaded!", file=sys.stderr)
	queue.enqueue(100, play_sound)