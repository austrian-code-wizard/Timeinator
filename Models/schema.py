from marshmallow import fields, Schema, post_load
from Models.models import User, Task, Interval


class IntervalSchema(Schema):

	id = fields.Integer(dump_only=True)
	created_at = fields.DateTime(dump_only=True)
	ended_at = fields.DateTime()
	description = fields.String()
	device = fields.String()
	location = fields.String()
	user_id = fields.Integer()

	@post_load
	def init_model(self, data):
		return Interval(**data)

class TaskSchema(Schema):
	id = fields.Integer(dump_only=True)
	name = fields.String()
	description = fields.String()
	created_at = fields.DateTime(dump_only=True)
	estimated_done_by = fields.DateTime()
	actual_done_by = fields.DateTime()
	estimated_time = fields.Integer()
	actual_time = fields.Integer()

	@post_load
	def init_model(self, data):
		return Task(**data)

class UserSchema(Schema):
	id = fields.Integer(dump_only=True)
	name = fields.String()
	password = fields.String()
	created_at = fields.DateTime(dump_only=True)
	description = fields.String()
	email = fields.String()
	total_seconds = fields.Integer()

	@post_load
	def init_model(self, data):
		return User(**data)
