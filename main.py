from datetime import datetime
from flask import Flask, jsonify, request
from functools import wraps
from Businesslogic.businesslogic import Businesslogic

def process_response(func):
	@wraps(func)
	def execute(*args, **kwargs):
		result = func(*args, **kwargs)
		if isinstance(result, dict) and "info" in result.keys():
			if result["info"] == "ooops, something went wrong":
				return jsonify(result), 500
			else:
				return jsonify(result), 404
		else:
			return jsonify(result), 200
	return execute

app = Flask(__name__)

businesslogic = Businesslogic()


@app.route("/create-user", methods=["POST"])
@process_response
def create_user():
	user = request.json
	return businesslogic.create_user(user)

@app.route("/create-task", methods=["POST"])
@process_response
def create_task():
	task = request.json
	return businesslogic.create_task(task)

@app.route("/start-interval", methods=["POST"])
@process_response
def start_interval():
	json_request = request.json
	return businesslogic.start_interval(json_request["interval"], json_request["task_ids"], json_request["user_id"])

@app.route("/stop-interval/<int:interval_id>", methods=["GET"])
@process_response
def stop_interval(interval_id):
	return businesslogic.stop_interval(interval_id)

@app.route("/update-user", methods=["POST"])
@process_response
def update_user():
	user = request.json
	return businesslogic.update_user(user)

@app.route("/update-task", methods=["POST"])
@process_response
def update_task():
	task = request.json
	return businesslogic.update_task(task)

@app.route("/update-interval", methods=["POST"])
@process_response
def update_interval():
	interval = request.json
	return businesslogic.update_interval(interval)

@app.route("/delete-user/<int:user_id>", methods=["DELETE"])
@process_response
def delete_user(user_id):
	return businesslogic.delete_user(user_id)

@app.route("/delete-task/<int:task_id>", methods=["DELETE"])
@process_response
def delete_task(task_id):
	return businesslogic.delete_task(task_id)

@app.route("/delete-interval/<int:interval_id>", methods=["DELETE"])
@process_response
def delete_interval(interval_id):
	return businesslogic.delete_interval(interval_id)

@app.route("/get-user-by-id/<int:user_id>", methods=["GET"])
@process_response
def get_user_by_id(user_id):
	return businesslogic.get_user_by_id(user_id)

@app.route("/get-interval-by-id/<int:interval_id>", methods=["GET"])
@process_response
def get_interval_by_id(interval_id):
	return businesslogic.get_interval_by_id(interval_id)

@app.route("/get-task-by-id/<int:task_id>", methods=["GET"])
@process_response
def get_task_by_id(task_id):
	return businesslogic.get_task_by_id(task_id)

@app.route("/get-all-users", methods=["GET"])
@process_response
def get_all_users():
	return businesslogic.get_all_users()

@app.route("/get-all-tasks", methods=["GET"])
@process_response
def get_all_tasks():
	return businesslogic.get_all_tasks()

@app.route("/get-users-for-task/<int:id>", methods=["GET"])
@process_response
def get_user_for_task(id):
	return businesslogic.get_users_for_task(id)

@app.route("/get-intervals-for-user/<int:user_id>", methods=["GET"])
@process_response
def get_intervals_for_user(user_id):
	return businesslogic.get_intervals_for_user(user_id)

@app.route("/add-user-to-task/<int:user_id>/<int:task_id>", methods=["GET"])
@process_response
def add_user_to_task(user_id, task_id):
	return businesslogic.add_user_to_task(user_id, task_id)

@app.route("/remove-user-from-task/<int:user_id>/<int:task_id>", methods=["GET"])
@process_response
def remove_user_from_task(user_id, task_id):
	return businesslogic.remove_user_from_task(user_id, task_id)

@app.route("/add-task-to-interval/<int:interval_id>/<int:task_id>", methods=["GET"])
@process_response
def add_task_to_interval(interval_id, task_id):
	return businesslogic.add_task_to_interval(interval_id, task_id)

@app.route("/remove-task-from-interval/<int:interval_id>/<int:task_id>", methods=["GET"])
@process_response
def remove_task_from_interval(interval_id, task_id):
	return businesslogic.remove_task_from_interval(interval_id, task_id)

if __name__ == '__main__':
	app.run(debug=False, port=5000, host='0.0.0.0')
