import mysql.connector
from datetime import datetime

##############################################################################
# Import Instructions
#
# from database import DB
##############################################################################


# TODO
# Return Dictionary results. NO TUPLE!!!!
class DB:

    def __init__(self, host, user, pwd, db):
        self.mydb = mysql.connector.connect(
              host=host,
              user=user,
              passwd=pwd,
              database=db
            )

    def select(self, query, fetchall=1):
        # Select Queries
        try:
            cur = self.mydb.cursor()
        except:
            self.mydb.reconnect()
            cur=self.mydb.cursor()

        cur.execute(query)
        if fetchall==1:
            vals = cur.fetchall()
        else:
            vals = cur.fetchone()
        cur.close()
        return vals

    def insert(self, query):
        # Insert, Update, Delete Queries
        try:
            cur = self.mydb.cursor()
        except:
            self.mydb.reconnect()
            cur=self.mydb.cursor()

        try:
            cur.execute(query)
            self.mydb.commit()
            cur.close()
            return 1
        except Exception as e:
            print(e)
            cur.close()
            return 0
