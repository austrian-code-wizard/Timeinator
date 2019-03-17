from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()

users_tasks = Table("users_tasks", Base.metadata,
					Column("user_id", Integer, ForeignKey("user.id")),
					Column("task_id", Integer, ForeignKey("task.id")))

tasks_intervals = Table("tasks_intervals", Base.metadata,
						Column("task_id", Integer, ForeignKey("task.id")),
						Column("interval_id", Integer, ForeignKey("interval.id")))

class User(Base):
	"""
	User model
	"""

	__tablename__ = 'user'

	id = Column(Integer, primary_key=True, autoincrement=True)
	name = Column(String)
	password = Column(String)
	description = Column(String)
	email = Column(String)
	created_at = Column(DateTime(timezone=True))
	total_seconds = Column(Integer, default=0)

	intervals = relationship("Interval", back_populates="user")
	tasks = relationship("Task", secondary=users_tasks, back_populates="users")

class Interval(Base):
	"""
	Interval model
	"""

	__tablename__ = 'interval'

	id = Column(Integer, primary_key=True, autoincrement=True)
	created_at = Column(DateTime(timezone=True))
	ended_at = Column(DateTime(timezone=True))
	description = Column(String)
	device = Column(String)
	location = Column(String)
	user_id = Column(ForeignKey("user.id"))
	user = relationship("User", uselist=False, back_populates="intervals")
	tasks = relationship("Task", secondary=tasks_intervals, back_populates="intervals")

class Task(Base):
	"""
	Task model
	"""

	__tablename__ = 'task'

	id = Column(Integer, primary_key=True, autoincrement=True)
	name = Column(String)
	description = Column(String)
	created_at = Column(DateTime(timezone=True))
	estimated_done_by = Column(DateTime)
	actual_done_by = Column(DateTime)
	estimated_time = Column(Integer)
	actual_time = Column(Integer)
	intervals = relationship("Interval", secondary=tasks_intervals, back_populates="tasks")
	users = relationship("User", secondary=users_tasks, back_populates="tasks")

