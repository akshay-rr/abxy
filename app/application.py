from flask import *
import mysql.connector
from datetime import datetime
import json
import requests
from Utilities.database import DB

application = app = Flask(__name__)

application.secret_key = "ABXY0"

db = DB("aa1g61rixhyool1.cbvzqizsnmrt.us-east-1.rds.amazonaws.com", "admin", "b-SCALE2020", "abxy")

###############################################################################
# USER ACTIONS
###############################################################################

@application.route('/API/createUserRequest/', methods=['POST'])
def createUserRequest():
    # Function Call
    return "1"

@application.route('/API/loginUserRequest/', methods=['POST'])
def loginUserRequest():
    # Function Call
    return "1"

@application.route('/API/createTaskRequest/', methods=['POST'])
def createTaskRequest():
    # Function Call
    return "1"

@application.route('/API/logTaskRequest/', methods=['POST'])
def logTaskRequest():
    # Function Call
    return "1"

@application.route('/API/createNegTaskRequest/', methods=['POST'])
def createNegTaskRequest():
    # Function Call
    return "1"

@application.route('/API/logNegTaskRequest/', methods=['POST'])
def logNegTaskRequest():
    # Function Call
    return "1"

###############################################################################
#
###############################################################################

if __name__ == "__main__":
    application.run(debug=True, host='0.0.0.0', port = 8000)
