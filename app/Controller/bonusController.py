import math
from datetime import datetime
import bson

from Repositories.taskDatabase import TaskDatabase


class BonusController:
	def __init__(self, tdb: TaskDatabase):
		self.taskDatabase = tdb

	@staticmethod
	def computeScoreAddition(bonus, data):
		constants = bonus['constants']
		if bonus['evaluation_type'] == "LIN":
			return round(constants[0] * data)
		elif bonus['evaluation_type'] == "SIG":
			return round(constants[0] * math.tanh(data / (constants[1] / 2)))

	@staticmethod
	def hourDistanceIsOne(early: datetime, late: datetime):
		if early.date() == late.date():
			return late.hour - early.hour <= 1 and early.hour <= late.hour

		delta = late.date() - early.date()
		if delta.days == 1:
			return early.hour == 23 and late.hour == 0

		return False

	@staticmethod
	def dateDistanceIsOne(early: datetime, late: datetime):
		delta = late.date() - early.date()
		return 1 >= delta.days >= 0

	@staticmethod
	def isoYearHas53Weeks(isoYear: int):
		g = lambda y: math.floor((y - 100) / 400) - math.floor((y - 102) / 400)
		h = lambda y: math.floor((y - 200) / 400) - math.floor((y - 199) / 400)
		f = lambda y: 5 * y + 12 - 4 * (math.floor(y / 100) - math.floor(y / 400)) + g(y) + h(y)
		return f(isoYear) < 5

	@staticmethod
	def weekDistanceIsOne(early: datetime, late: datetime):
		earlyiso = early.isocalendar()
		lateiso = late.isocalendar()
		if earlyiso[0] == lateiso[0]:
			return lateiso[1] - earlyiso[1] <= 1 and earlyiso[1] <= lateiso[1]
		elif earlyiso[0] == (lateiso[0] - 1):
			return lateiso[1] == 1 and earlyiso[1] == 52 + (BonusController.isoYearHas53Weeks(earlyiso[0]))

	@staticmethod
	def monthDistanceIsOne(early: datetime, late: datetime):
		return (early.year == late.year and early.month <= late.month and late.month - early.month <= 1) or (
				early.year == (late.year - 1) and early.month == 12 and late.month == 1)

	@staticmethod
	def yearDistanceIsOne(early: datetime, late: datetime):
		return late.year >= early.year and late.year - early.year <= 1

	@staticmethod
	def isTimeRepeat(oldTime, newTime, frequency):

		print(oldTime)
		print(newTime)

		if frequency == "HOURLY":
			return BonusController.hourDistanceIsOne(oldTime, newTime)
		elif frequency == "DAILY":
			return BonusController.dateDistanceIsOne(oldTime, newTime)
		elif frequency == "WEEKLY":
			return BonusController.weekDistanceIsOne(oldTime, newTime)
		elif frequency == "MONTHLY":
			return BonusController.monthDistanceIsOne(oldTime, newTime)
		elif frequency == "YEARLY":
			return BonusController.yearDistanceIsOne(oldTime, newTime)
		else:
			return False

	def createBonus(self, bonusCreationRequest):
		bonusObject = {}
		firebase_id = bonusCreationRequest['firebase_id']
		task_id = bonusCreationRequest['task_id']

		bonusObjectKeysFromRequest = ["data_source", "bonus_name", "input_label", "upper_bound", "lower_bound", "evaluation_type", "constants"]
		for key in bonusObjectKeysFromRequest:
			bonusObject[key] = bonusCreationRequest[key]

		bonusObject['_id'] = bson.ObjectId()
		bonusObject['created_on'] = datetime.now()

		return self.taskDatabase.putNewBonusByFirebaseID(firebase_id, task_id, bonusObject)

	def createPenalty(self, penaltyCreationRequest):
		penaltyObject = {}
		firebase_id = penaltyCreationRequest['firebase_id']
		reward_id = penaltyCreationRequest['reward_id']

		penaltyObjectKeysFromRequest = ["data_source", "penalty_name", "input_label", "upper_bound", "lower_bound", "evaluation_type", "constants"]
		for key in penaltyObjectKeysFromRequest:
			penaltyObject[key] = penaltyCreationRequest[key]

		penaltyObject['_id'] = bson.ObjectId()
		penaltyObject['created_on'] = datetime.now()

		return self.taskDatabase.putNewPenaltyByFirebaseID(firebase_id, reward_id, penaltyObject)

	def getDataQuantity(self, firebase_id, task_id, logTimestamp, bonus):
		if bonus['data_source'] == "REPETITION":
			# get the most recent taskLog with the same uid,tid
			mostRecentLog = self.taskDatabase.getMostRecentLogByFirebaseIDAndTaskID(firebase_id, task_id)
			if mostRecentLog is None:
				return 0
			for bonusInstance in mostRecentLog['bonus_instances']:
				# check the input value for the same bonus
				if bonusInstance['bonus_id'] == bonus['_id']:
					if BonusController.isTimeRepeat(mostRecentLog['timestamp'], logTimestamp, bonus['input_label']):
						return float(bonusInstance['input_quantity'] + 1)
					else:
						return 0
		return 0

	def getDataQuantityForReward(self, firebase_id, reward_id, logTimestamp, penalty):
		if penalty['data_source'] == "REPETITION":
			# get the most recent taskLog with the same uid,tid
			mostRecentLog = self.taskDatabase.getMostRecentRewardLogByFirebaseIDAndTaskID(firebase_id, reward_id)
			if mostRecentLog is None:
				return 0
			for penaltyInstance in mostRecentLog['penalty_instances']:
				# check the input value for the same bonus
				if penaltyInstance['penalty_id'] == penalty['_id']:
					if BonusController.isTimeRepeat(mostRecentLog['timestamp'], logTimestamp, penalty['input_label']):
						return float(penaltyInstance['input_quantity'] + 1)
					else:
						return 0
		return 0
