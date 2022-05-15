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



def get_all_colleges():
    clgs = db.collection('Colleges').get()
    data=[]
    
    for clg in clgs:
        dict=clg.to_dict()
        data.append(dict)
        # print(dict)
        # print(dict['CollegeKey'])
        
    return data



def get_all_users():
    
    users = db.collection('Users').get()
    
    data=[]
    for user in users:
        dict=user.to_dict()
        data.append(dict)
        # print(dict)
    
        # print(user)
        # print(dict['Email'])

    return data
    
        

def create_user(dict):
    try:
        db.collection('Users').add(dict)
        return 1;
    except:
        print("ERROR IN CREATE_USER")
        return 0;



def check_email_exist(email):
    try:
        data = db.collection('Users').where("Email", "==", email).get()

        if(len(data) == 0):
            return 0
        else:
            return 1

    except:
        print("ERROR IN CHECK_USER_EXIST")
        return -1
    


def check_college_exist(college):
    try:
        data = db.collection('Colleges').where("CollegeName", "==", college).get()

        if(len(data) == 0):
            return 0
        else:
            return 1
    except:
        print("ERROR IN CHECK_COLLEGE_EXIST")
        return -1
    


def get_college_name(email):
    try:
        data = db.collection('Users').where("Email", "==", email).get()
        
        if(len(data)==0):
            return -1
        else:
            for i in data:
                dict=i.to_dict()
                return dict['College']            
    except:
        print("ERROR IN GET_COLLEGE_Name")
        return -1




def get_college_key(college):
    try:
        data = db.collection('Colleges').where("CollegeName", "==", college).get()
        
        if(len(data)==0):
            return -1
        else:
            for i in data:
                dict=i.to_dict()
                return dict['CollegeKey']            
    except:
        print("ERROR IN GET_COLLEGE_KEY")
        return -1
    
    
