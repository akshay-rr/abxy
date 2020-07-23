# from Entities.entities import *
# from Repositories.taskDatabase import TaskDatabase
#
#
# class BonusController:
# 	def __init__(self, tdb: TaskDatabase):
# 		self.taskDatabase = tdb
#
# 	def createTimeBonus(self, timeBonus: TimeBonus) -> int:
# 		if self.taskDatabase.getUserByID(timeBonus.uid) != -1:
# 			return self.taskDatabase.putNewTimeBonus(timeBonus)
# 		print('User not found')
# 		return -1
#
# 	def createRepeatBonus(self, repeatBonus: RepeatBonus) -> int:
# 		if self.taskDatabase.getUserByID(repeatBonus.uid) != -1:
# 			return self.taskDatabase.putNewRepeatBonus(repeatBonus)
# 		print('User not found')
# 		return -1
#
# 	def createFocusBonus(self, focusBonus: FocusBonus) -> int:
# 		if self.taskDatabase.getUserByID(focusBonus.uid) != -1:
# 			return self.taskDatabase.putNewFocusBonus(focusBonus)
# 		print('User not found')
# 		return -1
#
# 	def listBonusesByUID(self, uid: int) -> int:
# 		if self.taskDatabase.getUserByID(uid) != -1:
# 			return self.taskDatabase.getBonusesByUID(uid)
# 		print('User not found')
# 		return -1
