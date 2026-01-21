from pathlib import Path
import peewee as pw

class PathField(pw.Field):
	field_type = 'varchar'

	def db_value(self, value: Path):
		return str(value)
	
	def python_value(self, value):
		return Path(value)