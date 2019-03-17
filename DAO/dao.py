from Database.database import DatabaseConnector
from functools import wraps
from datetime import datetime


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
	return execute


class DAO:

	def __init__(self):
		self.db_connector = DatabaseConnector()
		self.session = self.db_connector.get_session()

	@execute_in_session
	def insert_entity(self, entity_json, entity_class):
		model, errors = entity_class.schema.load(entity_json)
		model.created_at = datetime.utcnow()
		merged_model = self.session.merge(model)
		self.session.commit()
		return merged_model.id

	@execute_in_session
	def update_entity(self, entity_json, entity_class, id):
		model, errors = entity_class.schema.load(entity_json)
		model.id = id
		merged_model = self.session.merge(model)
		self.session.commit()
		return merged_model.id

	@execute_in_session
	def delete_entity(self, entity_class, id):
		model = self.session.query(entity_class).filter(entity_class.id == id).first()
		self.session.delete(model)
		return id

	@execute_in_session
	def get_entity(self, entity_class, id):
		model = self.session.query(entity_class).filter(entity_class.id == id).first()
		return entity_class.schema.dump(model)[0]

	@execute_in_session
	def search_entity(self, entity_json, entity_class):
		model, errors = entity_class.schema.load(entity_json)
		query = self.session.query(entity_class)
		for column_object in entity_class.__table__.columns:
			column = column_object.description
			if hasattr(model, column):
				value = getattr(model, column)
				if value is not None:
					query = query.filter(getattr(entity_class, column) == value)
		results = query.all()
		results_json = []
		for result in results:
			json_model, errors = entity_class.schema.dump(result)
			results_json.append(json_model)
		return results_json

	@execute_in_session
	def get_all_entities(self, entity_class):
		entities = self.session.query(entity_class).all()
		results_json = []
		for result in entities:
			json_model, errors = entity_class.schema.dump(result)
			results_json.append(json_model)
		return results_json

	@execute_in_session
	def link_entities(self, id_1, id_2, class_1, class_2, key, many=True):
		entity_1 = self.session.query(class_1).filter(class_1.id == id_1).first()
		entity_2 = self.session.query(class_2).filter(class_2.id == id_2).first()
		if entity_1 is None or entity_2 is None:
			return False
		if many is False:
			setattr(entity_1, key, entity_2)
		else:
			entity_list = getattr(entity_1, key)
			entity_list.append(entity_2)
			setattr(entity_1, key, entity_list)
		return True

	@execute_in_session
	def unlink_entities(self, id_1, id_2, class_1, class_2, key, many=True):
		entity_1 = self.session.query(class_1).filter(class_1.id == id_1).first()
		entity_2 = self.session.query(class_2).filter(class_2.id == id_2).first()
		if entity_1 is None or entity_2 is None:
			return False
		if many is False:
			setattr(entity_1, key, None)
		else:
			entity_list = getattr(entity_1, key)
			entity_list.remove(entity_2)
			setattr(entity_1, key, entity_list)
		return True

	@execute_in_session
	def get_nested_entities(self, entity_id, entity_class, attribute_name):
		entity = self.session.query(entity_class).filter(entity_class.id == entity_id).first()
		json_results = []
		for result in getattr(entity, attribute_name):
			json_result, errors = result.__class__.schema.dump(result)
			json_results.append(json_result)
		return json_results
