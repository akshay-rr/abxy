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


    def createNewUser(self, email, password):
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

    def createNewTimeBonus(self, name, type, multiplier, upperbound, uid):
        if not self.db.insert("INSERT INTO TIME_BONUS(NAME,TYPE,MULTIPLIER,UPPER_BOUND,UID) VALUES('%s','%s',%s,%s,%s)"%(name,type,multiplier,upperbound,uid)):
        	return -1
        return 1

    def createNewRepeatBonus(self, name, frequency, upperbound, uid):
        if not self.db.insert("INSERT INTO REPEAT_BONUS(NAME,FREQUENCY,UPPER_BOUND,UID) VALUES('%s','%s',%s,%s)"%(name,frequency,upperbound,uid)):
        	return -1
        return 1

    def createNewFocusBonus(self, name, type, lowerbound, distraction_penalty, uid):
        if not self.db.insert("INSERT INTO FOCUS_BONUS(NAME,TYPE,LOWER_BOUND,DISTRACTION_PENALTY,UID) VALUES('%s','%s',%s,%s,%s)"%(name,type,lowerbound,distraction_penalty,uid)):
        	return -1
        return 1
