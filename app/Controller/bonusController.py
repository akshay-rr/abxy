from Repositories.taskDatabase import TaskDatabase

class BonusController:
	def __init__(self,tdb):
		self.taskDatabase = tdb

	def createTimeBonus(self, timeBonus):
		if self.taskDatabase.getUserByID(timeBonus.uid):
			return self.taskDatabase.putNewTimeBonus(timeBonus)
		print('User not found')
		return -1

	def createRepeatBonus(self, repeatBonus):
		if self.taskDatabase.getUserByID(repeatBonus.uid):
			return self.taskDatabase.putNewRepeatBonus(repeatBonus)
		print('User not found')
		return -1

	def createFocusBonus(self, focusBonus):
		if self.taskDatabase.getUserByID(focusBonus.uid):
			return self.taskDatabase.putNewFocusBonus(focusBonus)
		print('User not found')
		return -1

	def listBonusesByUID(self, uid):
		if self.taskDatabase.getUserByID(uid):
			return self.taskDatabase.getBonusesByUID(uid)
		print('User not found')
		return -1
