from Repositories.taskDatabase import TaskDatabase
from Controller.logController import LogController
from datetime import datetime


def convert_all_dates_to_strings(myObject):
	if isinstance(myObject, dict):
		keys = myObject.keys()
		for key in keys:
			myObject[key] = convert_all_dates_to_strings(myObject[key])
	elif isinstance(myObject, list):
		for i in range(len(myObject)):
			myObject[i] = convert_all_dates_to_strings(myObject[i])
	elif isinstance(myObject, datetime):
		return myObject.isoformat()
	return myObject


class UserController:
	def __init__(self, tdb: TaskDatabase, lgc: LogController):
		self.taskDatabase = tdb
		self.logController = lgc

	def fetchCurrentActiveUserByAccessToken(self, accessToken):
		return self.taskDatabase.getActiveUser(accessToken)

	def registerNewUserAndReturnData(self, signInRequest: dict):
		userObjectKeysFromSignInRequest = ["name", "email", "firebase_id"]
		userObject = {}
		for key in userObjectKeysFromSignInRequest:
			userObject[key] = signInRequest[key]

		userObject['tasks'] = []
		userObject['rewards'] = []
		userObject['score'] = 0
		insertedID = self.taskDatabase.putNewUser(userObject)
		if insertedID is None:
			return "INSERT FAILURE"
		else:
			return self.fetchLatestUserWithoutArchivedTasksByFirebaseID(userObject['firebase_id'])

	def fetchLatestUserWithLogEntriesByFirebaseId(self, firebase_id):
		return self.logController.appendLogEntries(self.taskDatabase.getUserObjectByFirebaseID(firebase_id))

	def fetchLatestUserWithoutArchivedTasksByFirebaseID(self, firebase_id):
		user = self.fetchLatestUserWithLogEntriesByFirebaseId(firebase_id)
		not_archived_tasks = [task for task in user['tasks'] if ('archived' not in task) or (not task['archived'])]
		user = convert_all_dates_to_strings(user)

		user['tasks'] = not_archived_tasks
		return user
