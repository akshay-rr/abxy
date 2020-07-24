from datetime import datetime
from pymongo import MongoClient
import bson


class TaskDatabase:

	def __init__(self, db_string: str, db_name: str):
		# "mongodb+srv://test_user0:riktXHrvxRuVkS6F@cluster0.heb4n.mongodb.net/test?retryWrites=true&w=majority"
		self.client = MongoClient(db_string)
		self.db = self.client[db_name]
		self.userCollection = self.db['users']
		self.taskLogCollection = self.db['taskLog']

	def getUserObjectByEmailAndGoogleID(self, email: str, google_id: str):
		return self.userCollection.find_one({"email": email, "google_id": google_id})

	def getUserObjectByUserID(self, userID: bson.ObjectId):
		return self.userCollection.find_one({"_id": userID})

	def putNewUser(self, user):
		result = self.userCollection.insert_one(user)
		if result.acknowledged:
			return result.inserted_id
		return None

	def putNewTask(self, uid, task):
		result = self.userCollection.update_one({"_id": uid}, {"$push": {'tasks': task}})
		if result.acknowledged:
			return task['_id']
		return None

	def putNewBonus(self, uid, task_id, bonus):
		result = self.userCollection.update_one({"_id": uid, "tasks._id": task_id}, {"$push": {'tasks.$[].bonuses': bonus}})
		if result.acknowledged:
			return bonus['_id']
		return None
