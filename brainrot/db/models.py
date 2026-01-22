import peewee as pw

from brainrot.db import BaseModel, UUIDModel
from brainrot.db.fields import PathField

class Sound(UUIDModel):
	"""a brainrot sound"""
	path = PathField(unique=True, index=True)
	playcount = pw.IntegerField(default=0)
	def __str__(self):
		return f"{self.__class__!s}(path={self.path}, playcount={self.playcount})"

class QueuedSound(BaseModel):
	"""brainrot sounds to try to play next, before others"""
	id = pw.AutoField() # use autofield for sorting
	sound = pw.ForeignKeyField(Sound)

class DiscordChannel(UUIDModel):
	"""a discord channel that is registered to for commands or audio files"""
	discord_id = pw.IntegerField(index=True,unique=True)

class DiscordToken(BaseModel):
	token = pw.TextField(primary_key=True)