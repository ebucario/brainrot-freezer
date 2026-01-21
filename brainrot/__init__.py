"""starts and orchestrates the brainrot service"""

print("initializing brainrot...")

from brainrot import queue
from brainrot import sound
from brainrot import signal
from brainrot import button
from brainrot import discord

print("brainrot initialized.")

queue.spin()