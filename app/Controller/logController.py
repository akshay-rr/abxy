from datetime import datetime

from Repositories.taskDatabase import TaskDatabase
from Controller.bonusController import BonusController


class LogController:
	def __init__(self, tdb: TaskDatabase, bc: BonusController):
		self.taskDatabase = tdb
		self.bonusController = bc

	def logTask(self, logRequest) -> int:
		# logRequest has a uid, task_id, a remarks field, and a list of bonuses, where each bonus is a json object(dict) with a number and json id

		# get the task from DB
		# loop through each bonus, source the data either from the logRequest or from system sources
		# loop through each bonus with filled data, calculate score addition, build bonus array
		# update task last_done_one
		# update user score
		# add to log

		uid = logRequest['uid']
		task_id = logRequest['task_id']

		# get the task from DB
		task = self.taskDatabase.getTaskObjectByUserIDAndTaskID(uid, task_id)

		if task is None:
			return None

		# we're building this bonusLog to eventually be put into the taskLog db
		bonusLog = []

		# the actual list of all bonuses
		bonuses = task['bonuses']
		totalLogScoreAddition = 0.0

		for i in range(len(bonuses)):
			bonusLog.append({})

			data = 0.0
			# source the data either from the logRequest or from system sources
			if bonuses[i]['data_source'] == "USER_INPUT":
				# get from logRequest
				for bonusDataInstance in logRequest['bonus_instances']:
					if str(bonusDataInstance['bonus_id']) == str(bonuses[i]['_id']):
						data = bonusDataInstance['data']
						break
			else:
				data = self.bonusController.getDataQuantity(uid, task_id, bonuses[i])
				if data is None:
					return None

			# calculate score addition, build bonus array
			bonusLog[i]['bonus_id'] = bonuses[i]['_id']
			bonusLog[i]['input_quantity'] = data
			bonusLog[i]['score_addition'] = self.bonusController.computeScoreAddition(bonuses[i], bonusLog[i]['input_quantity'])
			if bonusLog[i]['score_addition'] is None:
				return None
			totalLogScoreAddition += bonusLog[i]['score_addition']

		totalLogScore = task['base_score'] + totalLogScoreAddition
		timeNow = datetime.now()

		# build taskLogObject
		taskLog = {'uid': uid, 'task_id': task_id, 'timestamp': timeNow, 'bonus_instances': bonusLog, 'remarks': logRequest['remarks'], 'score': totalLogScore}

		# update task last_done_on
		if self.taskDatabase.setTaskLastDone(uid, task_id, timeNow) is None:
			return None

		# update user object score
		if self.taskDatabase.addToUserScore(uid, totalLogScore) is None:
			return None

		# put Task Log in db
		if self.taskDatabase.putNewLog(taskLog) is None:
			return None

		return totalLogScore
