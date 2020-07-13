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
    	result = self.db.select("SELECT PASSWORD FROM USERS WHERE ID = %s"%(uid), fetchall=0)
    	if result:
    		return result[0]
    	else:
    		return -1


    def createNewUser(self, email, password)
	    if not self.db.insert("INSERT INTO USERS(POINTS,EMAIL) VALUES(0,'%s')"%(email)):
	    	return -1
	    uid = self.getUserByEmail(email)
	    if not self.db.insert("INSERT INTO ACCOUNTS(T,EMAIL,PASSWORD,UID) VALUES('%s','%s','%s',%s)"%(str(datetime.Now()),email,password,uid)):
	    	return -1
	    return uid

