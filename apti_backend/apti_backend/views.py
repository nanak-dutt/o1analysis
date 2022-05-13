from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
import requests

from .handleDB import get_all_questions

@api_view(['GET'])
def testing_function(request):
    questions = get_all_questions()
    print(questions)
    return JsonResponse(questions)