import math
from Entities.entities import *
from Repositories.taskDatabase import TaskDatabase


class RewardsController:

    def __init__(self, tdb: TaskDatabase):
        self.taskDatabase = tdb

    def calculateTimeBonus(self, taskEntry: TaskLogEntry, taskObj: Task) -> object:
        if taskObj:
            timeBonusObject = self.taskDatabase.getTimeBonusByIDandUID(taskObj.time_bonus_id, taskEntry.uid)
            # Calculation
            ans = 0
            if timeBonusObject.type == "DIMINISHING":
                ans = timeBonusObject.upper_bound * (2.0 / math.pi) * math.atan(
                    (taskEntry.duration / taskObj.target_time) - 1)
            return ans
        return None

    def calculateRepeatBonus(self, taskEntry: TaskLogEntry, taskObj: Task) -> int:
        if taskObj:
            repeatBonusObject = self.taskDatabase.getRepeatBonusByIDandUID(
                taskObj.repeat_bonus_id, taskEntry.uid)
            # Calculation
            ans = 0
            return ans
        return None

    def calculateFocusBonus(self, taskEntry: TaskLogEntry, taskObj: Task) -> int:
        if taskObj:
            focusBonusObject = self.taskDatabase.getFocusBonusByIDandUID(
                taskObj.focus_bonus_id, taskEntry.uid)
            # Calculation
            ans = 0
            return ans
        return None

    def calculateScore(self, taskEntry: TaskLogEntry) -> int:
        taskObj = self.taskDatabase.getTaskById(taskEntry.tid)
        baseScoreVal = taskObj.base_score
        timeBonusVal = self.calculateTimeBonus(taskEntry, taskObj)
        repeatBonusVal = self.calculateRepeatBonus(taskEntry, taskObj)
        focusBonusVal = self.calculateFocusBonus(taskEntry, taskObj)
        return baseScoreVal + timeBonusVal + repeatBonusVal + focusBonusVal
