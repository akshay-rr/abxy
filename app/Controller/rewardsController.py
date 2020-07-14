import math

class RewardsController:

	def __init__(self, tdb):
		self.taskDatabase = tdb

	def calculateTimeBonus(self, taskEntry, taskObj):
		if taskObj:
			timeBonusObject = self.taskDatabase.getTimeBonusByIDandUID(
				taskObj.time_bonus_id, taskEntry.uid)
			# Calculation
			ans = 0
			# if timeBonusObject.type=='LOGARITHMIC':
			#     ans=timeBonusObject.upper_bound*(2.0/math.PI)*math.arctan(taskEntry.duration/taskObj.target_time-1))
			# elif timeBonusObject.type='ADDITIVE':
			#     ans=timeBonusObject.
			return ans
		return None

	def calculateRepeatBonus(self, taskEntry, taskObj):
		if taskObj:
			repeatBonusObject = self.taskDatabase.getRepeatBonusByIDandUID(
				taskObj.repeat_bonus_id, taskEntry.uid)
			# Calculation
			ans = 0
			return ans
		return None

	def calculateFocusBonus(self, taskEntry, taskObj):
		if taskObj:
			focusBonusObject = self.taskDatabase.getFocusBonusByIDandUID(
				taskObj.focus_bonus_id, taskEntry.uid)
			# Calculation
			ans = 0
			return ans
		return None

	def calculateScore(self, taskEntry):
		taskObj = self.taskDatabase.getTaskById(taskEntry.tid)
		baseScoreVal = taskObj.base_score
		timeBonusVal = self.calculateTimeBonus(taskEntry, taskObj)
		repeatBonusVal = self.calculateRepeatBonus(taskEntry, taskObj)
		focusBonusVal = self.calculateFocusBonus(taskEntry, taskObj)
		return baseScoreVal + timeBonusVal + repeatBonusVal + focusBonusVal
