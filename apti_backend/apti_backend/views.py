from django.http import HttpResponse, JsonResponse

from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
import requests

from .handleDB import *
from .serializers import *

"""
{
	"email": "parthdhorajiya2211@gmail.com"
}
"""
@api_view(['GET'])
def question_bank(request):
	questions = get_all_questions()
	return Response({"data" : questions}, status = status.HTTP_200_OK)


@api_view(['POST'])
def analytics(request):
	serializer = EmailSerializer(data = request.data)
	if serializer.is_valid():
		email = serializer.data['email']
		data = get_user_data(email)

		if data is None:
			return Response("No user found", status = status.HTTP_404_NOT_FOUND)

		print(data)

		return Response(data)
	else:
		return Response("Invalid data", status = status.HTTP_400_BAD_REQUEST)


"""
{
	"name": "Demo User8",
	"email": "demouser8@gmail.com",
	"college": "Yeshwantrao Chavan College of Engineering",
	"key": "YCCE",
	"mobile": 8888888888
}
"""
@api_view(['POST'])
def register(request):
	serializer = UserSerializer(data=request.data)

	if serializer.is_valid():
		data = serializer.data
		college = data['college']
		key = data['key']

		user_data = {
			'name': data['name'],
			'email': data['email'],
			'college': data['college'],
			'mobile': data['mobile'],
		}

		user_id = data["email"].split("@")[0]

		if check_id_exist(user_id)!=0:
			print("EMAIL ALREADY EXIST")
			return Response("EMAIL ALREADY EXIST", status=status.HTTP_400_BAD_REQUEST)

		if check_college_exist(college)!=1:
			print("COLLEGE DOES NOT EXIST")
			return Response("COLLEGE DOES NOT EXIST", status=status.HTTP_400_BAD_REQUEST)

		collegekey = get_college_key(college)

		if (collegekey==-1):
			print("KEY FINDING ERROR")
			return Response("KEY FINDING ERROR", status=status.HTTP_401_UNAUTHORIZED)

		if (key==collegekey):
			print("MATCHED")
			create_user(user_data, user_id)
			return Response("REGISTERED SUCCESSFULLY", status=status.HTTP_201_CREATED)
		else:
			print("NOT MATCHED")
			return Response("WRONG KEY", status=status.HTTP_401_UNAUTHORIZED)

	else:
		return Response("INVALID DATA", status=status.HTTP_400_BAD_REQUEST)


"""
{
	"email": "demouser8@gmail.com",
	"college": "Yeshwantrao Chavan College of Engineering",
	"key": "YCCE"
}
"""
@api_view(['POST'])
def login(request):
	serializer = UserLoginSerializer(data=request.data)

	if serializer.is_valid():
		data = serializer.data

		email = data['email']
		college = data['college']
		key = data['key']

		dict = {
			'email': email,
			'college': college,
			'key': key,
		}

		user_id = email.split("@")[0]

		if (check_id_exist(user_id)!=1):
			print("EMAIL DOES NOT EXIST")
			return Response("EMAIL DOES NOT EXIST", status=status.HTTP_401_UNAUTHORIZED)

		clg = get_college_name(user_id)

		if (clg==0 or clg==-1):
			print("WRONG COLLEGE NAME")
			return Response("WRONG COLLEGE NAME", status=status.HTTP_401_UNAUTHORIZED)

		if (clg!=college):
			print("WRONG COLLEGE NAME")
			return Response("WRONG COLLEGE NAME", status=status.HTTP_401_UNAUTHORIZED)

		collegekey = get_college_key(college)

		if(collegekey==-1):
			print("KEY FINDING ERROR")
			return Response("KEY FINDING ERROR", status=status.HTTP_401_UNAUTHORIZED)

		if(key==collegekey):
			print("LOGGED IN SUCCESFULLY")
			return Response("LOGGED IN SUCCESSFULLY", status=status.HTTP_200_OK)
		else:
			print("NOT MATCHED")
			return Response("WRONG key", status=status.HTTP_401_UNAUTHORIZED)

	else:
		return Response("INVALID DATA", status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def db(request):
	u_id="demouser5"
	subject='overall'
	answers={1:'a',2:'b',3:'c',4:'c',5:'b',6:'b',7:'c',8:'a',9:'a',10:'b',11:'c',12:'c',13:'b',14:'b',15:'c',16:'a',17:'a',18:'b',19:'c',20:'d'}
	data = get_analysis(u_id,answers)
	data = get_data_json(subject,u_id)

	return JsonResponse(data)


#Function To Return a dictionary containing user responses
@api_view(['GET'])
def user_responses(request):
	sa = gspread.service_account(filename="service_accounto1.json")
	sh = sa.open("responses")
	wks = sh.worksheet("Sheet1")

	d = wks.get_all_values()

	email = 'ritulrdeshmukh@gmail.com'  # put here the requested email id which will be obtained from frontend##
	ans = {}
	k = 1
	m = 3
	n = 0
	for i in d:
		for j in i:
			if i[1] == email:
				n = n + 1
				if n>=3:
					ans[k] = str(j)
					k = k+1
	#to test wheater response dict is correct or not
	# print(ans)

	#change here to return dict instead of http response
	return HttpResponse("Hello")

"""
{
	"college" : "Shri Ramdeobaba College of Engineering and Management"
}
"""
@api_view(['POST'])
def ranklist(request):
	serializer = CollegeRankListSerializer(data = request.data)
	if serializer.is_valid():
		college = serializer.data['college']
		lst = get_college_ranklist(college)
		data = {
			"ranklist" : lst
		}
		return Response(data, status = status.HTTP_200_OK)

	return Response(status = status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def globalranklist(request):
	lst = get_global_ranklist()
	data = {
		"ranklist" : lst
	}
	return Response(data, status = status.HTTP_200_OK)