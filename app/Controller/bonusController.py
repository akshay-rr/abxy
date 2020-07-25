import math
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

	def getDataQuantity(self, uid, task_id, bonus):
		if bonus['data_source'] == "REPETITION":
			# get the most recent taskLog with the same uid,tid
			mostRecentLog = self.taskDatabase.getMostRecentLogByUserIDAndTaskID(uid, task_id)
			for bonusInstance in mostRecentLog['bonus_instances']:
				# check the input value for the same bonus
				if bonusInstance['bonus_id'] == bonus['_id']:
					return float(bonusInstance['input_quantity'] + 1)
		return None

	def computeScoreAddition(self, bonus, data):
		constants = bonus['constants']
		if bonus['evaluation_type'] == "ADDITIVE":
			return round(constants[0] * data)
		elif bonus['evaluation_type'] == "SIGMOID":
			return round(constants[0] * math.tanh(data / (constants[1] / 2)))
