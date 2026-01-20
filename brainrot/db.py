import json
from collections import UserDict

DB_PATH = "/app/db.json"

class Db(UserDict):
	def __init__(self):
		self.data = {}
		try:
			with open(DB_PATH) as fp:
				data = json.load(fp)
				self.data.update(data)
		except (FileNotFoundError, json.decoder.JSONDecodeError):
			print(f"warning: no db file found at \"{DB_PATH}\". recreating db...")
			self._save()

	def __setitem__(self, key, item):
		self.data[key] = item
		self._save()

	def __delitem__(self, key):
		del self.data[key]
		self._save()
	
	def _save(self):
		with open(DB_PATH, "w") as fp:
			s = json.dumps(self.data)
			fp.write(s)

db = Db()