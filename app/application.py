from flask import *
from Controller.userController import UserController
from Controller.taskController import TaskController
from Controller.bonusController import BonusController
from Repositories.taskDatabase import TaskDatabase
from bson.json_util import dumps
import bson

application = app = Flask(__name__)

tdb = TaskDatabase("mongodb+srv://test_user0:riktXHrvxRuVkS6F@cluster0.heb4n.mongodb.net/test?retryWrites=true&w=majority", "test")
user_ctrl = UserController(tdb)
task_ctrl = TaskController(tdb)
bonus_ctrl = BonusController(tdb)


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
	# TODO: auth
	return bson.ObjectId('5f1adb931083a8b78f7f5ff2')


def stringToFloatArray(string):
	if string == "" or string == "[]":
		return []
	if string[0] == '[':
		string = string[1:-1]
	if string[-1] == ']':
		string = string[0:-2]

	stringArr = string.split(",")
	newArr = []
	for elem in stringArr:
		newArr.append(float(elem))
	return newArr


def stringToStringArray(string):
	if string == "" or string == "[]":
		return []

	if string[0] == '[':
		string = string[1:-1]
	if string[-1] == ']':
		string = string[0:-2]

	stringArr = string.split(",")
	newArr = []
	for elem in stringArr:
		newArr.append(elem.replace('"', '').replace("'", ""))
	return newArr


def verifyNecessaryRequestKeys(myMap: dict, necessaryKeys: list) -> bool:
	for key in necessaryKeys:
		try:
			myMap[key]
		except KeyError:
			return False
	return True


def extractRequiredKeys(myMap: dict, required: list) -> dict:
	newMap = {}
	for key in required:
		newMap[key] = myMap[key]
	return newMap


@application.route('/API/signInUser/', methods=['POST'])
def signInUser():
	necessaryKeys = ["access_token", "name", "email", "google_id"]
	objectKeys = ["name", "email", "google_id"]

	if not verifyNecessaryRequestKeys(request.form, necessaryKeys):
		return "Invalid Request: Items Missing"
	processedRequest = extractRequiredKeys(request.form, objectKeys)

	return dumps(user_ctrl.signInUser(processedRequest))


@application.route('/API/createTask/', methods=['POST'])
def createTask():
	necessaryKeys = ["access_token", "name", "description", "base_score", "category", "tags"]
	objectKeys = ["name", "description", "base_score", "category", "tags"]

	if not verifyNecessaryRequestKeys(request.form, necessaryKeys):
		return "Invalid Request: Items Missing"
	processedRequest = extractRequiredKeys(request.form, objectKeys)

	processedRequest['base_score'] = int(processedRequest['base_score'])
	processedRequest['tags'] = stringToStringArray(processedRequest['tags'])

	uid = authenticateToken(request.form['access_token'])
	processedRequest['uid'] = uid

	result = task_ctrl.createTask(processedRequest)
	if result is None:
		return "IT DIDN'T WORK"
	return str(result)


# createBonusRequest(access_token,task_id,data_source,bonus_name,input_label,upper_bound,lower_bound,evaluation_type,constants)
@application.route('/API/createBonus/', methods=['POST'])
def createBonus():
	necessaryKeys = ["access_token", "task_id", "data_source", "bonus_name", "input_label", "upper_bound", "lower_bound", "evaluation_type", "constants"]
	objectKeys = ["task_id", "data_source", "bonus_name", "input_label", "upper_bound", "lower_bound", "evaluation_type", "constants"]

	if not verifyNecessaryRequestKeys(request.form, necessaryKeys):
		return "Invalid Request: Items Missing"
	processedRequest = extractRequiredKeys(request.form, objectKeys)

	processedRequest['constants'] = stringToFloatArray(processedRequest['constants'])
	processedRequest['upper_bound'] = float(processedRequest['upper_bound'])
	processedRequest['lower_bound'] = float(processedRequest['lower_bound'])
	processedRequest['task_id'] = bson.ObjectId(processedRequest['task_id'])

	uid = authenticateToken(request.form['access_token'])
	processedRequest['uid'] = uid

	result = bonus_ctrl.createBonus(processedRequest)
	if result is None:
		return "IT DIDN'T WORK"
	return str(result)


###############################################################################
#
###############################################################################


if __name__ == "__main__":
	application.run(debug=True, host='0.0.0.0', port=8000)
