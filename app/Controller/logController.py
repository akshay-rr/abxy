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

		firebase_id = logRequest['firebase_id']
		task_id = bson.ObjectId(logRequest['task_id'])

		# get the task from DB
		task = self.taskDatabase.getTaskObjectByFirebaseIDAndTaskID(firebase_id, task_id)

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
				data = self.bonusController.getDataQuantity(firebase_id, task_id, timeOfLog, bonuses[i])
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
		taskLog = {'_id': bson.ObjectId(), 'firebase_id': firebase_id, 'task_id': task_id, 'timestamp': timeOfLog, 'bonus_instances': bonusLog, 'remarks': logRequest['remarks'], 'score': totalLogScore, 'server_time': timeNow}

		# update task last_done_on
		if self.taskDatabase.setTaskLastDoneByFirebaseID(firebase_id, task_id, timeOfLog) is None:
			return None

		# print("REACHED HERE 1")
		# update user object score
		if self.taskDatabase.addToUserScoreByFirebaseID(firebase_id, totalLogScore) is None:
			return None

		# print("REACHED HERE 2")
		# print(taskLog)

		# put Task Log in db
		if self.taskDatabase.putNewLog(taskLog) is None:
			return None

		return totalLogScore

	def deleteLog(self, deleteRequest):
		# Lookup the log, find the score, subtract from the user score, update the task last done, remove the log from the DB

		firebase_id = deleteRequest['firebase_id']
		log_id = bson.ObjectId(deleteRequest['log_id'])

		# Lookup the log
		taskLogObject = self.taskDatabase.getLogEntryByFirebaseIDandLogID(firebase_id, log_id)
		if taskLogObject is None:
			return None

		task_id = taskLogObject['task_id']

		# find the score
		scoreOfDeletedTask = taskLogObject['score']

		# remove user object score
		if self.taskDatabase.addToUserScoreByFirebaseID(firebase_id, -scoreOfDeletedTask) is None:
			return None

		# remove the log from the DB
		if self.taskDatabase.deleteLogByID(log_id) is None:
			return None

		# update the task last done
		mostRecentLog = self.taskDatabase.getMostRecentLogByFirebaseIDAndTaskID(firebase_id, task_id)
		if mostRecentLog is None:
			if self.taskDatabase.setTaskLastDoneByFirebaseID(firebase_id, task_id, datetime.fromtimestamp(0)) is None:
				return None
		else:
			if self.taskDatabase.setTaskLastDoneByFirebaseID(firebase_id, task_id, mostRecentLog['timestamp']) is None:
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

	def retrieveUserRewardLogEntriesByFirebaseID(self, firebase_id):
		logs = self.taskDatabase.getRewardLogEntriesByFirebaseID(firebase_id)
		user = self.taskDatabase.getUserObjectByFirebaseID(firebase_id)
		idToNameMap = {}
		idToCategoryMap = {}

		for reward in user['rewards']:
			idToNameMap[reward['_id']] = reward['name']
			idToCategoryMap[reward['_id']] = reward['category']

		for i in range(len(logs)):
			logs[i]['reward_name'] = idToNameMap[logs[i]['reward_id']]
			logs[i]['reward_category'] = idToCategoryMap[logs[i]['reward_id']]

		return logs

	def appendLogEntries(self, userObject):
		userObject['task_log'] = self.retrieveUserLogEntriesByFirebaseID(userObject['firebase_id'])
		userObject['reward_log'] = self.retrieveUserRewardLogEntriesByFirebaseID(userObject['firebase_id'])
		return userObject

	def logReward(self, logRequest) -> int:
		# logRequest has a uid, task_id, a remarks field, and a list of bonuses, where each bonus is a json object(dict) with a number and json id

		# get the task from DB
		# loop through each bonus, source the data either from the logRequest or from system sources
		# loop through each bonus with filled data, calculate score addition, build bonus array
		# update task last_done_one
		# update user score
		# add to log

		# print(logRequest['bonus_instances'])

		firebase_id = logRequest['firebase_id']
		reward_id = bson.ObjectId(logRequest['reward_id'])

		# get the task from DB
		reward = self.taskDatabase.getRewardObjectByFirebaseIDAndRewardID(firebase_id, reward_id)

		if reward is None:
			return None

		# we're building this bonusLog to eventually be put into the taskLog db
		penaltyLog = []

		# the actual list of all bonuses
		penalties = reward['penalties']
		totalLogScoreSubtraction = 0.0

		timeOfLog = dateutil.parser.parse(logRequest['timestamp'])
		# timeOfLog = datetime.utcfromtimestamp(int(logRequest["timestamp"] / 1000))

		for i in range(len(penalties)):
			penaltyLog.append({})

			data = 0.0
			# source the data either from the logRequest or from system sources
			if penalties[i]['data_source'] == "USER_INPUT":
				# get from logRequest
				for rewardDataInstance in logRequest['penalty_instances']:
					if str(rewardDataInstance['penalty_id']) == str(penalties[i]['_id']):
						data = rewardDataInstance['input_quantity']
						break
			else:
				data = self.bonusController.getDataQuantityForReward(firebase_id, reward_id, timeOfLog, penalties[i])
				# print("DATA", data)
				if data is None:
					return None

			# calculate score addition, build bonus array
			penaltyLog[i]['penalty_id'] = penalties[i]['_id']
			penaltyLog[i]['input_quantity'] = float(data)
			penaltyLog[i]['score_addition'] = int(self.bonusController.computeScoreAddition(penalties[i], penaltyLog[i]['input_quantity']))
			if penaltyLog[i]['score_addition'] is None:
				return None
			totalLogScoreSubtraction += penaltyLog[i]['score_addition']
		# print("REACHED HERE")

		totalLogCost = -1*int(reward['base_cost'] + totalLogScoreSubtraction)
		timeNow = datetime.now()

		# build taskLogObject
		rewardLog = {'_id': bson.ObjectId(), 'firebase_id': firebase_id, 'reward_id': reward_id, 'timestamp': timeOfLog, 'penalty_instances': penaltyLog, 'remarks': logRequest['remarks'], 'cost': totalLogCost, 'server_time': timeNow}

		# update task last_done_on
		if self.taskDatabase.setRewardLastDoneByFirebaseID(firebase_id, reward_id, timeOfLog) is None:
			return None

		# print("REACHED HERE 1")
		# update user object score
		if self.taskDatabase.addToUserScoreByFirebaseID(firebase_id, totalLogCost) is None:
			return None

		# print("REACHED HERE 2")
		# print(taskLog)

		# put Task Log in db
		if self.taskDatabase.putNewRewardLog(rewardLog) is None:
			return None

		return totalLogCost

	def deleteRewardLog(self, deleteRequest):
		# Lookup the log, find the score, subtract from the user score, update the task last done, remove the log from the DB

		firebase_id = deleteRequest['firebase_id']
		reward_log_id = bson.ObjectId(deleteRequest['reward_log_id'])

		# Lookup the log
		rewardLogObject = self.taskDatabase.getRewardLogEntryByFirebaseIDandLogID(firebase_id, reward_log_id)
		if rewardLogObject is None:
			return None

		reward_id = rewardLogObject['reward_id']

		# find the score
		scoreOfDeletedReward = rewardLogObject['cost']

		# remove user object score
		if self.taskDatabase.addToUserScoreByFirebaseID(firebase_id, -scoreOfDeletedReward) is None:
			return None

		# remove the log from the DB
		if self.taskDatabase.deleteRewardLogByID(reward_log_id) is None:
			return None

		# update the task last done
		mostRecentRewardLog = self.taskDatabase.getMostRecentRewardLogByFirebaseIDAndTaskID(firebase_id, reward_id)
		if mostRecentRewardLog is None:
			if self.taskDatabase.setRewardLastDoneByFirebaseID(firebase_id, reward_id, datetime.fromtimestamp(0)) is None:
				return None
		else:
			if self.taskDatabase.setRewardLastDoneByFirebaseID(firebase_id, reward_id, mostRecentRewardLog['timestamp']) is None:
				return None

		return "SUCCESS"
