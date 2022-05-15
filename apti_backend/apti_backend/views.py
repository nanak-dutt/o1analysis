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
    # print("lvl-1")
    if(request.method == 'POST'):    
        # print("lvl-2")    
        serializer = UserSerializer(data=request.data)
        
        # print("lvl-3")
        
        if(serializer.is_valid()):            
            data=serializer.data
            
            # print("lvl-4")
            
            print(data)
        
            Name = data['Name']
            Email = data['Email']
            College = data['College']
            Key = data['Key']

            dict = {
                'Name': Name,
                'Email': Email,
                'College': College,
                'Key': Key,
            }

            if(check_email_exist(Email)==1):
                messages.error(request, 'EMAIL ALREADY EXIST',extra_tags='email')
                print("EMAIL ALREADY EXIST")
                return Response(status=status.HTTP_400_BAD_REQUEST)
            
            if(check_college_exist(College)==0):
                messages.success(request, 'COLLEGE DOES NOT EXIST', extra_tags='college')
                print("COLLEGE DOES NOT EXIST")
                return Response(status=status.HTTP_400_BAD_REQUEST)
            
            Password=get_college_key(College)
            
            print(Password)
            print(Key)                
            
            if(Key==Password):
                print("MATCHED")
                create_user(dict)
                messages.success(request, 'REGISTERED SUCCESSFULLY', extra_tags='register')
                return Response(status=status.HTTP_201_CREATED)
            else:
                print("NOT MATCHED")
                messages.success(request, 'WRONG KEY', extra_tags='key')
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            
        else:
            messages.error(request, 'INVALID DATA', extra_tags='create')
            return Response(status=status.HTTP_400_BAD_REQUEST)               
    
    messages.error(request, 'NO POST FOUND', extra_tags='create')    
    return Response(status=status.HTTP_401_UNAUTHORIZED)

# {
#     "Name": "DemoUser1",
#     "Email": "demouser1@gmail.com",
#     "College": "RCOEM",
#     "Key": "RCOEM-123"
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
        
            Email = data['Email']
            College = data['College']
            Key = data['Key']

            dict = {
                'Email': Email,
                'College': College,
                'Key': Key,
            }

            if(check_email_exist(Email)==0):
                messages.error(request, 'EMAIL DOES NOT EXIST',extra_tags='email')
                print("EMAIL DOES NOT EXIST")
                return Response(status=status.HTTP_400_BAD_REQUEST)
            
            clg=get_college_name(Email)
            print(clg)
            print(College)
            
            if(clg!=College):
                messages.success(request, 'WRONG COLLEGE NAME', extra_tags='college')
                print("WRONG COLLEGE NAME")
                return Response(status=status.HTTP_400_BAD_REQUEST)
            
            Password=get_college_key(College)
            
            print(Password)
            print(Key)                
            
            if(Key==Password):
                print("MATCHED")
                print("LOGGED IN SUCCESFULLY")
                messages.success(request, 'LOGGED IN SUCCESSFULLY', extra_tags='login')
                return Response(status=status.HTTP_201_CREATED)
            else:
                print("NOT MATCHED")
                messages.success(request, 'WRONG KEY', extra_tags='key')
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            
        else:
            messages.error(request, 'INVALID DATA', extra_tags='create')
            return Response(status=status.HTTP_400_BAD_REQUEST)               
    
    messages.error(request, 'NO POST FOUND', extra_tags='create')    
    return Response(status=status.HTTP_401_UNAUTHORIZED)

# {
#     "Email": "demouser1@gmail.com",
#     "College": "RCOEM",
#     "Key": "RCOEM-123"
# }