from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
import requests

from .handleDB import get_all_questions, add_analytics_to_user, get_user_data
from .serializers import EmailSerializer

"""
{
    "email": "parthdhorajiya2211@gmail.com"
}
"""

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