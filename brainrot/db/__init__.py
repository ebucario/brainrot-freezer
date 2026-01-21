from uuid import uuid4
import peewee as pw

db = pw.SqliteDatabase("./db.sqlite")

class BaseModel(pw.Model):
	class Meta:
		database = db

class UUIDModel(BaseModel):
	id = pw.UUIDField(primary_key=True, default=uuid4)

from brainrot.db.models import *
db.connect()
db.create_tables([Sound, DiscordChannel, DiscordToken, QueuedSound])