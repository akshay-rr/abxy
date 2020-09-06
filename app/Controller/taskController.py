from Repositories.taskDatabase import TaskDatabase
import bson
from datetime import datetime


class TaskController:
	def __init__(self, tdb: TaskDatabase):
		self.taskDatabase = tdb

	def createTask(self, taskCreationRequest):
		taskObject = {}
		uid = taskCreationRequest['uid']
		taskObjectKeysFromRequest = ["name", "description", "base_score", "category", "tags"]
		for key in taskObjectKeysFromRequest:
			taskObject[key] = taskCreationRequest[key]
		taskObject['_id'] = bson.ObjectId()
		taskObject['created_on'] = datetime.now()
		taskObject['last_done_on'] = datetime.utcfromtimestamp(0)
		taskObject['bonuses'] = []
		taskObject['archived'] = False

		return self.taskDatabase.putNewTask(uid, taskObject)

	def archiveTask(self, taskArchivalRequest):
		return self.taskDatabase.archiveTaskByUIDAndTaskID(bson.ObjectId(taskArchivalRequest['uid']), bson.ObjectId(taskArchivalRequest['task_id']))
