from Utilities.database import DB
from datetime import datetime

class TaskDatabase:
    def __init__(self, host, user, pwd, db):
    	self.db = DB(host, user, pwd,db)

    def getTaskFromTuple(self,tpl):
        return Task(tpl[2],tpl[3],tpl[4],tpl[5],tpl[6],tpl[7],tpl[8],tpl[9],tpl[10],tpl[11],tpl[0])

    def getTimeBonusFromTuple(self,tpl):
        return TimeBonus(tpl[1],tpl[2],tpl[3],tpl[4],tpl[5],tpl[0])

    def getRepeatBonusFromTuple(self,tpl):
        return RepeatBonus(tpl[1],tpl[2],tpl[3],tpl[4],tpl[0])

    def getFocusBonusFromTuple(self,tpl):
        return FocusBonus(tpl[1],tpl[2],tpl[3],tpl[4],tpl[5],tpl[0])

    # def getUserFromTuple(self, tpl):



    def getUserIDByEmail(self, email):
    	result = self.db.select("SELECT ID FROM USERS WHERE EMAIL = '%s'"%(email), fetchall=0)
    	if result:
    		return result[0]
    	else:
    		return -1

    def getUserPasswordByID(self, uid):
    	result = self.db.select("SELECT PASSWORD FROM ACCOUNTS WHERE UID = %s"%(uid), fetchall=0)
    	if result:
    		return result[0]
    	else:
    		return -1

    def getUserByID(self, uid):
        result = self.db.select("SELECT * FROM USERS WHERE ID=%s"%(uid), fetchall=0)
        if result:
            return result[0]
        return -1


    def putNewUser(self, user):
        if not self.db.insert("INSERT INTO USERS(POINTS,EMAIL) VALUES(0,'%s')"%(user.email)):
        	return -1
        uid = self.getUserIDByEmail(user.email)
        try:
            res=self.db.insert("INSERT INTO ACCOUNTS(T,EMAIL,PASSWORD,UID) VALUES('%s','%s','%s',%s)"%(str(datetime.now()),user.email,user.password,uid))
        except Exception as e:
            res=0
            print(e)
        if not res:
        	return -1
        return uid

    def putNewTimeBonus(self, timeBonus):
        if not self.db.insert("INSERT INTO TIME_BONUS(NAME,TYPE,MULTIPLIER,UPPER_BOUND,UID) VALUES('%s','%s',%s,%s,%s)"%(timeBonus.name,timeBonus.type,timeBonus.multiplier,timeBonus.upperbound,timeBonus.uid)):
        	return -1
        return 1

    def putNewRepeatBonus(self, repeatBonus):
        if not self.db.insert("INSERT INTO REPEAT_BONUS(NAME,FREQUENCY,UPPER_BOUND,UID) VALUES('%s','%s',%s,%s)"%(repeatBonus.name,repeatBonus.frequency,repeatBonus.upperbound,repeatBonus.uid)):
        	return -1
        return 1

    def putNewFocusBonus(self, focusBonus):
        if not self.db.insert("INSERT INTO FOCUS_BONUS(NAME,TYPE,LOWER_BOUND,DISTRACTION_PENALTY,UID) VALUES('%s','%s',%s,%s,%s)"%(focusBonus.name,focusBonus.type,focusBonus.lowerbound,focusBonus.distraction_penalty,focusBonus.uid)):
        	return -1
        return 1

    def getBonusesByUID(self, uid):
        time_bonuses = self.db.select("SELECT * FROM TIME_BONUS WHERE UID=%s"%(uid))
        repeat_bonuses = self.db.select("SELECT * FROM REPEAT_BONUS WHERE UID=%s"%(uid))
        focus_bonuses = self.db.select("SELECT * FROM FOCUS_BONUS WHERE UID=%s"%(uid))
        results={
            "time_bonus_list": [getTimeBonusFromTuple(bonus).__dict__ for bonus in time_bonuses],
            "repeat_bonus_list": [getRepeatBonusFromTuple(bonus).__dict__ for bonus in repeat_bonuses],
            "focus_bonus_list": [getFocusBonusFromTuple(bonus).__dict__ for bonus in focus_bonuses]
        }
        return results

    def getTimeBonusByIDandUID(self,tid, uid):
        time_bonus = self.db.select("SELECT * FROM TIME_BONUS WHERE ID=%s and UID=%s"%(tid, uid), fetchall=0)
        return time_bonus

    def getRepeatBonusByIDandUID(self,tid, uid):
        repeat_bonus = self.db.select("SELECT * FROM REPEAT_BONUS WHERE ID=%s and UID=%s"%(tid, uid), fetchall=0)
        return repeat_bonus

    def getFocusBonusByIDandUID(self,tid, uid):
        focus_bonus = self.db.select("SELECT * FROM FOCUS_BONUS WHERE ID=%s and UID=%s"%(tid, uid), fetchall=0)
        return focus_bonus

    def putNewTask(self, task):
        t = str(datetime.now())
        result = self.db.insert("INSERT INTO TASKS VALUES (NULL, '%s', %s, '%s', '%s', '%s', '%s', %s, %s, %s, %s, %s)"%(t, task.uid, task.name, task.description, task.tags, task.type, task.base_score, task.target_time, task.time_bonus, task.repeat_bonus, task.focus_bonus))
        if result:
            return 1
        return -1
