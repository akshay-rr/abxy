from flask import *
import mysql.connector
from datetime import datetime
import json
import requests
from Utilities.database import DB
from Controller.userController import UserController
from Repositories.taskDatabase import TaskDatabase

application = app = Flask(__name__)

application.secret_key = "ABXY0"

tdb = TaskDatabase('aa1g61rixhyool1.cbvzqizsnmrt.us-east-1.rds.amazonaws.com','admin','b-SCALE2020','abxy')
userctrl = UserController(tdb)
ctrl = UserController(tdb)

###############################################################################
# USER ACTIONS
###############################################################################

@application.route('/API/createUserRequest/', methods=['POST'])
def createUserRequest():
    email = request.form['email']
    pwd = request.form['pwd']
    if email and pwd:
        return str(userctrl.createUser(email, pwd))
    return "Invalid Request: Items Missing"

@application.route('/API/loginUserRequest/', methods=['POST'])
def loginUserRequest():
    email = request.form['email']
    pwd = request.form['pwd']
    if email and pwd:
        return str(userctrl.loginUser(email, pwd))
    return "Invalid Request: Items Missing"

@application.route('/API/createTaskRequest/', methods=['POST'])
def createTaskRequest():
    name = request.form['name']
    desc = request.form['desc']
    tags = request.form['tags']
    type = request.form['type']
    base_score = request.form['base_score']
    target_time = request.form['target_time']
    time_bonus_id = request.form['time_bonus_id']
    repeat_bonus_id = request.form['repeat_bonus_id']
    focus_bonus_id = request.form['focus_bonus_id']
    if name and desc and base_score and time_bonus_id and focus_bonus_id and repeat_bonus_id:
        if target_time or ((not target_time) and type=='EVENT'):
            return ctrl.createTask(name, desc, tags, type, base_score, target_time, time_bonus_id, repeat_bonus_id, focus_bonus_id)
    return "Invalid Request"

@application.route('/API/logTaskRequest/', methods=['POST'])
def logTaskRequest():
    uid = request.form['uid']
    tid = request.form['tid']
    duration = request.form['duration']
    focus = request.form['focus']
    remarks = request.form['remarks']
    if uid and tid and focus:
        return ctrl.logTask(uid, tid, duration, focus, remarks)
    return "Invalid Request"

@application.route('/API/createNegTaskRequest/', methods=['POST'])
def createNegTaskRequest():
    name = request.form['name']
    desc = request.form['desc']
    tags = request.form['tags']
    type = request.form['type']
    base_score = request.form['base_score']
    target_time = request.form['target_time']
    time_pen_id = request.form['time_pen_id']
    repeat_pen_id = request.form['repeat_pen_id']
    if name and desc and base_score and time_pen_id and repeat_pen_id:
        if target_time or ((not target_time) and type=='EVENT'):
            return ctrl.createNegTask(name, desc, tags, type, base_score, target_time, time_pen_id, repeat_pen_id)
    return "Invalid Request"

@application.route('/API/logNegTaskRequest/', methods=['POST'])
def logNegTaskRequest():
    uid = request.form['uid']
    ntid = request.form['ntid']
    duration = request.form['duration']
    remarks = request.form['remarks']
    if uid and ntid:
        return ctrl.logNegTask(uid, ntid, duration, remarks)
    return "Invalid Request"

@application.route('/API/createTimeBonusRequest/', methods=['POST'])
def createTimeBonusRequest():
    uid = request.form['uid']
    name = request.form['name']
    type = request.form['type']
    multiplier = request.form['multiplier']
    upperbound = request.form['upperbound']
    if uid and upperbound and type=='LOGARITHMIC':
        return ctrl.createTimeBonus(name, type, multiplier, upperbound, uid)
    if uid and multiplier and type=="ADDITIVE":
        return ctrl.createTimeBonus(name, type, multiplier, upperbound, uid)
    return "Invalid Request"

@application.route('/API/createRepeatBonusRequest/', methods=['POST'])
def createRepeatBonusRequest():
    uid = request.form['uid']
    name = request.form['name']
    frequency = request.form['frequency']
    upperbound = request.form['upperbound']
    if uid and upperbound and name and frequency:
        return ctrl.createRepeatBonus(name, frequency, upperbound, uid)
    return "Invalid Request"

@application.route('/API/createFocusBonusRequest/', methods=['POST'])
def createFocusBonusRequest():
    uid = request.form['uid']
    name = request.form['name']
    type = request.form['type']
    lowerbound = request.form['lowerbound']
    distraction_penalty = request.form['distraction_penalty']

    if uid and name and lowerbound and type=='LOGARITHMIC':
        return ctrl.createFocusBonus(name, type, lowerbound, distraction_penalty, uid)

    if uid and name and distraction_penalty and type=='ADDITIVE':
        return ctrl.createFocusBonus(name, type, lowerbound, distraction_penalty, uid)
    return "Invalid Request"

@application.route('/API/createTimePenRequest/', methods=['POST'])
def createTimePenRequest():
    uid = request.form['uid']
    name = request.form['name']
    type = request.form['type']
    multiplier = request.form['multiplier']
    upperbound = request.form['upperbound']

    if uid and upperbound and type=='LOGARITHMIC':
        return ctrl.createTimePen(name, type, multiplier, upperbound, uid)
    if uid and multiplier and type=="ADDITIVE":
        return ctrl.createTimePen(name, type, multiplier, upperbound, uid)

    return "Invalid Request"

@application.route('/API/createRepeatPenRequest/', methods=['POST'])
def createRepeatPenRequest():
    uid = request.form['uid']
    name = request.form['name']
    upperbound = request.form['upperbound']
    if uid and upperbound and name:
        return ctrl.createRepeatPen(name, upperbound, uid)
    return "Invalid Request"

@application.route('/API/listBonusRequest/', methods=['POST'])
def listBonusRequest():
    uid = request.form['uid']
    if uid:
        return ctrl.listBonus(uid)
    return "Invalid Request"

@application.route('/API/listPenRequest/', methods=['POST'])
def listPenRequest():
    uid = request.form['uid']
    if uid:
        return ctrl.listPen(uid)
    return "Invalid Request"
###############################################################################
#
###############################################################################

if __name__ == "__main__":
    application.run(debug=True, host='0.0.0.0', port = 8000)
