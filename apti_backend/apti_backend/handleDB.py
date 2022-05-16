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
		"quants": {
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
		uid = users[0].id
		udata = users[0].to_dict()
		return {uid : udata}

	return None


def get_analysis(u_id,answers):
    
    ### this is temporary answers as no answers are available
    answers_temp={1:'a',2:'b',3:'c',4:'d',5:'a',6:'b',7:'c',8:'d',9:'a',10:'b',11:'c',12:'d',13:'a',14:'b',15:'c',16:'d',17:'a',18:'b',19:'c',20:'d'}
    datalist = db.collection("user").document(u_id).get()
    data=datalist.to_dict()
    
    status=1
    if('Status' in data):
        status=data['Status']
    
    print(status)
    #### DB Fields
    totaldb=0
    scores={}
    level_wise_distribution={}
    topic_wise_distribution={}
    
    
    if(status==0):
        db.collection('user').document(u_id).update({'Status': 1 })
        Questions = db.collection('ques_bank').get()
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