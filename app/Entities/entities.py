from datetime import datetime
from bson import objectid

# TODO: make a UserFromAPI, UserFromDatabase, etc
class User:
	def __init__(self, name: str, email: str, google_id: str, score=-1, _id=objectid.ObjectId(), tasks=None):
		if tasks is None:
			tasks = []
		self._id = _id
		self.name = name
		self.email = email
		self.google_id = google_id
		self.score = score
		self.tasks = tasks


class Task:
	def __init__(self, uid: objectid.ObjectId, name: str, description: str, base_score: int, category: str, _id=objectid.ObjectId(), tags=None, bonuses=None, created_on=datetime.now(), last_done_on=datetime.now()):
		if tags is None:
			tags = []

		if bonuses is None:
			bonuses = []

		self.uid = uid

		self._id = _id
		self.name = name
		self.description = description
		self.tags = tags
		self.base_score = base_score
		self.category = category
		self.bonuses = bonuses
		self.created_on = created_on
		self.last_done_on = last_done_on


class Bonus:
	def __init__(self, uid: objectid.ObjectId, tid: objectid.ObjectId, data_source: str, bonus_name: str, input_label: str, upper_bound: float, lower_bound: float, evaluation_type: str, constants: list, created_on=datetime.now(), _id=objectid.ObjectId()):
		self.uid = uid
		self.tid = tid
		self.data_source = data_source
		self.bonus_name = bonus_name
		self.input_label = input_label
		self.upper_bound = upper_bound
		self.lower_bound = lower_bound
		self.evaluation_type = evaluation_type
		self.constants = constants
		self.created_on = created_on
		self._id = _id


class TaskLogEntry:
	def __init__(self, uid: objectid.ObjectId, tid: objectid.ObjectId, bonus_instances: list, remarks: str, score=None, _id=objectid.ObjectId(), t=datetime.now()):
		self.uid = uid
		self.tid = tid
		self.bonus_instances = bonus_instances
		self.remarks = remarks
		self.score = score
		self._id = _id
		self.timestamp = t

class BonusInstance:
	def __init__(self, task_instance_id: objectid.ObjectId, bonus_id: objectid.ObjectId, input_quantity: float, score_addition: int):
		self.task_instance_id = task_instance_id
		self.bonus_id=bonus_id
		self.input_quantity = input_quantity
		self.score_addition = score_addition