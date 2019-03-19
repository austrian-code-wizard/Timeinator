from DAO.dao import DAO
from functools import wraps
from Models.models import User, Interval, Task
from datetime import datetime
from exceptions.exceptions import TimeinatorException

def handle_exceptions(func):
	@wraps(func)
	def execute(*args, **kwargs):
		try:
			result = func(*args, **kwargs)
			return result
		except TimeinatorException as e:
			return {"info": str(e)}
		except Exception as e:
			return {"info": "ooops, something went wrong"}
	return execute


class Businesslogic:

	def __init__(self):
		self.dao = DAO()

	@handle_exceptions
	def create_user(self, user_json):
		result = self.dao.insert_entity(user_json, User)
		return f"The user with the ID {result} was created successfully"

	@handle_exceptions
	def create_task(self, task_json):
		task_json["actual_time"] = 0
		result = self.dao.insert_entity(task_json, Task)
		return f"The task with the ID {result} was created successfully"

	@handle_exceptions
	def update_user(self, user_json, id):
		result = self.dao.update_entity(user_json, User, id)
		return f"The user with the id {result} was updated successfully"

	@handle_exceptions
	def update_interval(self, interval_json, id):
		result = self.dao.update_entity(interval_json, Interval, id)
		return f"The interval with the ID {result} was created successfully"

	@handle_exceptions
	def update_task(self, task_json, id):
		result = self.dao.update_entity(task_json, Task, id)
		return f"The task with the ID {result} was created successfully"

	@handle_exceptions
	def delete_user(self, id):
		if self.dao.get_nested_entities(id, User, "tasks") is []:
			raise TimeinatorException("Please remove this user from the tasks it is assigned to before deleting it.")
		else:
			result = self.dao.delete_entity(User, id)
			return f"The user with the ID {result} was deleted successfully"

	@handle_exceptions
	def delete_interval(self, id):
		result = self.dao.delete_entity(Interval, id)
		return f"The interval with the ID {result} was deleted successfully"

	@handle_exceptions
	def delete_task(self, id):
		result = self.dao.delete_entity(Task, id)
		return f"The task with the ID {result} was deleted successfully"

	@handle_exceptions
	def get_user_by_id(self, id):
		result = self.dao.get_entity(User, id)
		return result

	@handle_exceptions
	def get_users_for_task(self, id):
		result = self.dao.get_nested_entities(id, Task, "users")
		return result

	@handle_exceptions
	def get_interval_by_id(self, id):
		result = self.dao.get_entity(Interval, id)
		return result

	@handle_exceptions
	def get_task_by_id(self, id):
		result = self.dao.get_entity(Task, id)
		return result

	@handle_exceptions
	def get_task_by_id(self, id):
		result = self.dao.get_entity(Task, id)
		return result

	@handle_exceptions
	def start_interval(self, interval_json, task_ids, user_id):
		interval_id = self.dao.insert_entity(interval_json, Interval)
		for id in task_ids:
			found = False
			for user in self.dao.get_nested_entities(id, Task, "users"):
				if user["id"] == user_id:
					found = True
			if found is False:
				raise TimeinatorException(f"The user is not part of task {id}. Please add them to the task first.")
			result = self.dao.link_entities(interval_id, id, Interval, Task, "tasks")
			if result is False:
				self.dao.delete_entity(Interval, interval_id)
				raise TimeinatorException(f"Task with ID {id} not found")
		result = self.dao.link_entities(interval_id, user_id, Interval, User, "user", many=False)
		if result is False:
			self.dao.delete_entity(Interval, interval_id)
			raise TimeinatorException(f"User with id {user_id} not found")
		return f"The interval with the ID {interval_id} was created successfully"

	@handle_exceptions
	def stop_interval(self, id):
		interval = self.dao.get_entity(Interval, id)
		if interval["ended_at"] is not None:
			raise TimeinatorException("This interval was already ended")
		else:
			time_now = datetime.utcnow().isoformat()
			self.dao.update_entity({"ended_at": time_now}, Interval, id)
			tasks = self.dao.get_nested_entities(id, Interval, "tasks")
			interval = self.dao.get_entity(Interval, id)
			delta = (datetime.fromisoformat(interval["ended_at"])-datetime.fromisoformat(interval["created_at"])).total_seconds()
			for task in tasks:
				new_actual_time = task["actual_time"] + delta
				self.dao.update_entity({"actual_time": new_actual_time}, Task, task["id"])
			return f"Ended interval with ID {id}"

	@handle_exceptions
	def get_all_users(self):
		result = self.dao.get_all_entities(User)
		return result

	@handle_exceptions
	def get_all_tasks(self):
		result = self.dao.get_all_entities(Task)
		return result

	@handle_exceptions
	def get_intervals_for_user(self, user_id):
		result = self.dao.search_entity({"user_id": user_id}, Interval)
		return result

	@handle_exceptions
	def add_user_to_task(self, user_id, task_id):
		result = self.dao.link_entities(user_id, task_id, User, Task, "tasks")
		if result is True:
			return f"The user {user_id} is now working on task {task_id}"
		else:
			return f"This user cannot be added to that task"

	@handle_exceptions
	def remove_user_from_task(self, user_id, task_id):
		result = self.dao.unlink_entities(user_id, task_id, User, Task, "tasks")
		if result is True:
			return f"The user {user_id} is now not working on task {task_id} anymore"
		else:
			return f"This user cannot be removed from that task"

	@handle_exceptions
	def add_task_to_interval(self, interval_id, task_id):
		result = self.dao.link_entities(interval_id, task_id, Interval, Task, "tasks")
		if result is True:
			return f"The task {task_id} is now part of interval {interval_id}"
		else:
			return f"This task cannot be added to that interval"

	@handle_exceptions
	def remove_task_from_interval(self, interval_id, task_id):
		result = self.dao.unlink_entities(interval_id, task_id, Interval, Task, "tasks")
		if result is True:
			return f"The task {task_id} is now not part of interval {interval_id} anymore"
		else:
			return f"This task cannot be removed from that interval"






