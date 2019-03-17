from Models.models import User, Task, Interval
from Models.schema import UserSchema, TaskSchema, IntervalSchema

User.schema = UserSchema()
Task.schema = TaskSchema()
Interval.schema = IntervalSchema()