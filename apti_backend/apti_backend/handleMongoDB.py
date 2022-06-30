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


def get_global_ranklist(subject = None):
	if subject == "overall":
		user_data = user_collection.find({"total_score":{"$ne": None}}).sort("total_score", -1)
	else:
		user_data = user_collection.find({"scores":{"$ne": None}}).sort("scores.{subj}".format(subj = subject), -1)

	data = []
	rank = 0
	for user in user_data:
		if subject == "overall":
			score = user.get("total_score")
		else:
			score = user.get("scores").get(subject)

		if len(data) > 0 and score == data[-1].get("total_score"):
			pass
		else:
			rank += 1

		data.append({
			"name": user.get("name"),
			"email": user.get("email"),
			"college": user.get("college"),
			"mobile": user.get("mobile"),
			"total_score": score,
			"rank": rank
		})

	return data


def get_college_ranklist(college, subject = None):
	if subject == "overall":
		user_data = user_collection.find({"total_score":{"$ne": None}, "college":college}).sort("total_score", -1)
	else:
		user_data = user_collection.find({"scores":{"$ne": None}, "college":college}).sort("scores.{subj}".format(subj = subject), -1)

	data = []
	rank = 0
	for user in user_data:
		if subject == "overall":
			score = user.get("total_score")
		else:
			score = user.get("scores").get(subject)

		if len(data) > 0 and score == data[-1].get("total_score"):
			pass
		else:
			rank += 1

		data.append({
			"name": user.get("name"),
			"email": user.get("email"),
			"college": user.get("college"),
			"mobile": user.get("mobile"),
			"total_score": score,
			"rank": rank
		})

	return data


def update_scored_db(email, totalscore, scores):
	if user_collection.find_one({"email" : email}) is None:
		print("No user found to update db")
		return -1

	res = user_collection.update_one({"email" : email}, { "$set": { "total_score":totalscore, "scores" : scores } })
	return 1