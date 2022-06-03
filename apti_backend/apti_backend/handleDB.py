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

def get_user_answers():
    questions= db.collection('ques_bank').stream()
    answers_temp={}
    for q in questions:
        doc=q.to_dict()
        no=doc['no']
        corr=doc['answer']
        answers_temp[no]=corr
        if(no%4==0 or no%5==0):
            answers_temp[no]="wrong answer"
    return answers_temp

def add_analytics_to_user(email, level, topics):
	"""
	level =
	{
		"os": {
			"hard": [3, 2, 1],
			"medium": [3, 1, 2],
			"easy": [3, 3, 0]
		},
		"dbms": {
			"hard": [3, 1, 2],
			"medium": [3, 1, 2],
			"easy": [3, 2, 1]
		},
		"dsa": {
			"hard": [3, 3, 0],
			"medium": [3, 2, 1],
			"easy": [3, 2, 1]
		},
		"cn": {
			"hard": [3, 0, 3],
			"medium": [3, 1, 2],
			"easy": [3, 2, 1]
		},
		"oops": {
			"hard": [3, 2, 1],
			"medium": [3, 3, 0],
			"easy": [3, 1, 2]
		},
		"verbal": {
			"hard": [3, 2, 1],
			"medium": [3, 3, 0],
			"easy": [3, 1, 2]
		},
		"logical": {
			"hard": [3, 2, 1],
			"medium": [3, 3, 0],
			"easy": [3, 1, 2]
		},
		"quantitative": {
			"hard": [3, 2, 1],
			"medium": [3, 3, 0],
			"easy": [3, 1, 2]
		}
	}
	"""
	users = db.collection("user").where(u'email', u'==', email).get()

	if len(users) > 0:
		uid = users[0].id
		db.collection("user").document(uid).update({
			"level_wise": level,
			"topic_wise": topics
		})

	return True


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
	i = 1
	for doc in query:
		data = doc.to_dict()
		data.pop("level_wise_distribution")
		data.pop("topic_wise_distribution")
		lst.append(data)
		# lst.append(i)
		# i += 1

	actual_ranklist = {}
	for scores in lst:
		actual_ranklist[i] = []
		actual_ranklist[i].append(scores)
		i+=1

	return actual_ranklist


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
		actual_ranklist[i] = []
		actual_ranklist[i].append(scores)
		i+=1

	return actual_ranklist


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

	d = wks.get_all_values()
	ans = {}
	k = 1
	m = 3
	n = 0
	# uid = 'demouser1'
	data = db.collection('user').document(uid).get()
	data = data.to_dict()
	# print(data['email'])

	for i in d:
		for j in i:
			if i[1] == data['email']:
				n = n + 1
				if n >= 3:
					ans[k] = str(j)
					k = k+1
	# to test wheater response dict is correct or not
	print(ans)

	answers_in_json = json.dumps(ans, indent=3)

	return answers_in_json


def leetcode_api(uid, subject):
    
    data = db.collection('user').document(uid).get()
    data = data.to_dict()

    arr_subjects = []
    arr_scores = []

    easyque_correct_count = 0
    medque_correct_count = 0
    hardque_correct_count = 0
    if (subject == 'all'):
        for key,value in data['level_wise_distribution'].items():
            arr_subjects.append(key)
            for key1,value1 in value.items():
                if(key1 == 'easy'):
                    easyque_correct_count = easyque_correct_count + value1[1]
                if(key1 == 'medium'):
                    medque_correct_count = medque_correct_count + value1[1]
                if(key1 == 'hard'):
                    hardque_correct_count = hardque_correct_count + value1[1]
        
        totalque_correct_count =  easyque_correct_count + medque_correct_count + hardque_correct_count    
    else:
        arr_subjects.append(subject)
        for key,value in data['level_wise_distribution'].items():
            if(key == subject):
                for key1,value1 in value.items():
                    if(key1 == 'easy'):
                        easyque_correct_count = easyque_correct_count + value1[1]
                    if(key1 == 'medium'):
                        medque_correct_count = medque_correct_count + value1[1]
                    if(key1 == 'hard'):
                        hardque_correct_count = hardque_correct_count + value1[1]
        
        totalque_correct_count =  easyque_correct_count + medque_correct_count + hardque_correct_count

    arr_scores.append(easyque_correct_count)
    arr_scores.append(medque_correct_count)
    arr_scores.append(hardque_correct_count)
    arr_scores.append(totalque_correct_count)

    arr_ezy_med_hard = ["easy","medium","hard","overall"]

    leetcode = {
        'correct_questions': arr_scores,
        'labels':arr_ezy_med_hard,
        'x-axis-labels' : arr_subjects,
    }

    leetcode_json = json.dumps(leetcode, indent = 4)
    
    return leetcode_json

def get_85percent_score():
    os_questions = db.collection("ques_bank").where(u'subject', u'==', 'OS').where(u'topic', u'==', 'scheduling').get()
    
    score=0
    
    for question in os_questions:
        dict = question.to_dict()
        
        if(dict['level']=='easy'):
            score=score+2
        elif(dict['level']=='medium'):
            score=score+4
        elif(dict['level']=='hard'):
            score=score+6
    
    # print(score)
    
    return (score*0.85)
