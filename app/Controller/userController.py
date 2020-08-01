from Repositories.taskDatabase import TaskDatabase
from Controller.logController import LogController

class UserController:
	def __init__(self, tdb: TaskDatabase, lgc: LogController):
		self.taskDatabase = tdb
		self.logController = lgc

	def signInUser(self, signInRequest: dict):
		userAlreadyExists = self.taskDatabase.getUserObjectByEmailAndGoogleID(signInRequest['email'], signInRequest['google_id'])
		if userAlreadyExists is not None:
			return self.logController.appendLogEntries(userAlreadyExists)

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
			return self.logController.appendLogEntries.appendLogEntries(self.taskDatabase.getUserObjectByUserID(insertedID))
