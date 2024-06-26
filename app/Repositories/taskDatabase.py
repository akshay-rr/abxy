from datetime import datetime
import pymongo
from pymongo import MongoClient
import bson


# import pymongo
# from pymongo import MongoClient
# import bson
# client = MongoClient("mongodb+srv://admin_user:Brskol8pZbhZwcec@cluster0.j34k4.mongodb.net/test?retryWrites=true&w=majority")
# db = client['test']


class TaskDatabase:

	def __init__(self, db_string: str, db_name: str):
		self.client = MongoClient(db_string)
		self.db = self.client[db_name]
		self.userCollection = self.db['users']
		self.taskLogCollection = self.db['taskLog']
		self.activeSessionCollection = self.db['activeSessions']
		self.rewardLogCollection = self.db['rewardLog']

	def getUserObjectByEmailAndGoogleID(self, email: str, google_id: str):
		return self.userCollection.find_one({"email": email, "google_id": google_id})

	def getUserObjectByUserID(self, userID: bson.ObjectId):
		return self.userCollection.find_one({"_id": userID})

	def getUserObjectByFirebaseID(self, firebase_id: str):
		return self.userCollection.find_one({"firebase_id": firebase_id})

	def getTaskObjectByUserIDAndTaskID(self, userID: bson.ObjectId, taskID: bson.ObjectId):
		user = self.userCollection.find_one({"_id": userID})
		for task in user['tasks']:
			if str(task['_id']) == str(taskID):
				return task
		return None

	def getTaskObjectByFirebaseIDAndTaskID(self, firebase_id, task_id):
		user = self.userCollection.find_one({"firebase_id": firebase_id})
		for task in user['tasks']:
			if str(task['_id']) == str(task_id):
				return task
		return None

	def getRewardObjectByFirebaseIDAndRewardID(self, firebase_id, reward_id):
		user = self.userCollection.find_one({"firebase_id": firebase_id})
		for task in user['rewards']:
			if str(task['_id']) == str(reward_id):
				return task
		return None

	def putNewUser(self, user):
		result = self.userCollection.insert_one(user)
		if result.inserted_id is not None:
			return result.inserted_id
		return None

	def putNewTask(self, uid, task):
		result = self.userCollection.update_one({"_id": uid}, {"$push": {'tasks': task}})
		if result.matched_count > 0:
			return task['_id']
		return None

	def putNewTaskByFirebaseID(self, firebase_id, task):
		result = self.userCollection.update_one({"firebase_id": firebase_id}, {"$push": {'tasks': task}})
		if result.matched_count > 0:
			return task['_id']
		return None

	def putNewRewardByFirebaseID(self, firebase_id, reward):
		result = self.userCollection.update_one({"firebase_id": firebase_id}, {"$push": {'rewards': reward}})
		if result.matched_count > 0:
			return reward['_id']
		return None

	def putNewBonus(self, uid, task_id, bonus):
		result = self.userCollection.update_one({"_id": uid}, {"$push": {'tasks.$[xyz].bonuses': bonus}}, array_filters=[{"xyz._id": task_id}])
		if result.matched_count > 0:
			return bonus['_id']
		return None

	def putNewBonusByFirebaseID(self, firebase_id, task_id, bonus):
		result = self.userCollection.update_one({"firebase_id": firebase_id}, {"$push": {'tasks.$[xyz].bonuses': bonus}}, array_filters=[{"xyz._id": task_id}])
		if result.matched_count > 0:
			return bonus['_id']
		return None

	def putNewPenaltyByFirebaseID(self, firebase_id, reward_id, penalty):
		result = self.userCollection.update_one({"firebase_id": firebase_id}, {"$push": {'rewards.$[xyz].penalties': penalty}}, array_filters=[{"xyz._id": reward_id}])
		if result.matched_count > 0:
			return penalty['_id']
		return None

	def putNewLog(self, taskLog):
		result = self.taskLogCollection.insert_one(taskLog)
		if result.inserted_id is not None:
			return result.inserted_id
		return None

	def putNewRewardLog(self, rewardLog):
		result = self.rewardLogCollection.insert_one(rewardLog)
		if result.inserted_id is not None:
			return result.inserted_id
		return None

	def deleteLogByID(self, log_id: bson.ObjectId):
		return self.taskLogCollection.find_one_and_delete({"_id": log_id})

	def deleteRewardLogByID(self, reward_log_id: bson.ObjectId):
		return self.rewardLogCollection.find_one_and_delete({"_id": reward_log_id})

	def setTaskLastDone(self, uid: bson.ObjectId, task_id: bson.ObjectId, time):
		result = self.userCollection.update_one({"_id": uid, "tasks._id": task_id}, {"$set": {"tasks.$.last_done_on": time}})
		if result.matched_count > 0:
			return time
		return None

	def setTaskLastDoneByFirebaseID(self, firebase_id: str, task_id: bson.ObjectId, time):
		result = self.userCollection.update_one({"firebase_id": firebase_id, "tasks._id": task_id}, {"$set": {"tasks.$.last_done_on": time}})
		if result.matched_count > 0:
			return time
		return None

	def setRewardLastDoneByFirebaseID(self, firebase_id: str, reward_id: bson.ObjectId, time):
		result = self.userCollection.update_one({"firebase_id": firebase_id, "rewards._id": reward_id}, {"$set": {"rewards.$.last_done_on": time}})
		if result.matched_count > 0:
			return time
		return None

	def addToUserScore(self, uid, addition):
		result = self.userCollection.update_one({"_id": uid}, {"$inc": {"score": addition}})
		if result.matched_count > 0:
			return addition
		return None

	def addToUserScoreByFirebaseID(self, firebase_id, addition):
		result = self.userCollection.update_one({"firebase_id": firebase_id}, {"$inc": {"score": addition}})
		if result.matched_count > 0:
			return addition
		return None

	def getMostRecentLogByUserIDAndTaskID(self, uid, task_id):
		return self.taskLogCollection.find_one({'uid': uid, "task_id": task_id}, sort=[('timestamp', pymongo.DESCENDING)])

	def getMostRecentLogByFirebaseIDAndTaskID(self, firebase_id, task_id):
		return self.taskLogCollection.find_one({'firebase_id': firebase_id, "task_id": task_id}, sort=[('timestamp', pymongo.DESCENDING)])

	def getMostRecentRewardLogByFirebaseIDAndTaskID(self, firebase_id, reward_id):
		return self.rewardLogCollection.find_one({'firebase_id': firebase_id, "reward_id": reward_id}, sort=[('timestamp', pymongo.DESCENDING)])

	def getLogEntriesByUid(self, uid):
		return list(self.taskLogCollection.find({'uid': uid}))

	def getLogEntriesByFirebaseID(self, firebase_id):
		return list(self.taskLogCollection.find({'firebase_id': firebase_id}))

	def getRewardLogEntriesByFirebaseID(self, firebase_id):
		return list(self.rewardLogCollection.find({'firebase_id': firebase_id}))

	def putActiveUser(self, accessToken, uid):
		result = self.activeSessionCollection.insert_one({"access_token": accessToken, "uid": uid})
		if result.inserted_id is not None:
			return result.inserted_id
		return None

	def getActiveUser(self, accessToken):
		return self.activeSessionCollection.find_one({"access_token": accessToken})['uid']

	def eraseActiveUser(self, accessToken):
		return self.activeSessionCollection.find_one_and_delete({"access_token": accessToken})

	def archiveTaskByUIDAndTaskID(self, uid, task_id):
		return self.userCollection.update_one({'_id': uid}, {"$set": {"tasks.$[xyz].archived": True}}, array_filters=[{"xyz._id": task_id}])

	def archiveTaskByFirebaseIDAndTaskID(self, firebase_id, task_id):
		return self.userCollection.update_one({'firebase_id': firebase_id}, {"$set": {"tasks.$[xyz].archived": True}}, array_filters=[{"xyz._id": task_id}])

	def archiveRewardByFirebaseIDAndTaskID(self, firebase_id, reward_id):
		return self.userCollection.update_one({'firebase_id': firebase_id}, {"$set": {"rewards.$[xyz].archived": True}}, array_filters=[{"xyz._id": reward_id}])

	def getLogEntryByUserIDandLogID(self, uid, logID):
		return self.taskLogCollection.find_one({'uid': uid, "_id": logID})

	def getLogEntryByFirebaseIDandLogID(self, firebase_id, logID):
		return self.taskLogCollection.find_one({'firebase_id': firebase_id, "_id": logID})

	def getRewardLogEntryByFirebaseIDandLogID(self, firebase_id, rewardLogID):
		return self.rewardLogCollection.find_one({'firebase_id': firebase_id, "_id": rewardLogID})
