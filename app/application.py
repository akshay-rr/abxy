from flask import *
from Controller.userController import UserController
from Repositories.taskDatabase import TaskDatabase
from bson.json_util import dumps

application = app = Flask(__name__)

tdb = TaskDatabase("mongodb+srv://test_user0:riktXHrvxRuVkS6F@cluster0.heb4n.mongodb.net/test?retryWrites=true&w=majority", "test")
user_ctrl = UserController(tdb)


# bonus_ctrl = BonusController(tdb)
# task_ctrl = TaskController(tdb)
# rewards_ctrl = RewardsController(tdb)
# task_log_ctrl = TaskLogController(tdb, rewards_ctrl)


###############################################################################
# USER ACTIONS
###############################################################################
# signInUserRequest(accessToken, name, email, google_id) -> (check if user already exists),
# createTaskRequest(accessToken,name,description,base_points,category,tags)
# createBonusRequest(accessToken,task_id,bonus_type,bonus_name,input_label,upper_bound,lower_bound,evaluation_type,constants)
# logTaskRequest(accessToken,task_id,bonus_instances,remarks)
# accessToken proxies for UID

def verifyNecessaryKeys(myMap: dict, necessaryKeys: list) -> bool:
	for key in necessaryKeys:
		try:
			myMap[key]
		except KeyError:
			return False
	return True


def getUsableKeys(myMap: dict, usableKeys: list) -> dict:
	newMap = {}
	for key in usableKeys:
		newMap[key] = myMap[key]
	return newMap


# TODO: ACCESSTOKEN BASED AUTH
@application.route('/API/signInUserRequest/', methods=['POST'])
def signInUserRequest():
	necessaryKeys = ["access_token", "name", "email", "google_id"]
	optionalKeys = []

	if not verifyNecessaryKeys(request.form, necessaryKeys):
		return "Invalid Request: Items Missing"
	processedRequest = getUsableKeys(request.form, necessaryKeys + optionalKeys)

	asd = user_ctrl.signInUser(processedRequest)
	print("HI")
	return dumps(asd)


# @application.route('/API/createUserRequest/', methods=['POST'])
# def createUserRequest():
# 	email = request.form['email']
# 	pwd = request.form['pwd']
# 	if email and pwd:
# 		user_object = User(email, pwd)
# 		return str(user_ctrl.createUser(user_object))
# 	return "Invalid Request: Items Missing"
#
#
# @application.route('/API/loginUserRequest/', methods=['POST'])
# def loginUserRequest():
# 	email = request.form['email']
# 	pwd = request.form['pwd']
# 	if email and pwd:
# 		user_object = User(email, pwd)
# 		return str(user_ctrl.loginUser(user_object))
# 	return "Invalid Request: Items Missing"
#
#
# @application.route('/API/createTaskRequest/', methods=['POST'])
# def createTaskRequest():
# 	uid = request.form['uid']
# 	name = request.form['name']
# 	desc = request.form['description']
# 	tags = request.form['tags']
# 	task_type = request.form['task_type']
# 	base_score = request.form['base_score']
# 	target_time = request.form['target_time']
# 	time_bonus_id = request.form['time_bonus_id']
# 	repeat_bonus_id = request.form['repeat_bonus_id']
# 	focus_bonus_id = request.form['focus_bonus_id']
# 	task_object = Task(uid, name, desc, tags, taks_type, base_score,
# 					   target_time, time_bonus_id, repeat_bonus_id, focus_bonus_id)
# 	if name and desc and base_score and time_bonus_id and focus_bonus_id and repeat_bonus_id:
# 		if target_time or ((not target_time) and task_type == 'EVENT'):
# 			return str(task_ctrl.createTask(task_object))
# 	return "Invalid Request"
#
#
# @application.route('/API/logTaskRequest/', methods=['POST'])
# def logTaskRequest():
# 	uid = request.form['uid']
# 	tid = request.form['tid']
# 	duration = int(request.form['duration'])
# 	focus = int(request.form['focus'])
# 	remarks = request.form['remarks']
# 	task_log_object = TaskLogEntry(uid, tid, duration, focus, remarks)
# 	if uid and tid and focus:
# 		return str(task_log_ctrl.logTask(task_log_object))
# 	return "Invalid Request"
#
#
# @application.route('/API/createNegTaskRequest/', methods=['POST'])
# def createNegTaskRequest():
# 	uid = request.form['uid']
# 	name = request.form['name']
# 	desc = request.form['desc']
# 	tags = request.form['tags']
# 	type = request.form['type']
# 	base_score = request.form['base_score']
# 	target_time = request.form['target_time']
# 	time_pen_id = request.form['time_pen_id']
# 	repeat_pen_id = request.form['repeat_pen_id']
# 	if name and desc and base_score and time_pen_id and repeat_pen_id:
# 		if target_time or ((not target_time) and type == 'EVENT'):
# 			return task_ctrl.createNegTask(uid, name, desc, tags, type, base_score, target_time, time_pen_id, repeat_pen_id)
# 	return "Invalid Request"
#
#
# @application.route('/API/logNegTaskRequest/', methods=['POST'])
# def logNegTaskRequest():
# 	uid = request.form['uid']
# 	ntid = request.form['ntid']
# 	duration = request.form['duration']
# 	remarks = request.form['remarks']
# 	if uid and ntid:
# 		return task_ctrl.logNegTask(uid, ntid, duration, remarks)
# 	return "Invalid Request"
#
#
# @application.route('/API/createTimeBonusRequest/', methods=['POST'])
# def createTimeBonusRequest():
# 	uid = request.form['uid']
# 	name = request.form['name']
# 	tb_type = request.form['type']
# 	multiplier = request.form['multiplier']
# 	upper_bound = request.form['upper_bound']
# 	if uid and upper_bound and tb_type == 'LOGARITHMIC':
# 		time_bonus_object = TimeBonus(name, tb_type, multiplier, upper_bound, uid)
# 		return str(bonus_ctrl.createTimeBonus(time_bonus_object))
# 	if uid and multiplier and tb_type == "ADDITIVE":
# 		time_bonus_object = TimeBonus(name, tb_type, multiplier, upper_bound, uid)
# 		return str(bonus_ctrl.createTimeBonus(time_bonus_object))
# 	return "Invalid Request"
#
#
# @application.route('/API/createRepeatBonusRequest/', methods=['POST'])
# def createRepeatBonusRequest():
# 	uid = request.form['uid']
# 	name = request.form['name']
# 	frequency = request.form['frequency']
# 	upper_bound = request.form['upper_bound']
# 	if uid and upper_bound and name and frequency:
# 		repeat_bonus_object = RepeatBonus(name, frequency, upper_bound, uid)
# 		return str(bonus_ctrl.createRepeatBonus(repeat_bonus_object))
# 	return "Invalid Request"
#
#
# @application.route('/API/createFocusBonusRequest/', methods=['POST'])
# def createFocusBonusRequest():
# 	uid = request.form['uid']
# 	name = request.form['name']
# 	fb_type = request.form['type']
# 	lower_bound = request.form['lower_bound']
# 	distraction_penalty = request.form['distraction_penalty']
#
# 	if uid and name and lower_bound and fb_type == 'MULTIPLICATIVE':
# 		focus_bonus_object = FocusBonus(
# 			name, fb_type, lower_bound, distraction_penalty, uid)
# 		return str(bonus_ctrl.createFocusBonus(focus_bonus_object))
#
# 	if uid and name and distraction_penalty and fb_type == 'ADDITIVE':
# 		focus_bonus_object = FocusBonus(
# 			name, fb_type, lower_bound, distraction_penalty, uid)
# 		return str(bonus_ctrl.createFocusBonus(focus_bonus_object))
# 	return "Invalid Request"
#
#
# @application.route('/API/createTimePenRequest/', methods=['POST'])
# def createTimePenRequest():
# 	uid = request.form['uid']
# 	name = request.form['name']
# 	type = request.form['type']
# 	multiplier = request.form['multiplier']
# 	upper_bound = request.form['upper_bound']
#
# 	if uid and upper_bound and type == 'LOGARITHMIC':
# 		return bonus_ctrl.createTimePen(name, type, multiplier, upper_bound, uid)
# 	if uid and multiplier and type == "ADDITIVE":
# 		return bonus_ctrl.createTimePen(name, type, multiplier, upper_bound, uid)
# 	return "Invalid Request"
#
#
# @application.route('/API/createRepeatPenRequest/', methods=['POST'])
# def createRepeatPenRequest():
# 	uid = request.form['uid']
# 	name = request.form['name']
# 	upper_bound = request.form['upper_bound']
# 	if uid and upper_bound and name:
# 		return bonus_ctrl.createRepeatPen(name, upper_bound, uid)
# 	return "Invalid Request"
#
#
# @application.route('/API/listBonusRequest/', methods=['POST'])
# def listBonusRequest():
# 	uid = request.form['uid']
# 	if uid:
# 		response = bonus_ctrl.listBonusesByUID(uid)
# 		if response == -1:
# 			return "-1"
# 		else:
# 			return response
# 	return "Invalid Request"
#
#
# @application.route('/API/listPenRequest/', methods=['POST'])
# def listPenRequest():
# 	uid = request.form['uid']
# 	if uid:
# 		return bonus_ctrl.listPen(uid)
# 	return "Invalid Request"


###############################################################################
#
###############################################################################


if __name__ == "__main__":
	application.run(debug=True, host='0.0.0.0', port=8000)
