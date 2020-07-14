from Entities.entities import *
from Repositories.taskDatabase import TaskDatabase


class UserController:
	def __init__(self, tdb: TaskDatabase):
		self.taskDatabase = tdb

	def createUser(self, user: User) -> int:
		if self.taskDatabase.getUserIDByEmail(user.email) != -1:
			# the user already exists!
			return -1
		return self.taskDatabase.putNewUser(user)

	def loginUser(self, user: User) -> int:
		uid = self.taskDatabase.getUserIDByEmail(user.email)
		if uid == -1:
			return -1

		actualPassword = self.taskDatabase.getUserPasswordByID(uid)
		if actualPassword == -1:
			return -1
		if actualPassword != user.password:
			return -1

		return uid
