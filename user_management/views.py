from django.shortcuts import render
from django.http import HttpResponse

import json
# Create your views here.

from user_management.models import User

def get_friends(request,user_id):
    response = {'success':True}
    response['msg']=''
    try:
        response['data']=[{'id':frnd.id,'value':frnd.username} for frnd in User.objects.get(id=user_id).many_friends.all()]
    except Exception, fault:
        response['msg']=str(fault)
        response['success']=False
    return HttpResponse(json.dumps(response['data']),content_type="text/html")

def index(request):
    return HttpResponse('Users are being resurected!!!')
