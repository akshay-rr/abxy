from Repositories.taskDatabase import TaskDatabase

class BonusController:
	def __init__(self,tdb):
		self.taskDatabase = tdb

	def createTimeBonus(self, name, type, multiplier, upper_bound, uid):
		if self.taskDatabase.getUserByID(uid):
			return self.taskDatabase.createNewTimeBonus(name, type, multiplier, upper_bound, uid)
		print('User not found')
		return -1

	def createRepeatBonus(self, name, frequency, upper_bound, uid):
		if self.taskDatabase.getUserByID(uid):
			return self.taskDatabase.createNewRepeatBonus(name, frequency, upper_bound, uid)
		print('User not found')
		return -1

	def createFocusBonus(self, name, type, lower_bound, distraction_penalty, uid):
		if self.taskDatabase.getUserByID(uid):
			return self.taskDatabase.createNewFocusBonus(name, type, lower_bound, distraction_penalty, uid)
		print('User not found')
		return -1
