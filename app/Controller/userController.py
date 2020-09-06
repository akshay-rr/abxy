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

	def signInUser(self, accessToken, uid):
		return self.taskDatabase.putActiveUser(accessToken, uid)

	def signInUserAndReturnData(self, signInRequest: dict):
		userAlreadyExists = self.taskDatabase.getUserObjectByEmailAndGoogleID(signInRequest['email'], signInRequest['google_id'])
		if userAlreadyExists is not None:
			self.signInUser(signInRequest['access_token'], userAlreadyExists['_id'])
			return self.logController.appendLogEntries(self.fetchLatestUserWithoutArchivedTasks(userAlreadyExists['_id']))

		userObjectKeysFromSignInRequest = ["name", "email", "google_id"]
		userObject = {}
		for key in userObjectKeysFromSignInRequest:
			userObject[key] = signInRequest[key]

		userObject['tasks'] = []
		userObject['score'] = 0
		insertedID = self.taskDatabase.putNewUser(userObject)
		if insertedID is None:
			return "INSERT FAILURE"
		else:
			self.signInUser(signInRequest['access_token'], insertedID)
			return self.fetchLatestUserWithoutArchivedTasks(insertedID)

	def fetchLatestUser(self, uid):
		return self.logController.appendLogEntries(self.taskDatabase.getUserObjectByUserID(uid))

	def fetchLatestUserWithoutArchivedTasks(self, uid):
		user = self.fetchLatestUser(uid)
		# print(user)
		# print(convert_all_dates_to_strings(user))
		not_archived_tasks = [task for task in user['tasks'] if ('archived' not in task) or (not task['archived'])]
		user = convert_all_dates_to_strings(user)

		user['tasks'] = not_archived_tasks
		return user

	def signOutUser(self, signOutRequest):
		return self.taskDatabase.eraseActiveUser(signOutRequest['access_token'])
