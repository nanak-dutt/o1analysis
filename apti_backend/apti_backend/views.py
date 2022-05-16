from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
import requests

from .handleDB import get_all_questions, add_analytics_to_user, get_user_data, get_analysis, get_data_json
from .serializers import EmailSerializer


# {
#     "email": "parthdhorajiya2211@gmail.com"
# }



@api_view(['GET'])
def testing_function(request):
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

        return Response("Success")
    else:
        return Response("Invalid data", status = status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def db(request):
    u_id="demouser2"
    subject='overall'
    answers={1:'a',2:'b',3:'c',4:'c',5:'b',6:'b',7:'c',8:'a',9:'a',10:'b',11:'c',12:'c',13:'b',14:'b',15:'c',16:'a',17:'a',18:'b',19:'c',20:'d'}
    data = get_analysis(u_id,answers)
    data = get_data_json(subject,u_id)
    
    return JsonResponse(data)