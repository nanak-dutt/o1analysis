from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
import requests
from django.contrib import messages

from .handleDB import *
from .serializers import *

@api_view(['GET'])
def testing_function(request):
    questions = get_all_questions()
    print(questions)
    return JsonResponse(questions)



@api_view(['POST'])
def register(request):
    print("lvl-1")
    if(request.method == 'POST'):    
        print("lvl-2")    
        serializer = UserSerializer(data=request.data)

        print("lvl-3")

        if(serializer.is_valid()):            
            data=serializer.data

            print("lvl-4")

            print(data)

            name = data['name']
            email = data['email']
            college = data['college']
            key = data['key']
            mobile = data['mobile']

            dict = {
                'name': name,
                'email': email,
                'college': college,
                'mobile': mobile,
            }

            id=""
            str=email
            n=len(email)
            i=0
            while(i<n and str[i]!='@'):
                id+=str[i]
                i=i+1

            print(id)

            if(i==n):
                print("INVALID EMAIL")
                messages.error(request, 'INVALID EMAIL',extra_tags='@email')
                return Response(status=status.HTTP_400_BAD_REQUEST)
                

            if(check_id_exist(id)!=0):
                messages.error(request, 'EMAIL ALREADY EXIST',extra_tags='email')
                print("EMAIL ALREADY EXIST")
                return Response(status=status.HTTP_400_BAD_REQUEST)
            
            if(check_college_exist(college)!=1):
                messages.success(request, 'college DOES NOT EXIST', extra_tags='college')
                print("COLLEGE DOES NOT EXIST")
                return Response(status=status.HTTP_400_BAD_REQUEST)

            collegekey=get_college_key(college)

            print(collegekey)
            print(key)       
            
            if(collegekey==-1):
                print("KEY FINDING ERROR")
                messages.success(request, 'WRONG KEY', extra_tags='key')
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            
            if(key==collegekey):
                print("MATCHED")
                create_user(dict,id)
                messages.success(request, 'REGISTERED SUCCESSFULLY', extra_tags='register')
                return Response(status=status.HTTP_201_CREATED)
            else:
                print("NOT MATCHED")
                messages.success(request, 'WRONG key', extra_tags='key')
                return Response(status=status.HTTP_401_UNAUTHORIZED)

        else:
            messages.error(request, 'INVALID DATA', extra_tags='create')
            return Response(status=status.HTTP_400_BAD_REQUEST)               
    
    messages.error(request, 'NO POST FOUND', extra_tags='create')    
    return Response(status=status.HTTP_401_UNAUTHORIZED)

# {
# 	"name": "Demo User8",
# 	"email": "demouser8@gmail.com",
# 	"college": "Yeshwantrao Chavan College of Engineering",
#     "key": "YCCE",
#     "mobile": 8888888888
# }

@api_view(['POST'])
def login(request):
    # print("lvl-1")
    if(request.method == 'POST'):    
        # print("lvl-2")    
        serializer = UserLoginSerializer(data=request.data)
        
        # print("lvl-3")
        
        if(serializer.is_valid()):            
            data=serializer.data
            
            # print("lvl-4")
            
            print(data)
        
            email = data['email']
            college = data['college']
            key = data['key']

            dict = {
                'email': email,
                'college': college,
                'key': key,
            }
            
            id=""
            str=email
            n=len(email)
            i=0
            while(i<n and str[i]!='@'):
                id+=str[i]
                i=i+1

            print(id)

            if(check_id_exist(id)!=1):
                messages.error(request, 'EMAIL DOES NOT EXIST',extra_tags='email')
                print("EMAIL DOES NOT EXIST")
                return Response(status=status.HTTP_400_BAD_REQUEST)
            
            clg=get_college_name(id)
            print(clg)
            print(college)
            
            if(clg==0 or clg==-1):
                print("NO COLLEGE FOUND")
                messages.success(request, 'WRONG COLLEGE NAME', extra_tags='clg')
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            
            if(clg!=college):
                messages.success(request, 'WRONG COLLEGE NAME', extra_tags='college')
                print("WRONG college name")
                return Response(status=status.HTTP_400_BAD_REQUEST)
            
            collegekey=get_college_key(college)
            
            print(collegekey)
            print(key)           
            
            if(collegekey==-1):
                print("KEY FINDING ERROR")
                messages.success(request, 'WRONG KEY', extra_tags='key')
                return Response(status=status.HTTP_401_UNAUTHORIZED)     
            
            if(key==collegekey):
                print("MATCHED")
                print("LOGGED IN SUCCESFULLY")
                messages.success(request, 'LOGGED IN SUCCESSFULLY', extra_tags='login')
                return Response(status=status.HTTP_201_CREATED)
            else:
                print("NOT MATCHED")
                messages.success(request, 'WRONG key', extra_tags='key')
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            
        else:
            messages.error(request, 'INVALID DATA', extra_tags='create')
            return Response(status=status.HTTP_400_BAD_REQUEST)               
    
    messages.error(request, 'NO POST FOUND', extra_tags='create')    
    return Response(status=status.HTTP_401_UNAUTHORIZED)

# {
#     "email": "demouser8@gmail.com",
# 	"college": "Yeshwantrao Chavan College of Engineering",
#     "key": "YCCE",
# }