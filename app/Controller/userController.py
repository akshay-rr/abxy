from Repositories.taskDatabase import TaskDatabase


class UserController:
	def __init__(self, tdb: TaskDatabase):
		self.taskDatabase = tdb

	def signInUser(self, user: dict):
		userAlreadyExists = self.taskDatabase.getUserObjectByEmailAndGoogleID(user['email'], user['google_id'])
		if userAlreadyExists is not None:
			return userAlreadyExists

		insertedID = self.taskDatabase.putNewUser(user)
		print(insertedID)
		print(type(insertedID))
		if insertedID is None:
			return "INSERT FAILURE"
		else:
			return self.taskDatabase.getUserObjectByUserID(insertedID)

# def loginUser(self, user: User) -> int:
# 	uid = self.taskDatabase.getUserIDByEmail(user.email)
# 	if uid == -1:
# 		return -1
#
# 	actualPassword = self.taskDatabase.getUserPasswordByID(uid)
# 	if actualPassword == -1:
# 		return -1
# 	if actualPassword != user.password:
# 		return -1
#
# 	return uid
