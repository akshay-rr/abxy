from Repositories import TaskDatabase

class UserController:
	def __init__(self,tdb):
		self.taskDatabase = tdb
	
	def createUser(self,email, pwd):
		if self.taskDatabase.getUserIDByEmail(email)!=-1:
			# the user already exists!
			return -1
		return self.taskDatabase.createNewUser(email,pwd)

	def loginUser(self,email,pwd):
		uid = self.taskDatabase.getUserIDByEmail(email) 
		if uid==-1:
			return -1
		
		actualPassword=self.taskDatabase.getUserPasswordByID(uid)
		if actualPassword==-1:
			return -1
		if actualPassword!=pwd:
			return -1

		return uid