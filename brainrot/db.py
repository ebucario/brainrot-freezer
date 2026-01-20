import json
from collections import UserDict

DB_PATH = "/app/brainrot/db.json"

class Db(UserDict):
	def __init__(self):
		self.data = {}
		try:
			with open(DB_PATH) as fp:
				data = json.load(fp)
				self.data.update(data)
		except (FileNotFoundError, json.decoder.JSONDecodeError):
			print(f"warning: no db file found at \"{DB_PATH}\". recreating db...")
			self.save()

	def __setitem__(self, key, item):
		self.data[key] = item
		self.save()

	def __delitem__(self, key):
		del self.data[key]
		self.save()
	
	def save(self):
		with open(DB_PATH, "w") as fp:
			s = json.dumps(self.data)
			fp.write(s)

db = Db()