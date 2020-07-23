# from Entities.entities import *
# from Repositories.taskDatabase import TaskDatabase
#
#
# class TaskController:
# 	def __init__(self, tdb: TaskDatabase):
# 		self.taskDatabase = tdb
#
# 	def createTask(self, task: Task) -> int:
# 		if self.taskDatabase.getUserByID(task.uid):
# 			if self.taskDatabase.getTimeBonusByIDandUID(task.time_bonus_id, task.uid) and self.taskDatabase.getRepeatBonusByIDandUID(task.repeat_bonus_id, task.uid) and self.taskDatabase.getFocusBonusByIDandUID(task.focus_bonus_id, task.uid):
# 				return self.taskDatabase.putNewTask(task)
# 		return -1
#
# 	# def createNegTask(uid, name, desc, tags, type, base_score, target_time, time_pen_id, repeat_pen_id):
