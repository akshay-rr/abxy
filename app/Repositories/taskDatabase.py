from Utilities.database import DB
from datetime import datetime

class TaskDatabase:
    def __init__(self, host, user, pwd, db):
    	self.db = DB(host, user, pwd,db)

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


    def putNewUser(self, email, password):
        if not self.db.insert("INSERT INTO USERS(POINTS,EMAIL) VALUES(0,'%s')"%(email)):
        	return -1
        uid = self.getUserIDByEmail(email)
        try:
            res=self.db.insert("INSERT INTO ACCOUNTS(T,EMAIL,PASSWORD,UID) VALUES('%s','%s','%s',%s)"%(str(datetime.now()),email,password,uid))
        except Exception as e:
            res=0
            print(e)
        if not res:
        	return -1
        return uid

    def putNewTimeBonus(self, name, type, multiplier, upperbound, uid):
        if not self.db.insert("INSERT INTO TIME_BONUS(NAME,TYPE,MULTIPLIER,UPPER_BOUND,UID) VALUES('%s','%s',%s,%s,%s)"%(name,type,multiplier,upperbound,uid)):
        	return -1
        return 1

    def putNewRepeatBonus(self, name, frequency, upperbound, uid):
        if not self.db.insert("INSERT INTO REPEAT_BONUS(NAME,FREQUENCY,UPPER_BOUND,UID) VALUES('%s','%s',%s,%s)"%(name,frequency,upperbound,uid)):
        	return -1
        return 1

    def putNewFocusBonus(self, name, type, lowerbound, distraction_penalty, uid):
        if not self.db.insert("INSERT INTO FOCUS_BONUS(NAME,TYPE,LOWER_BOUND,DISTRACTION_PENALTY,UID) VALUES('%s','%s',%s,%s,%s)"%(name,type,lowerbound,distraction_penalty,uid)):
        	return -1
        return 1

    def getBonusesByUID(self, uid):
        time_bonuses = self.db.select("SELECT * FROM TIME_BONUS WHERE UID=%s"%(uid))
        repeat_bonuses = self.db.select("SELECT * FROM REPEAT_BONUS WHERE UID=%s"%(uid))
        focus_bonuses = self.db.select("SELECT * FROM FOCUS_BONUS WHERE UID=%s"%(uid))
        results={
            "time_bonus_list": time_bonuses,
            "repeat_bonus_list": repeat_bonuses,
            "focus_bonus_list": focus_bonuses
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

    def putNewTask(self, uid, name, description, tags, type, base_score, target_time, time_bonus, repeat_bonus, focus_bonus):
        t = str(datetime.now())
        result = self.db.insert("INSERT INTO TASKS VALUES (NULL, '%s', %s, '%s', '%s', '%s', '%s', %s, %s, %s, %s, %s)"%(t, uid, name, description, tags, type, base_score, target_time, time_bonus, repeat_bonus, focus_bonus))
        if result:
            return 1
        return -1
