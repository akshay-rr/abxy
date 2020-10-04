from flask import *
from Controller.userController import UserController
from Controller.taskController import TaskController
from Controller.bonusController import BonusController
from Controller.logController import LogController
from Repositories.taskDatabase import TaskDatabase
from bson.json_util import dumps
import bson

import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth

cred = credentials.Certificate("abxy-3e495-firebase-adminsdk-zir93-682dad0957.json")
firebase_admin.initialize_app(cred)

application = app = Flask(__name__)

tdb = TaskDatabase("mongodb+srv://admin_user:Brskol8pZbhZwcec@cluster0.j34k4.mongodb.net/test?retryWrites=true&w=majority", "test")
task_ctrl = TaskController(tdb)
bonus_ctrl = BonusController(tdb)
log_ctrl = LogController(tdb, bonus_ctrl)
user_ctrl = UserController(tdb, log_ctrl)


# rewards_ctrl = RewardsController(tdb)
# task_log_ctrl = TaskLogController(tdb, rewards_ctrl)


###############################################################################
# USER ACTIONS
###############################################################################
# signInUserRequest(accessToken, name, email, google_id) -> (check if user already exists),
# createTaskRequest(accessToken,name,description,base_score,category,tags)
# createBonusRequest(accessToken,task_id,bonus_type,bonus_name,input_label,upper_bound,lower_bound,evaluation_type,constants)
# logTaskRequest(accessToken,task_id,bonus_instances,remarks) -> bonus_instances is an array of
# accessToken proxies for UID

def authenticateToken(id_token):
	# id_token comes from the client app (shown above)
	try:
		decoded_token = auth.verify_id_token(id_token)
	except ValueError:
		return "ID TOKEN MALFORMED"
	except auth.ExpiredIdTokenError:
		return "ID TOKEN EXPIRED"
	uid = decoded_token['uid']
	return uid


def verifyNecessaryRequestKeys(myMap: dict, necessaryKeys: list) -> bool:
	for key in necessaryKeys:
		try:
			myMap[key]
		except KeyError:
			return False
	return True


keysToBeFloats = ["upper_bound", "lower_bound"]
keysToBeFloatArrays = ["constants"]


def extractRequiredKeys(myMap: dict, required: list) -> dict:
	newMap = {}
	for key in required:
		newMap[key] = json.loads(myMap[key])
		if key in keysToBeFloats:
			newMap[key] = float(newMap[key])
		if key in keysToBeFloatArrays:
			newMap[key] = [float(x) for x in newMap[key]]
	return newMap


@application.route('/API/Health/', methods=['POST'])
def health():
	print(request.form)
	return dumps({"KEY": "HEALTHY"})


@application.route('/API/registerNewUser/', methods=['POST'])
def registerNewUser():
	id_token = request.headers['id_token']
	firebase_id = authenticateToken(id_token)
	if firebase_id == "ID TOKEN MALFORMED" or firebase_id == "ID TOKEN EXPIRED":
		return dumps(firebase_id)

	necessaryKeys = ["name", "email"]
	objectKeys = ["name", "email"]

	if not verifyNecessaryRequestKeys(request.form, necessaryKeys):
		return dumps("Invalid Request: Items Missing")

	processedRequest = extractRequiredKeys(request.form, objectKeys)
	processedRequest['firebase_id'] = firebase_id

	test = dumps(user_ctrl.registerNewUserAndReturnData(processedRequest))
	return test


@application.route('/API/getUser/', methods=['POST'])
def getUser():
	id_token = request.headers['id_token']
	firebase_id = authenticateToken(id_token)
	if firebase_id == "ID TOKEN MALFORMED" or firebase_id == "ID TOKEN EXPIRED":
		return dumps(firebase_id)

	test = dumps(user_ctrl.fetchLatestUserWithoutArchivedTasksByFirebaseID(firebase_id))
	# print(test)
	return test


@application.route('/API/createTask/', methods=['POST'])
def createTask():
	id_token = request.headers['id_token']
	firebase_id = authenticateToken(id_token)
	if firebase_id == "ID TOKEN MALFORMED" or firebase_id == "ID TOKEN EXPIRED":
		return dumps(firebase_id)

	necessaryKeys = ["name", "description", "base_score", "category", "tags"]
	objectKeys = ["name", "description", "base_score", "category", "tags"]

	if not verifyNecessaryRequestKeys(request.form, necessaryKeys):
		return dumps("Invalid Request: Items Missing")
	processedRequest = extractRequiredKeys(request.form, objectKeys)

	processedRequest['firebase_id'] = firebase_id

	result = task_ctrl.createTask(processedRequest)
	if result is None:
		return dumps("IT DIDN'T WORK")
	return dumps(str(result))


@application.route('/API/archiveTask/', methods=['POST'])
def archiveTask():
	id_token = request.headers['id_token']
	firebase_id = authenticateToken(id_token)
	if firebase_id == "ID TOKEN MALFORMED" or firebase_id == "ID TOKEN EXPIRED":
		return dumps(firebase_id)

	necessaryKeys = ["task_id"]
	objectKeys = ["task_id"]

	if not verifyNecessaryRequestKeys(request.form, necessaryKeys):
		return dumps("Invalid Request: Items Missing")
	processedRequest = extractRequiredKeys(request.form, objectKeys)

	processedRequest['firebase_id'] = firebase_id

	result = task_ctrl.archiveTask(processedRequest)
	if result is None:
		return dumps("IT DIDN'T WORK")
	return dumps(str(result))


# createBonusRequest(access_token,task_id,data_source,bonus_name,input_label,upper_bound,lower_bound,evaluation_type,constants)
@application.route('/API/createBonus/', methods=['POST'])
def createBonus():
	id_token = request.headers['id_token']
	firebase_id = authenticateToken(id_token)
	if firebase_id == "ID TOKEN MALFORMED" or firebase_id == "ID TOKEN EXPIRED":
		return dumps(firebase_id)

	necessaryKeys = ["task_id", "data_source", "bonus_name", "input_label", "upper_bound", "lower_bound", "evaluation_type", "constants"]
	objectKeys = ["task_id", "data_source", "bonus_name", "input_label", "upper_bound", "lower_bound", "evaluation_type", "constants"]

	# print(request.form)

	if not verifyNecessaryRequestKeys(request.form, necessaryKeys):
		return dumps("Invalid Request: Items Missing")
	processedRequest = extractRequiredKeys(request.form, objectKeys)

	processedRequest['task_id'] = bson.ObjectId(processedRequest['task_id'])

	processedRequest['firebase_id'] = firebase_id

	result = bonus_ctrl.createBonus(processedRequest)
	if result is None:
		return dumps("IT DIDN'T WORK")
	return dumps(str(result))


# @application.route('/API/deleteBonus',methods=['DELETE'])
# def createBonus():


# logTaskRequest(access_token,task_id,bonus_instances,remarks) -> bonus_instances is an array of
@application.route('/API/logTask/', methods=["POST"])
def logTask():
	id_token = request.headers['id_token']
	firebase_id = authenticateToken(id_token)
	if firebase_id == "ID TOKEN MALFORMED" or firebase_id == "ID TOKEN EXPIRED":
		return dumps(firebase_id)

	necessaryKeys = ["task_id", "bonus_instances", "remarks", "timestamp"]
	objectKeys = ["task_id", "bonus_instances", "remarks", "timestamp"]

	# print(request.form)

	if not verifyNecessaryRequestKeys(request.form, necessaryKeys):
		return dumps("Invalid Request: Items Missing")
	processedRequest = extractRequiredKeys(request.form, objectKeys)

	processedRequest['firebase_id'] = firebase_id

	result = log_ctrl.logTask(processedRequest)
	if result is None:
		return dumps("IT DIDN'T WORK")
	return dumps(str(result))


@application.route('/API/deleteLog/', methods=["POST"])
def deleteLog():
	id_token = request.headers['id_token']
	firebase_id = authenticateToken(id_token)
	if firebase_id == "ID TOKEN MALFORMED" or firebase_id == "ID TOKEN EXPIRED":
		return dumps(firebase_id)

	necessaryKeys = [ "log_id"]
	objectKeys = ["log_id"]

	if not verifyNecessaryRequestKeys(request.form, necessaryKeys):
		return dumps("Invalid Request: Items Missing")
	processedRequest = extractRequiredKeys(request.form, objectKeys)

	processedRequest['firebase_id'] = firebase_id

	result = log_ctrl.deleteLog(processedRequest)
	if result is None:
		return dumps("IT DIDN'T WORK")
	return dumps(str(result))


# getUserLogEntries(access_token)
@application.route('/API/getUserLogEntries/', methods=["POST"])
def getUserLogEntries():
	# IS BROKEN
	necessaryKeys = ["access_token"]
	processedRequest = {}

	if not verifyNecessaryRequestKeys(request.form, necessaryKeys):
		return dumps("Invalid Request: Items Missing")

	uid = authenticateToken(request.form['access_token'])
	processedRequest['uid'] = uid

	result = log_ctrl.retrieveUserLogEntries(processedRequest)
	if result is None:
		return dumps("IT DIDN'T WORK")
	return dumps(str(result))


###############################################################################
#
###############################################################################


if __name__ == "__main__":
	application.run(debug=True, host='0.0.0.0', port=8000)
