from Repositories.taskDatabase import TaskDatabase


class UserController:
	def __init__(self, tdb: TaskDatabase):
		self.taskDatabase = tdb

	def signInUser(self, signInRequest: dict):
		userAlreadyExists = self.taskDatabase.getUserObjectByEmailAndGoogleID(signInRequest['email'], signInRequest['google_id'])
		if userAlreadyExists is not None:
			return userAlreadyExists

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
			return self.taskDatabase.getUserObjectByUserID(insertedID)
