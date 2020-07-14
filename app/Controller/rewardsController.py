import math
from Entities.entities import *
from Repositories.taskDatabase import TaskDatabase


class RewardsController:

    def __init__(self, tdb: TaskDatabase):
        self.taskDatabase = tdb

    def calculateTimeBonus(self, taskEntry: TaskLogEntry, taskObj: Task) -> object:
        if taskObj:
            timeBonusObject = self.taskDatabase.getTimeBonusByIDandUID(taskObj.time_bonus_id, taskEntry.uid)
            ans = 0
            print(taskEntry.duration)
            print(type(taskEntry.duration))
            if timeBonusObject.tb_type == "DIMINISHING":
                ans = timeBonusObject.upper_bound * math.tanh(
                    (taskEntry.duration / taskObj.target_time) - 1)
            elif timeBonusObject.tb_type == "ADDITIVE":
                ans = timeBonusObject.multiplier * (taskEntry.duration-taskObj.target_time)
            return ans
        return None

    def calculateRepeatBonus(self, taskEntry: TaskLogEntry, taskObj: Task) -> int:
        if taskObj:
            repeatBonusObject = self.taskDatabase.getRepeatBonusByIDandUID(
                taskObj.repeat_bonus_id, taskEntry.uid)
            ans = repeatBonusObject.upper_bound * math.tanh(taskEntry.repetition/10)
            return ans
        return None

    def calculateFocusBonus(self, taskEntry: TaskLogEntry, taskObj: Task) -> int:
        if taskObj:
            focusBonusObject = self.taskDatabase.getFocusBonusByIDandUID(
                taskObj.focus_bonus_id, taskEntry.uid)
            if focusBonusObject.fb_type == "ADDITIVE":
                ans = focusBonusObject.distraction_penalty*(taskEntry.focus-5)
            # elif focusBonusObject.fb_type == "MULTIPLICATIVE":
            #                     TODO
            return ans
        return None

    def calculateScore(self, taskEntry: TaskLogEntry) -> int:
        taskObj = self.taskDatabase.getTaskByID(taskEntry.tid)
        baseScoreVal = taskObj.base_score
        timeBonusVal = self.calculateTimeBonus(taskEntry, taskObj)
        repeatBonusVal = self.calculateRepeatBonus(taskEntry, taskObj)
        focusBonusVal = self.calculateFocusBonus(taskEntry, taskObj)
        return baseScoreVal + timeBonusVal + repeatBonusVal + focusBonusVal
