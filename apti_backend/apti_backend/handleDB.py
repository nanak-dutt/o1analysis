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



def get_all_college():
    clgs = db.collection('college').get()
    data=[]
    
    for clg in clgs:
        dict=clg.to_dict()
        data.append(dict)
        # print(dict)
        # print(dict['college_key'])
        
    return data



def get_all_user():
    
    user = db.collection('user').get()
    
    data=[]
    for user in user:
        dict=user.to_dict()
        data.append(dict)
        # print(dict)
    
        # print(user)
        # print(dict['Email'])

    return data
    
        

def create_user(dict,id):
    try:
        db.collection('user').document(id).set(dict)
        return 1;
    except:
        print("ERROR IN CREATE_USER")
        return 0;



def check_id_exist(id):
    try:
        user = db.collection('user').document(id).get()

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
    


def get_college_name(id):
    try:
        user = db.collection('user').document(id).get()
        
        if(user.exists):
            user=user.to_dict()
            return user['college']
        else:
            return 0

    except:
        print("ERROR IN GET_COLLEGE_Name")
        return -1




def get_college_key(college):
    try:
        data = db.collection('college').where("college_name", "==", college).get()
        
        if(len(data)==0):
            return 0
        else:
            for i in data:
                dict=i.to_dict()
                return dict['college_key']            
    except:
        print("ERROR IN GET_COLLEGE_KEY")
        return -1
    
    

# db.collection('user').document('demouser7').set({
# 	'name': 'Demo User7',
# 	'email': 'demouser7@gmail.com',
# 	'college': 'Yeshwantrao Chavan College of Engineering',
#     'mobile': 7777777777
# })

# dict_ck = {
# 	'college_name': 'Yeshwantrao Chavan College of Engineering',
# 	'college_key': 'YCCE',
# }
# db.collection('college').add(dict_ck)


    
    
