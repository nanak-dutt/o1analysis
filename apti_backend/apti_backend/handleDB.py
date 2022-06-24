import gspread
import json
import firebase_admin
from firebase_admin import credentials, firestore
from grpc import Status

cred = credentials.Certificate("credentials.json")
firebase_admin.initialize_app(cred)
db = firestore.client()


def get_all_questions():
	questions = db.collection("ques_bank").stream()
	data = []
	for q in questions:
		doc = q.to_dict()
		doc["id"] = q.id

		data.append(doc)

	return data


def get_all_colleges():
	colleges = db.collection("college").stream()
	data = []
	for q in colleges:
		doc = q.to_dict()
		data.append(doc['college_name'])
	return data


def get_correct_answers():
	questions = db.collection('ques_bank').stream()
	answers = {}
	for q in questions:
		doc = q.to_dict()
		answers[doc.get("no", -1)] = {
			"id" : q.id,
			"question" : doc.get("question"),
			"answer" : doc.get("answer"),
			"subject" : doc.get("subject"),
			"topic" : doc.get("topic"),
			"level" : doc.get("level")
		}
	return answers


def get_user_responses(email):
	sa = gspread.service_account(filename="credentials.json")
	config = json.load(open("config.json"))

	sh = sa.open_by_url(config["SHEET_URL"])
	wks = sh.worksheet("Form Responses 1")
	d = wks.get_all_values()

	for row in d:
		if row[1] == email:
			return row

	return None


def get_user_data(email):
	users = db.collection("user").where(u'email', u'==', email).get()

	if len(users) > 0:
		udata = users[0].to_dict()
		udata["id"] = users[0].id
		return udata

	return None


def create_user(data, uid):
	try:
		db.collection('user').document(uid).set(data)
		return 1
	except:
		print("ERROR IN CREATE_USER")
		return -1


def check_id_exist(uid):
	try:
		user = db.collection('user').document(uid).get()
		if(user.exists):
			return 1
		return 0
	except:
		print("ERROR IN CHECK_USER_EXIST")
		return -1


def check_college_exist(college):
	try:
		data = db.collection('college').where("college_name", "==", college).get()
		if(len(data) == 0):
			return 0
		return 1
	except:
		print("ERROR IN CHECK_COLLEGE_EXIST")
		return -1


def check_analytics_exist(uid):
	try:
		user = db.collection('user').document(uid).get()
		if (user.exists):
			user = user.to_dict()
			if user.get("level_wise_distribution") and user.get("scores") and user.get("topic_wise_distribution") and user.get("total_score"):
				return 1
		return 0
	except:
		print("ERROR IN CHECK_ANALYTICS_EXIST")
		return -1


def get_college_name(uid):
	try:
		user = db.collection('user').document(uid).get()
		if(user.exists):
			user = user.to_dict()
			return user['college']
		else:
			return 0
	except:
		print("ERROR IN GET_COLLEGE_NAME")
		return -1


def get_college_key(college):
	try:
		data = db.collection('college').where("college_name", "==", college).get()
		if(len(data)==0):
			return 0
		else:
			college = data[0].to_dict()
			return college['college_key']
	except:
		print("ERROR IN GET_COLLEGE_KEY")
		return -1


def get_test_link():
	testlink = db.collection(u'testlink').get()
	try:
		link = testlink[0].to_dict()['link']
		return link
	except Exception as e:
		print("ERROR IN GET_TEST_LINK")
		print(e)
		return -1


def get_global_ranklist():
	users_ref = db.collection(u'user')
	query = users_ref.order_by(u'total_score', direction=firestore.Query.DESCENDING).stream()

	lst = []
	i = 1
	for doc in query:
		data = doc.to_dict()
		data.pop("level_wise_distribution")
		data.pop("topic_wise_distribution")
		data["rank"] = i
		data["marks"] = data.pop("total_score")
		i += 1
		lst.append(data)

	return lst


def get_college_ranklist(college):
	users_ref = db.collection(u'user').where(u"college", u"==", college)
	query = users_ref.order_by(u'total_score', direction=firestore.Query.DESCENDING).stream()

	lst = []
	for doc in query:
		data = doc.to_dict()
		data.pop("level_wise_distribution")
		data.pop("topic_wise_distribution")
		data.pop("college")
		lst.append(data)

	i = 1
	actual_ranklist = {}
	for scores in lst:
		actual_ranklist[i] = scores
		i+=1

	return actual_ranklist


def update_scored_db(totaldb, scores, level_wise_distribution, topic_wise_distribution, uid):
	try:
		db.collection('user').document(uid).update({
			'total_score': totaldb,
			'scores': scores,
			'level_wise_distribution': level_wise_distribution,
			'topic_wise_distribution': topic_wise_distribution
		})
	except Exception as e:
		print("ERROR IN UPDATE_SCORED_DB")
		return -1


def get_subject_ranklist(subject):
	my_list = []

	users = db.collection("user").get()
	for user in users:
		data = user.to_dict()
		if 'scores' in data.keys():
			scores = data['scores']
			if subject in scores.keys():
				marks = data['scores'][subject]
				user_rank_data = {
					'name': data['name'],
					'college': data['college'],
					'marks': marks
				}
				my_list.append(user_rank_data)

	my_list = sorted(my_list, key=lambda k: k['marks'], reverse=True)
	i = 1
	for user in my_list:
		user['rank'] = i
		i += 1

	return my_list