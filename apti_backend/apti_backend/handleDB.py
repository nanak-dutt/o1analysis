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
		return 1;
	except:
		print("ERROR IN CREATE_USER")
		return 0;


def check_id_exist(uid):
	try:
		user = db.collection('user').document(uid).get()
		if(user.exists):
			return 1
		else:
			return 0
	except:
		print("ERROR IN CHECK_USER_EXIST")
		return -1


def check_college_exist(college):
	try:
		data = db.collection('college').where("college_name", "==", college).get()
		if(len(data) == 0):
			return 0
		else:
			return 1
	except:
		print("ERROR IN CHECK_COLLEGE_EXIST")
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


def get_global_ranklist():
	users_ref = db.collection(u'user')
	query = users_ref.order_by(u'total_score', direction=firestore.Query.DESCENDING).stream()

	lst = []
	for doc in query:
		data = doc.to_dict()
		data.pop("level_wise_distribution")
		data.pop("topic_wise_distribution")
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

	return lst


def update_scored_db(totaldb, scores, level_wise_distribution, topic_wise_distribution, status, u_id):
	db.collection('user').document(u_id).update({
		'status': status,
		'total_score': totaldb,
		'scores': scores,
		'level_wise_distribution': level_wise_distribution,
		'topic_wise_distribution': topic_wise_distribution
	})


def set_questions(request):
	sa = gspread.service_account(filename="credentials.json")
	sh = sa.open_by_url(
		'https://docs.google.com/spreadsheets/d/1qExATJ3cdvzzv6vDIPqtRssx2QM4UnTBjXsqDfAVHho/edit?usp=sharing')
	wks = sh.worksheet("Sheet1")

	d = wks.get_all_records()

	for i in d:
		document_reference = db.collection('ques_bank').document()
		document_reference.set(i)


def get_user_responses(email):
	sa = gspread.service_account(filename="credentials.json")
	sh = sa.open_by_url(
		'https://docs.google.com/spreadsheets/d/1xygPuSLb4B4V3ps1SB9zWxXiADdZu_Hqx2YuluketEc/edit#gid=222477231')
	wks = sh.worksheet("Sheet1")

	d = wks.get_all_values()
	for row in d:
		if row[1] == email:
			return row

	return None