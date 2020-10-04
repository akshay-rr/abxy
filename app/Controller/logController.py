from datetime import datetime
import dateutil.parser
import bson
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

		# print(logRequest['bonus_instances'])

		uid = bson.ObjectId(logRequest['uid'])
		task_id = bson.ObjectId(logRequest['task_id'])

		# get the task from DB
		task = self.taskDatabase.getTaskObjectByUserIDAndTaskID(uid, task_id)

		if task is None:
			return None

		# we're building this bonusLog to eventually be put into the taskLog db
		bonusLog = []

		# the actual list of all bonuses
		bonuses = task['bonuses']
		totalLogScoreAddition = 0.0

		timeOfLog = dateutil.parser.parse(logRequest['timestamp'])
		# timeOfLog = datetime.utcfromtimestamp(int(logRequest["timestamp"] / 1000))

		for i in range(len(bonuses)):
			bonusLog.append({})

			data = 0.0
			# source the data either from the logRequest or from system sources
			if bonuses[i]['data_source'] == "USER_INPUT":
				# get from logRequest
				for bonusDataInstance in logRequest['bonus_instances']:
					if str(bonusDataInstance['bonus_id']) == str(bonuses[i]['_id']):
						data = bonusDataInstance['input_quantity']
						break
			else:
				data = self.bonusController.getDataQuantity(uid, task_id, timeOfLog, bonuses[i])
				# print("DATA", data)
				if data is None:
					return None

			# calculate score addition, build bonus array
			bonusLog[i]['bonus_id'] = bonuses[i]['_id']
			bonusLog[i]['input_quantity'] = float(data)
			bonusLog[i]['score_addition'] = int(self.bonusController.computeScoreAddition(bonuses[i], bonusLog[i]['input_quantity']))
			if bonusLog[i]['score_addition'] is None:
				return None
			totalLogScoreAddition += bonusLog[i]['score_addition']
		# print("REACHED HERE")

		totalLogScore = int(task['base_score'] + totalLogScoreAddition)
		timeNow = datetime.now()

		# build taskLogObject
		taskLog = {'_id': bson.ObjectId(), 'uid': uid, 'task_id': task_id, 'timestamp': timeOfLog, 'bonus_instances': bonusLog, 'remarks': logRequest['remarks'], 'score': totalLogScore, 'server_time': timeNow}

		# update task last_done_on
		if self.taskDatabase.setTaskLastDone(uid, task_id, timeOfLog) is None:
			return None

		# print("REACHED HERE 1")
		# update user object score
		if self.taskDatabase.addToUserScore(uid, totalLogScore) is None:
			return None

		# print("REACHED HERE 2")
		# print(taskLog)

		# put Task Log in db
		if self.taskDatabase.putNewLog(taskLog) is None:
			return None

		return totalLogScore

	def deleteLog(self, deleteRequest):
		# Lookup the log, find the score, subtract from the user score, update the task last done, remove the log from the DB

		uid = bson.ObjectId(deleteRequest['uid'])
		log_id = bson.ObjectId(deleteRequest['log_id'])

		# Lookup the log
		taskLogObject = self.taskDatabase.getLogEntryByUserIDandLogID(uid, log_id)
		if taskLogObject is None:
			return None

		task_id = taskLogObject['task_id']

		# find the score
		scoreOfDeletedTask = taskLogObject['score']

		# remove user object score
		if self.taskDatabase.addToUserScore(uid, -scoreOfDeletedTask) is None:
			return None

		# remove the log from the DB
		if self.taskDatabase.deleteLogByID(log_id) is None:
			return None

		# update the task last done
		mostRecentLog = self.taskDatabase.getMostRecentLogByUserIDAndTaskID(uid, task_id)
		if mostRecentLog is None:
			if self.taskDatabase.setTaskLastDone(uid, task_id, datetime.fromtimestamp(0)) is None:
				return None
		else:
			if self.taskDatabase.setTaskLastDone(uid, task_id, mostRecentLog['timestamp']) is None:
				return None

		return "SUCCESS"

	def retrieveUserLogEntriesByFirebaseID(self, firebase_id):
		logs = self.taskDatabase.getLogEntriesByFirebaseID(firebase_id)
		user = self.taskDatabase.getUserObjectByFirebaseID(firebase_id)
		idToNameMap = {}
		idToCategoryMap = {}

		for task in user['tasks']:
			idToNameMap[task['_id']] = task['name']
			idToCategoryMap[task['_id']] = task['category']

		for i in range(len(logs)):
			logs[i]['task_name'] = idToNameMap[logs[i]['task_id']]
			logs[i]['task_category'] = idToCategoryMap[logs[i]['task_id']]

		return logs

	def appendLogEntries(self, userObject):
		userObject['task_log'] = self.retrieveUserLogEntriesByFirebaseID(userObject['firebase_id'])
		return userObject
