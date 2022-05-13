from django.http.response import HttpResponse
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
import requests

from .getDBHandle import getDBConnection

db = getDBConnection()

@api_view(['GET'])
def testing_function(request):
    uid='iMqfNi59SgXk4hz4nsVE'
    user_ref = db.collection(u'user').document(uid).get().to_dict()
    print(user_ref)
    return user_ref

	
