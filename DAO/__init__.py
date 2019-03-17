from Database.database import DatabaseConnector
from functools import wraps
from Models.models import User

def execute_in_session(func):
	@wraps(func)
	def execute(*args, **kwargs):
		try:
			result = func(*args, **kwargs)
			args[0].session.commit()
			return result
		except Exception as e:
			args[0].session.rollback()
			raise e


class DAO():

	def __init__(self):
		self.db_connector = DatabaseConnector()
		self.session = self.db_connector.get_session()

	@execute_in_session
	def insert_user(self, user_json):
		self.session.add(User(name="moritz"))
		return True

	def update_user(self, user_json):
		pass

	def delete_user(self, user_id):
		pass

	def search_user(self, user_json):
		pass

	def insert_task(self, task_json):
		pass

	def update_task(self, task_json):
		pass

	def delete_task(self, task_id):
		pass

	def search_task(self, task_json):
		pass

	def insert_interval(self, interval_json):
		pass

	def update_interval(self, interval_json):
		pass

	def delete_interval(self, interval_id):
		pass

	def search_interval(self, interval_json):
		pass

	def add_task_to_user(self, task_id, user_id):
		pass

	def add_interval_to_user(self, interval_id, user_id):
		pass

	def add_task_to_interval(self, task_id, interval_id):
		pass

	def get_user(self, user_id):
		pass

	def get_task(self, task_id):
		pass

	def get_interval(self, interval_id):
		pass

