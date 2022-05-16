import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("credentials.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def get_all_questions():
	data = {}
	questions = db.collection("ques_bank").get()

	for q in questions:
		doc_id = q.id
		document = db.document("ques_bank", doc_id).get().to_dict()
		data[doc_id] = document

	print(data)
	return data


