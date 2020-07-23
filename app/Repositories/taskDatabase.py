from datetime import datetime
from pymongo import MongoClient
import bson


# def userObjectToMap(user: User) -> map:
# 	return vars(user)
#
# def mapToUserObject(myMap: map) -> User:
# 	tasks = []
# 	for task in myMap['tasks']:
# 		bonuses = []
# 		for bonus in myMap['bonus']:
# 			bonuses.append(Bonus(myMap['_id'],task['_id'],bonus['data_souce'],bonus['bonus_name'],bonus['input_label'],bonus['upper_bound'],bonus['lower_bound'],bonus['evaluation_type'],bonus['constants'],bonus['created_on'],bonus['_id']))
# 		tasks.append(Task(myMap['_id'],task['name'],task['description'],task['base_score'],task['category'],task['_id'],task['tags'],bonuses,task['created_on'],task['last_done_on']))
# 	return User(myMap['name'],myMap['email'],myMap['google_id'],myMap['score'],myMap['_id'],tasks)

class TaskDatabase:

	def __init__(self, db_string: str, db_name: str):
		# "mongodb+srv://test_user0:riktXHrvxRuVkS6F@cluster0.heb4n.mongodb.net/test?retryWrites=true&w=majority"
		self.client = MongoClient(db_string)
		self.db = self.client[db_name]
		self.userCollection = self.db['users']
		self.taskLogCollection = self.db['taskLog']

	def getUserObjectByEmailAndGoogleID(self, email: str, google_id: str):
		userLookup = self.userCollection.find_one({"email": email, "google_id": google_id})
		if userLookup is not None:
			return userLookup
		return None

	def getUserObjectByUserID(self, userID: bson.ObjectId):
		userLookup = self.userCollection.find_one({"_id": userID})
		if userLookup is not None:
			return userLookup
		return None

	def putNewUser(self, user):
		user['tasks'] = []
		user['score'] = 0

		result = self.userCollection.insert_one(user)
		if result.acknowledged:
			return result.inserted_id
		return None
