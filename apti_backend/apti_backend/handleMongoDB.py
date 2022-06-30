import pymongo
import gspread

client = pymongo.MongoClient("mongodb+srv://rishabh_rathi:qlMw1iYnur59VgCH@knowyourprep.kocnybk.mongodb.net/?retryWrites=true&w=majority")
db = client["o1apti"]

college_collection = db["colleges"]
quesbank_collection = db["question_bank"]
user_collection = db["users"]
config_collection = db["config"]


def get_all_questions():
	data = []
	for q in quesbank_collection.find():
		data.append({
			"no": q.get("no"),
			"question": q.get("question"),
			"answer": q.get("answer"),
			"subject": q.get("subject"),
			"topic": q.get("topic"),
			"level": q.get("level")
		})
	return data


def get_all_colleges():
	data = []
	for college in college_collection.find():
		data.append(college.get("name"))
	return data


def get_correct_answers():
	answers = {}
	for q in quesbank_collection.find():
		if q.get("subject") == "language":
			continue
		answers[q.get("no", -1)] = {
			"id" : q.get("_id"),
			"question" : q.get("question"),
			"answer" : q.get("answer"),
			"subject" : q.get("subject"),
			"topic" : q.get("topic"),
			"level" : q.get("level")
		}
	return answers


def get_language_answers(lang):
	answers = {}
	for q in quesbank_collection.find({"topic" : lang}):
		answers[q.get("no", -1)] = {
			"id" : q.get("_id"),
			"question" : q.get("question"),
			"answer" : q.get("answer"),
			"subject" : q.get("subject"),
			"topic" : q.get("topic"),
			"level" : q.get("level")
		}
	return answers


def get_user_responses(email):
	sa = gspread.service_account(filename="credentials.json")
	sheet_url = config_collection.find_one({"type" : "sheeturl"}).get("link")

	sh = sa.open_by_url(sheet_url)
	wks = sh.worksheet("Form Responses 1")
	d = wks.get_all_values()

	for row in d:
		if row[1] == email:
			return row

	return None


def get_user_data(email):
	user = user_collection.find_one({"email" : email})
	return user


def create_user(data):
	try:
		user_collection.insert_one(data)
		return 1
	except Exception as e:
		print("ERROR IN CREATE_USER")
		print(e)
		return -1


def get_college_key(college):
	data = college_collection.find_one({"name" : college})
	if data is None:
		return -1
	return data.get("key")


def get_test_link():
	testlink = config_collection.find_one({"type" : "testurl"}).get("link")

	if testlink is None:
		print("ERROR IN GET_TEST_LINK")
		return -1

	return testlink


def get_global_ranklist():
	data = []
	rank = 0
	for user in user_collection.find().sort("total_score", -1):
		if len(data) > 0 and user.get("total_score") == data[-1].get("total_score"):
			pass
		else:
			rank += 1

		data.append({
			"name": user.get("name"),
			"email": user.get("email"),
			"college": user.get("college"),
			"mobile": user.get("mobile"),
			"total_score": user.get("total_score"),
			"rank": rank
		})

	print(data)
	return data


def get_college_ranklist(college):
	data = []
	rank = 0
	for user in user_collection.find({"college" : college}).sort("total_score", -1):
		if len(data) > 0 and user.get("total_score") == data[-1].get("total_score"):
			pass
		else:
			rank += 1

		data.append({
			"name": user.get("name"),
			"email": user.get("email"),
			"college": user.get("college"),
			"mobile": user.get("mobile"),
			"total_score": user.get("total_score"),
			"rank": rank
		})

	print(data)
	return data


def update_scored_db(email, totalscore, scores):
	res = user_collection.update_one({"email" : email}, { "$set": { "total_score":totalscore, "scores" : scores } })
	if res.modified_count == 0:
		print("No user found to update db")
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
					'total_score': marks
				}
				my_list.append(user_rank_data)

	my_list = sorted(my_list, key=lambda k: k['total_score'], reverse=True)
	i = 1
	# print(my_list)
	for user in my_list:
		user['rank'] = i
		i += 1

	return my_list