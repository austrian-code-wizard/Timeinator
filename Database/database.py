from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Models.models import Base

class DatabaseConnector():

	def __init__(self):
		self.session = None
		self.engine = create_engine("sqlite:///timeinator.db")
		Base.metadata.create_all(self.engine)
		self.sessionmaker = sessionmaker(bind=self.engine)

	def get_session(self):
		if self.session is None:
			self.session = self.sessionmaker()
		return self.session