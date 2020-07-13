from Repositories.taskDatabase import TaskDatabase

class BonusController:
	def __init__(self,tdb):
		self.taskDatabase = tdb

	def createTimeBonus(self, name, type, multiplier, upper_bound, uid):
		return self.taskDatabase.createNewTimeBonus(name, type, multiplier, upper_bound, uid)

	def createRepeatBonus(self, name, frequency, upper_bound, uid):
		return self.taskDatabase.createNewRepeatBonus(name, frequency, upper_bound, uid)

	def createFocusBonus(self, name, type, lower_bound, distraction_penalty, uid):
		return self.taskDatabase.createNewFocusBonus(name, type, lower_bound, distraction_penalty, uid)

