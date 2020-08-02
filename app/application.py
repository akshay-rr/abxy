from flask import *
from Controller.userController import UserController
from Controller.taskController import TaskController
from Controller.bonusController import BonusController
from Controller.logController import LogController
from Repositories.taskDatabase import TaskDatabase
from bson.json_util import dumps
import bson

application = app = Flask(__name__)

tdb = TaskDatabase("mongodb+srv://test_user0:riktXHrvxRuVkS6F@cluster0.heb4n.mongodb.net/test?retryWrites=true&w=majority", "test")
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

def authenticateToken(accessToken):
	accessToken = json.loads(accessToken)
	return user_ctrl.fetchCurrentActiveUserByAccessToken(accessToken)


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


@application.route('/API/signInUser/', methods=['POST'])
def signInUser():
	necessaryKeys = ["access_token", "name", "email", "google_id"]
	objectKeys = ["access_token", "name", "email", "google_id"]

	if not verifyNecessaryRequestKeys(request.form, necessaryKeys):
		return dumps("Invalid Request: Items Missing")
	processedRequest = extractRequiredKeys(request.form, objectKeys)

	return dumps(user_ctrl.signInUserAndReturnData(processedRequest))


@application.route('/API/getUser/', methods=['POST'])
def getUser():
	necessaryKeys = ["access_token"]
	objectKeys = []

	if not verifyNecessaryRequestKeys(request.form, necessaryKeys):
		return dumps("Invalid Request: Items Missing")
	processedRequest = extractRequiredKeys(request.form, objectKeys)

	uid = authenticateToken(request.form['access_token'])
	processedRequest['uid'] = uid

	return dumps(user_ctrl.fetchLatestUser(uid))


@application.route('/API/createTask/', methods=['POST'])
def createTask():
	necessaryKeys = ["access_token", "name", "description", "base_score", "category", "tags"]
	objectKeys = ["name", "description", "base_score", "category", "tags"]

	if not verifyNecessaryRequestKeys(request.form, necessaryKeys):
		return dumps("Invalid Request: Items Missing")
	processedRequest = extractRequiredKeys(request.form, objectKeys)

	uid = authenticateToken(request.form['access_token'])
	processedRequest['uid'] = uid

	result = task_ctrl.createTask(processedRequest)
	if result is None:
		return dumps("IT DIDN'T WORK")
	return dumps(str(result))


# createBonusRequest(access_token,task_id,data_source,bonus_name,input_label,upper_bound,lower_bound,evaluation_type,constants)
@application.route('/API/createBonus/', methods=['POST'])
def createBonus():
	necessaryKeys = ["access_token", "task_id", "data_source", "bonus_name", "input_label", "upper_bound", "lower_bound", "evaluation_type", "constants"]
	objectKeys = ["task_id", "data_source", "bonus_name", "input_label", "upper_bound", "lower_bound", "evaluation_type", "constants"]

	if not verifyNecessaryRequestKeys(request.form, necessaryKeys):
		return dumps("Invalid Request: Items Missing")
	processedRequest = extractRequiredKeys(request.form, objectKeys)

	processedRequest['task_id'] = bson.ObjectId(processedRequest['task_id'])

	uid = authenticateToken(request.form['access_token'])
	processedRequest['uid'] = uid

	result = bonus_ctrl.createBonus(processedRequest)
	if result is None:
		return dumps("IT DIDN'T WORK")
	return dumps(str(result))


# logTaskRequest(access_token,task_id,bonus_instances,remarks) -> bonus_instances is an array of
@application.route('/API/logTask/', methods=["POST"])
def logTask():
	necessaryKeys = ["access_token", "task_id", "bonus_instances", "remarks"]
	objectKeys = ["task_id", "bonus_instances", "remarks"]

	if not verifyNecessaryRequestKeys(request.form, necessaryKeys):
		return dumps("Invalid Request: Items Missing")
	processedRequest = extractRequiredKeys(request.form, objectKeys)

	uid = authenticateToken(request.form['access_token'])
	processedRequest['uid'] = uid

	result = log_ctrl.logTask(processedRequest)
	if result is None:
		return dumps("IT DIDN'T WORK")
	return dumps(str(result))


# getUserLogEntries(access_token)
@application.route('/API/getUserLogEntries/', methods=["POST"])
def getUserLogEntries():
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


@application.route('/API/signOutUser/', methods=['POST'])
def signOutUser():
	necessaryKeys = ["access_token"]
	objectKeys = ["access_token"]
	processedRequest = extractRequiredKeys(request.form, objectKeys)

	if not verifyNecessaryRequestKeys(request.form, necessaryKeys):
		return dumps("Invalid Request: Items Missing")

	uid = authenticateToken(request.form['access_token'])
	processedRequest['uid'] = uid

	result = user_ctrl.signOutUser(processedRequest)
	if result is None:
		return dumps("IT DIDN'T WORK")
	return dumps(str(result))


###############################################################################
#
###############################################################################


if __name__ == "__main__":
	application.run(debug=True, host='0.0.0.0', port=8000)
