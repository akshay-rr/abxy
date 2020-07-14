from Utilities.database import DB
from datetime import datetime
from Entities.entities import *


class TaskDatabase:
	def __init__(self, host, user, pwd, db):
		self.db = DB(host, user, pwd, db)

	@staticmethod
	def getTaskFromTuple(tpl: tuple):
		return Task(tpl[2], tpl[3], tpl[4], tpl[5], tpl[6], tpl[7], tpl[8], tpl[9], tpl[10], tpl[11], tpl[0])

	@staticmethod
	def getTimeBonusFromTuple(tpl: tuple):
		return TimeBonus(tpl[1], tpl[2], tpl[3], tpl[4], tpl[5], tpl[0])

	@staticmethod
	def getRepeatBonusFromTuple(tpl: tuple):
		return RepeatBonus(tpl[1], tpl[2], tpl[3], tpl[4], tpl[0])

	@staticmethod
	def getFocusBonusFromTuple(tpl: tuple):
		return FocusBonus(tpl[1], tpl[2], tpl[3], tpl[4], tpl[5], tpl[0])

	# def getUserFromTuple(self, tpl):

	def getUserIDByEmail(self, email: str):
		result = self.db.select(
			"SELECT ID FROM USERS WHERE EMAIL = '%s'" % email, fetchall=0)
		if result:
			return result[0]
		else:
			return -1

	def getUserPasswordByID(self, uid: int):
		result = self.db.select(
			"SELECT PASSWORD FROM ACCOUNTS WHERE UID = %s" % uid, fetchall=0)
		if result:
			return result[0]
		else:
			return -1

	def getUserByID(self, uid: int):
		result = self.db.select(
			"SELECT * FROM USERS WHERE ID=%s" % uid, fetchall=0)
		if result:
			return result[0]
		return -1

	def putNewUser(self, user: User):
		if not self.db.insert("INSERT INTO USERS(POINTS,EMAIL) VALUES(0,'%s')" % user.email):
			return -1
		uid = self.getUserIDByEmail(user.email)
		try:
			res = self.db.insert("INSERT INTO ACCOUNTS(T,EMAIL,PASSWORD,UID) VALUES('%s','%s','%s',%s)" % (
				str(datetime.now()), user.email, user.password, uid))
		except Exception as e:
			res = 0
			print(e)
		if not res:
			return -1
		return uid

	def putNewTimeBonus(self, timeBonus: TimeBonus):
		if not self.db.insert("INSERT INTO TIME_BONUS(NAME,TYPE,MULTIPLIER,UPPER_BOUND,UID) VALUES('%s','%s',%s,%s,%s)" % (timeBonus.name, timeBonus.type, timeBonus.multiplier, timeBonus.upper_bound, timeBonus.uid)):
			return -1
		return 1

	def putNewRepeatBonus(self, repeatBonus: RepeatBonus):
		if not self.db.insert("INSERT INTO REPEAT_BONUS(NAME,FREQUENCY,UPPER_BOUND,UID) VALUES('%s','%s',%s,%s)" % (repeatBonus.name, repeatBonus.frequency, repeatBonus.upper_bound, repeatBonus.uid)):
			return -1
		return 1

	def putNewFocusBonus(self, focusBonus: FocusBonus):
		if not self.db.insert("INSERT INTO FOCUS_BONUS(NAME,TYPE,LOWER_BOUND,DISTRACTION_PENALTY,UID) VALUES('%s','%s',%s,%s,%s)" % (focusBonus.name, focusBonus.type, focusBonus.lower_bound, focusBonus.distraction_penalty, focusBonus.uid)):
			return -1
		return 1

	def getBonusesByUID(self, uid: int):
		time_bonuses = self.db.select(
			"SELECT * FROM TIME_BONUS WHERE UID=%s" % uid)
		repeat_bonuses = self.db.select(
			"SELECT * FROM REPEAT_BONUS WHERE UID=%s" % uid)
		focus_bonuses = self.db.select(
			"SELECT * FROM FOCUS_BONUS WHERE UID=%s" % uid)
		results = {
			"time_bonus_list": [self.getTimeBonusFromTuple(bonus).__dict__ for bonus in time_bonuses],
			"repeat_bonus_list": [self.getRepeatBonusFromTuple(bonus).__dict__ for bonus in repeat_bonuses],
			"focus_bonus_list": [self.getFocusBonusFromTuple(bonus).__dict__ for bonus in focus_bonuses]
		}
		return results

	def getTimeBonusByIDandUID(self, tbid: int, uid: int):
		time_bonus = self.db.select(
			"SELECT * FROM TIME_BONUS WHERE ID=%s and UID=%s" % (tbid, uid), fetchall=0)
		if time_bonus:
			return self.getTimeBonusFromTuple(time_bonus)
		return None

	def getRepeatBonusByIDandUID(self, rbid: int, uid: int):
		repeat_bonus = self.db.select(
			"SELECT * FROM REPEAT_BONUS WHERE ID=%s and UID=%s" % (rbid, uid), fetchall=0)
		if repeat_bonus:
			return self.getRepeatBonusFromTuple(repeat_bonus)
		return None

	def getFocusBonusByIDandUID(self, fbid: int, uid: int):
		focus_bonus = self.db.select(
			"SELECT * FROM FOCUS_BONUS WHERE ID=%s and UID=%s" % (fbid, uid), fetchall=0)
		if focus_bonus:
			return self.getFocusBonusFromTuple(focus_bonus)
		return None

	def putNewTask(self, task: Task):
		t = str(datetime.now())
		result = self.db.insert("INSERT INTO TASKS VALUES (NULL, '%s', %s, '%s', '%s', '%s', '%s', %s, %s, %s, %s, %s)" % (
			t, task.uid, task.name, task.description, task.tags, task.task_type, task.base_score, task.target_time, task.time_bonus_id, task.repeat_bonus_id, task.focus_bonus_id))
		if result:
			return 1
		return -1

	def getTaskByID(self, tid: int):
		result = self.db.select(
			"SELECT * FROM TASKS WHERE ID=%s" % tid, fetchall=0)
		if result:
			taskObj = self.getTaskFromTuple(result)
		else:
			taskObj = None
		return taskObj
