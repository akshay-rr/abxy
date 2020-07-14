from math import floor

from Entities.entities import *
from Repositories.taskDatabase import TaskDatabase
from Controller.rewardsController import RewardsController
from datetime import *


class TaskLogController:
	def __init__(self, tdb: TaskDatabase, rc: RewardsController):
		self.taskDatabase = tdb
		self.rewardsController = rc

	@staticmethod
	def dateDistanceIsOne(early: datetime, late: datetime):
		delta = late.date() - early.date()
		return 1 >= delta.days >= 0

	@staticmethod
	def hourDistanceIsOne(early: datetime, late: datetime):
		if early.date() == late.date():
			return late.hour - early.hour <= 1 and early.hour <= late.hour
		delta = late.date() - early.date()
		if delta.days == 1:
			return early.hour == 23 and late.hour == 0
		return False

	@staticmethod
	def isoYearHas53Weeks(isoYear: int):
		g = lambda y: floor((y - 100) / 400) - floor((y - 102) / 400)
		h = lambda y: floor((y - 200) / 400) - floor((y - 199) / 400)
		f = lambda y: 5 * y + 12 - 4 * (floor(y / 100) - floor(y / 400)) + g(y) + h(y)
		return f(isoYear) < 5

	@staticmethod
	def weekDistanceIsOne(early: datetime, late: datetime):
		earlyiso = early.isocalendar()
		lateiso = late.isocalendar()
		if earlyiso[0] == lateiso[0]:
			return lateiso[1] - earlyiso[1] <= 1 and earlyiso[1] <= lateiso[1]
		elif earlyiso[0] == (lateiso[0] - 1):
			return lateiso[1] == 1 and earlyiso[1] == 52 + (TaskLogController.isoYearHas53Weeks(earlyiso[0]))

	@staticmethod
	def yearDistanceIsOne(early: datetime, late: datetime):
		return late.year >= early.year and late.year - early.year <= 1

	@staticmethod
	def monthDistanceIsOne(early: datetime, late: datetime):
		return (early.year == late.year and early.month <= late.month and late.month - early.month <= 1) or (
				early.year == (late.year - 1) and early.month == 12 and late.month == 1)

	def fillRepeats(self, logEntry: TaskLogEntry):
		lastLogEntry = self.taskDatabase.getLatestLogEntryByUIDAndTID(logEntry.uid, logEntry.tid)
		if lastLogEntry:
			taskObject = self.taskDatabase.getTaskByID(logEntry.tid)
			repeatBonus = self.taskDatabase.getRepeatBonusByIDandUID(taskObject.repeat_bonus_id, taskObject.uid)

			hourlyRepeat = repeatBonus.frequency == "HOURLY" and TaskLogController.hourDistanceIsOne(lastLogEntry.timestamp, datetime.now())
			dailyRepeat = repeatBonus.frequency == "DAILY" and TaskLogController.dateDistanceIsOne(lastLogEntry.timestamp, datetime.now())
			weeklyRepeat = repeatBonus.frequency == "WEEKLY" and TaskLogController.weekDistanceIsOne(lastLogEntry.timestamp, datetime.now())
			monthlyRepeat = repeatBonus.frequency == "MONTHLY" and TaskLogController.monthDistanceIsOne(lastLogEntry.timestamp, datetime.now())
			yearlyRepeat = repeatBonus.frequency == "YEARLY" and TaskLogController.yearDistanceIsOne(lastLogEntry.timestamp, datetime.now())

			if hourlyRepeat or dailyRepeat or weeklyRepeat or monthlyRepeat or yearlyRepeat:
				return lastLogEntry.repetition + 1
		return 0

	def logTask(self, logEntry: TaskLogEntry):
		# call a function to fill repeats, as it may be necessary for
		logEntry.repetition = self.fillRepeats(logEntry)
		logEntry.score = self.rewardsController.calculateScore(logEntry)
		return self.taskDatabase.putNewLogEntry(logEntry)
