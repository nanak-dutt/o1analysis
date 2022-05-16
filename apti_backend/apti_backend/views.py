from django.http import HttpResponse, JsonResponse,render
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
import requests
import gspread

from .handleDB import get_all_questions


@api_view(['GET'])
def testing_function(request):
    questions = get_all_questions()
    print(questions)
    return JsonResponse(questions)

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
    # to test wheater response dict is correct or not
    # print(ans)

    #change here to return dict instead of http response
    return HttpResponse("Hello")

