from Repositories.taskDatabase import TaskDatabase

class TaskController:
    def __init__(self,tdb):
    	self.taskDatabase = tdb

    def createTask(self, uid, name, description, tags, type, base_score, target_time, time_bonus_id, repeat_bonus_id, focus_bonus_id):
        if self.taskDatabase.getUserByID(uid):
            if self.taskDatabase.getTimeBonusByIDandUID(time_bonus_id, uid) and self.taskDatabase.getRepeatBonusByIDandUID(repeat_bonus_id, uid) and self.taskDatabase.getFocusBonusByIDandUID(focus_bonus_id, uid):
                return self.taskDatabase.putNewTask(uid, name, description, tags, type, base_score, target_time, time_bonus_id, repeat_bonus_id, focus_bonus_id)
        return -1

    # def createNegTask(uid, name, desc, tags, type, base_score, target_time, time_pen_id, repeat_pen_id):
