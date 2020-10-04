from Repositories.taskDatabase import TaskDatabase
import bson
from datetime import datetime


class TaskController:
	def __init__(self, tdb: TaskDatabase):
		self.taskDatabase = tdb

	def createTask(self, taskCreationRequest):
		taskObject = {}
		firebase_id = taskCreationRequest['firebase_id']
		taskObjectKeysFromRequest = ["name", "description", "base_score", "category", "tags"]
		for key in taskObjectKeysFromRequest:
			taskObject[key] = taskCreationRequest[key]
		taskObject['_id'] = bson.ObjectId()
		taskObject['created_on'] = datetime.now()
		taskObject['last_done_on'] = datetime.fromtimestamp(0)
		taskObject['bonuses'] = []
		taskObject['archived'] = False

		return self.taskDatabase.putNewTaskByFirebaseID(firebase_id, taskObject)

	def archiveTask(self, taskArchivalRequest):
		return self.taskDatabase.archiveTaskByFirebaseIDAndTaskID(taskArchivalRequest['firebase_id'], bson.ObjectId(taskArchivalRequest['task_id']))
