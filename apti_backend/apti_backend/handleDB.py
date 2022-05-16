import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("credentials.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def get_all_questions():
	questions = db.collection("ques_bank").stream()
	data = []

	for q in questions:
		_id = q.id
		doc = q.to_dict()
		doc["id"] = _id
		data.append(doc)

	print(data)
	return data


