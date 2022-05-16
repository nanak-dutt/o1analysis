from collections import UserDict
import string
from unicodedata import name
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use the application default credentials
cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {
  'projectId': 'astute-charter-339619',
})

db = firestore.client()

# Add a new doc in collection 'user'
# UserDict={
#     "College": "Shri Ramdeobaba College of Engineering and Management",
#     "Email": "demouser8@gmail.com",
#     "Marks": 98,
#     "Name": "Demo User 8",
#     }

# db.collection(u'user').add(UserDict)   

# users_ref = db.collection(u'user')
# docs = users_ref.stream()

# for doc in docs:
#     print(f'{doc.id} => {doc.to_dict()}')

users_ref = db.collection(u'user')
query = users_ref.order_by(
    u'total_score', direction=firestore.Query.DESCENDING).get()

# For college sorting

# lst=[]
# for doc in query:
#     data = doc.to_dict()
#     if(data['college']=='Shri Ramdeobaba College of Engineering and Management'):
#         lst.append(data)
        
        
# For all India level sorting
lst=[]
for doc in query:
    data = doc.to_dict()
    lst.append(data)
    
    
# To print in string 

n=len(lst)

for i in range(0,n):
    str=""
    rank="{}".format(i+1)
    str+=rank
    total_score="{}".format(lst[i]['total_score'])
    str+=" "
    str+=(lst[i]['name'])
    str+=" "
    str+=total_score
    str+=" "
    str+=(lst[i]['college'])
    print(str)

    