from datetime import datetime
import bson

from Repositories.taskDatabase import TaskDatabase


class BonusController:
	def __init__(self, tdb: TaskDatabase):
		self.taskDatabase = tdb

	def createBonus(self, bonusCreationRequest):
		bonusObject = {}
		uid = bonusCreationRequest['uid']
		task_id = bonusCreationRequest['task_id']

		bonusObjectKeysFromRequest = ["data_source", "bonus_name", "input_label", "upper_bound", "lower_bound", "evaluation_type", "constants"]
		for key in bonusObjectKeysFromRequest:
			bonusObject[key] = bonusCreationRequest[key]

		bonusObject['_id'] = bson.ObjectId()
		bonusObject['created_on'] = datetime.now()

		return self.taskDatabase.putNewBonus(uid, task_id, bonusObject)
