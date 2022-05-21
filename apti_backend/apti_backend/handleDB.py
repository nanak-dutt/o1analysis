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

	data.sort(key = lambda x:x['no'])
	return data


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


<<<<<<< HEAD
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
		lst.append(data)

	return lst


def get_college_ranklist(college):
	users_ref = db.collection(u'user').where(u"college", u"==", college)
	query = users_ref.order_by(u'total_score', direction=firestore.Query.DESCENDING).stream()

	lst = []
	for doc in query:
		data = doc.to_dict()
		lst.append(data)

	return lst


def update_scored_db(totaldb,scores,level_wise_distribution,topic_wise_distribution,status,u_id):
    db.collection('user').document(u_id).update({'status':status})
    db.collection('user').document(u_id).update({'total_score':totaldb})
    db.collection('user').document(u_id).update({'scores':scores})
    db.collection('user').document(u_id).update({'level_wise_distribution':level_wise_distribution})
    db.collection('user').document(u_id).update({'topic_wise_distribution':topic_wise_distribution})
=======
def get_analysis(u_id,answers):
    
    ### this is temporary answers as no answers are available
    answers_temp={1:'a',2:'b',3:'c',4:'d',5:'a',6:'b',7:'c',8:'d',9:'a',10:'b',11:'c',12:'d',13:'a',14:'b',15:'c',16:'d',17:'a',18:'b',19:'c',20:'d'}
    datalist = db.collection("user").document(u_id).get()
    data=datalist.to_dict()
    
    status=0
    if('Status' in data):
        status=data['Status']
    else:
        data['Status']=0
    
    print(status)
    #### DB Fields
    totaldb=0
    scores={}
    level_wise_distribution={}
    topic_wise_distribution={}
    
    
    if(status==0):
        db.collection('user').document(u_id).update({'Status': 1 })
        Questions = db.collection('ques_bank').get()
        print("ENTERED")
        for quest in Questions:
            #print(question.to_dict())
            question=quest.to_dict()
            no=question['no']
            topic=question['subject']
            subtopic=question['topic']
            corr=question['answer']
            ### temporary
            checkanswer='0'
            if(no<=20):
                corr=answers_temp[no]
                checkanswer=answers[no]
            diff=question['level']
            
                 
            
            #### correct then
            if(checkanswer==corr and no<=20):
                # Update data with known key
                #db.collection('persons').document("p1").update({"age": 50}) # field already exists
                #db.collection('persons').document("p1").update({"age": firestore.Increment(2)}) # increment a field
        
                if(diff=='easy'):
                    totaldb=totaldb+2
                    #scores
                    if(topic in scores):
                        scores[topic]=scores[topic]+2
                    else:
                        scores[topic]=2
                    #level_wise
                    if(topic in level_wise_distribution):
                        level_wise_distribution[topic]['easy'][1]=level_wise_distribution[topic]['easy'][1]+1
                        level_wise_distribution[topic]['easy'][0]=level_wise_distribution[topic]['easy'][0]+2
                        
                    else:
                        level_wise_distribution[topic]={
							"hard":[0,0,0],
                            "medium":[0,0,0],
                            "easy":[2,1,0]
						}
                    #topic_wise
                    if(topic in topic_wise_distribution):
                        if(subtopic in topic_wise_distribution[topic]):
                            topic_wise_distribution[topic][subtopic][0]=topic_wise_distribution[topic][subtopic][0]+2
                            topic_wise_distribution[topic][subtopic][1]=topic_wise_distribution[topic][subtopic][1]+1
                        
                        else:
                            topic_wise_distribution[topic][subtopic]=[2,1,0]
                            
                    else:
                        topic_wise_distribution[topic]={}
                        topic_wise_distribution[topic][subtopic]=[2,1,0]
                        
                    
                if(diff=='medium'):
                    totaldb=totaldb+4
                    #scores
                    if(topic in scores):
                        scores[topic]=scores[topic]+4
                    else:
                        scores[topic]=4
                    #level_wise
                    if(topic in level_wise_distribution):
                        level_wise_distribution[topic]['medium'][1]=level_wise_distribution[topic]['medium'][1]+1
                        level_wise_distribution[topic]['medium'][0]=level_wise_distribution[topic]['medium'][0]+4
                        
                    else:
                        level_wise_distribution[topic]={
							"hard":[0,0,0],
                            "medium":[4,1,0],
                            "easy":[0,0,0]
						}
                    #topic_wise
                    if(topic in topic_wise_distribution):
                        if(subtopic in topic_wise_distribution[topic]):
                            topic_wise_distribution[topic][subtopic][0]=topic_wise_distribution[topic][subtopic][0]+4
                            topic_wise_distribution[topic][subtopic][1]=topic_wise_distribution[topic][subtopic][1]+1
                        
                        else:
                            topic_wise_distribution[topic][subtopic]=[4,1,0]
                            
                    else:
                        topic_wise_distribution[topic]={}
                        topic_wise_distribution[topic][subtopic]=[4,1,0]
                    
                if(diff=='hard'):
                    totaldb=totaldb+6
                    #scores
                    if(topic in scores):
                        scores[topic]=scores[topic]+6
                    else:
                        scores[topic]=6
                    #level_wise
                    if(topic in level_wise_distribution):
                        level_wise_distribution[topic]['easy'][1]=level_wise_distribution[topic]['easy'][1]+1
                        level_wise_distribution[topic]['easy'][0]=level_wise_distribution[topic]['easy'][0]+6
                        
                    else:
                        level_wise_distribution[topic]={
							"hard":[6,1,0],
                            "medium":[0,0,0],
                            "easy":[0,0,0]
						}
                    #topic_wise
                    if(topic in topic_wise_distribution):
                        if(subtopic in topic_wise_distribution[topic]):
                            topic_wise_distribution[topic][subtopic][0]=topic_wise_distribution[topic][subtopic][0]+6
                            topic_wise_distribution[topic][subtopic][1]=topic_wise_distribution[topic][subtopic][1]+1
                        
                        else:
                            topic_wise_distribution[topic][subtopic]=[6,1,0]
                            
                    else:
                        topic_wise_distribution[topic]={}
                        topic_wise_distribution[topic][subtopic]=[6,1,0]
                    
                
            elif(no<=20):
                if(diff=='easy'):
                    
                    #level_wise
                    if(topic in level_wise_distribution):
                        level_wise_distribution[topic]['easy'][2]=level_wise_distribution[topic]['easy'][2]+1
                        
                    else:
                        level_wise_distribution[topic]={
							"hard":[0,0,0],
                            "medium":[0,0,0],
                            "easy":[0,0,1]
						}
                        
                    #topic_wise
                    if(topic in topic_wise_distribution):
                        if(subtopic in topic_wise_distribution[topic]):
                            topic_wise_distribution[topic][subtopic][2]=topic_wise_distribution[topic][subtopic][2]+1
                        
                        else:
                            topic_wise_distribution[topic][subtopic]=[0,0,1]
                            
                    else:
                        topic_wise_distribution[topic]={}
                        topic_wise_distribution[topic][subtopic]=[0,0,1]
                        
                    
                if(diff=='medium'):
                    
                    #level_wise
                    if(topic in level_wise_distribution):
                        level_wise_distribution[topic]['medium'][2]=level_wise_distribution[topic]['medium'][2]+1
                        
                    else:
                        level_wise_distribution[topic]={
							"hard":[0,0,0],
                            "medium":[0,0,1],
                            "easy":[0,0,0]
						}
                    #topic_wise
                    if(topic in topic_wise_distribution):
                        if(subtopic in topic_wise_distribution[topic]):
                            topic_wise_distribution[topic][subtopic][2]=topic_wise_distribution[topic][subtopic][2]+1
                        
                        else:
                            topic_wise_distribution[topic][subtopic]=[0,0,1]
                            
                    else:
                        topic_wise_distribution[topic]={}
                        topic_wise_distribution[topic][subtopic]=[0,0,1]
                    
                if(diff=='hard'):
                    #level_wise
                    if(topic in level_wise_distribution):
                        level_wise_distribution[topic]['hard'][2]=level_wise_distribution[topic]['hard'][2]+1
                        
                    else:
                        level_wise_distribution[topic]={
							"hard":[0,0,1],
                            "medium":[0,0,0],
                            "easy":[0,0,0]
						}
                    #topic_wise
                    if(topic in topic_wise_distribution):
                        if(subtopic in topic_wise_distribution[topic]):
                            topic_wise_distribution[topic][subtopic][2]=topic_wise_distribution[topic][subtopic][2]+1
                        
                        else:
                            topic_wise_distribution[topic][subtopic]=[0,0,1]
                            
                    else:
                        topic_wise_distribution[topic]={}
                        topic_wise_distribution[topic][subtopic]=[0,0,1]
        
        print(level_wise_distribution)
        db.collection('user').document(u_id).update({'total_score':totaldb})
        db.collection('user').document(u_id).update({'scores':scores})
        db.collection('user').document(u_id).update({'level_wise_distribution':level_wise_distribution})
        db.collection('user').document(u_id).update({'topic_wise_distribution':topic_wise_distribution})

                
    else:
        print("alredy exist")
        
    tempreturn={}
    return tempreturn
        
        
def get_data_json(subject,u_id):
    if(subject=='overall'):
        datalist = db.collection("user").document(u_id).get()
        data1=datalist.to_dict()

        namer=data1['name']
        
        subject1=[]
        correct=[]
        incorrect=[]
        hard=0
        medium=0
        easy=0
        
        for sub in data1['level_wise_distribution']:
            innerdata=data1['level_wise_distribution'][sub]
            subject1.append(sub)
            hard=hard+innerdata['hard'][0]
            medium=medium+innerdata['medium'][0]
            easy=easy+innerdata['easy'][0]
            correct.append(innerdata['hard'][1]+innerdata['medium'][1]+innerdata['easy'][1])
            incorrect.append(innerdata['hard'][2]+innerdata['medium'][2]+innerdata['easy'][2])
            
            
        subject2=[]
        scores_subject=[]
        
        for sub in data1['scores']:
            subject2.append(sub)
            scores_subject.append(data1['scores'][sub])   
            



        returndata={
                'name': namer,
                'leetcode': {
                'series': [hard, medium, easy],
                'labels': ["Hard", "Medium", "Easy"],
                },
                'stackgraph': {
                'series': [
                    {
                    'name': "Correct",
                    'data': correct,
                    },
                    {
                    'name': "Incorrect",
                    'data': incorrect,
                    },
                ],
                'labels': subject1,
                },
                'linegraph': {
                'labels': subject2,
                'series': [
                    {
                    'name': "Subjects",
                    'data': scores_subject,
                    },
                ],
                },
                'piechart': {
                'series': scores_subject,
                'labels': subject2,
                },
            }

        datareturn=returndata
        print(type(datareturn)) 
    
    else:
        datareturn={subject:" subject wise data"}
        
    return datareturn 
>>>>>>> 172a66b37acd7535760c2e083f1189f89cda5a3c
