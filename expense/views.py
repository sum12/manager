from django.shortcuts import render
from django.http import HttpResponse,HttpResponseBadRequest
import json
#    from django.utils import simplejson as json


from expense.models import *
from user_management.models import User

from django.core import serializers
# Create your views here.
import logging
logger = logging.getLogger(__name__)

def myfunction():
    logger.debug("this is a debug message!")

def myotherfunction():
    logger.error("this is an error message!!")

def add(request):
    admin = User.objects.first()
    Expenses.objects.create(amount=111, spender=admin, tag='again,lunch')
    return HttpResponse('added the default expense')

def index(request):
    expenses = Expenses.objects.all()
    expenses_json = serializers.serialize('json',expenses)
    many_friends = json.dumps([{'id':frnd.email,'text':frnd.email} for frnd in User.objects.get(id=1).many_friends.all()])
    return render(request, 'expense_table.html',{'expenses':expenses, 'expenses_json':expenses_json, 'many_friends':many_friends})

def save(request):
    response = {'success': True}
    #requestData = json.loads(request.body)
    requestData = request.POST.copy()
    logger.error(requestData.lists())
    #TODO: This is a hack, possible bug in the xeditatble.js
    #      In case when post contains an javascript dict kind
    #      of object it is unable to parse in and sending `value`
    #      dict without any keys, so it has to be retried as a list.
    if 'tag' in requestData['name'] :
        if 'value[]' in requestData:
            requestData['value']=",".join([y for x,y in requestData.lists() if x =='value[]'][0])
        else:
            requestData['value']=[]
    if 'sharedWith' in requestData['name']:
        if 'value[]' in requestData:
            requestData['value']=[User.objects.filter(id=int(i)) for i in ([y for x,y in requestData.lists() if x =='value[]'][0])]
        else:
            requestData['value']=[]
    logger.error(requestData['value'])
    if requestData['pk'] and requestData['name']:
        exp = Expenses.objects.get(id=requestData['pk'])
        try:
            if 'sharedWith' in requestData['name']:
                [i.delete() for i in sharedExpense.objects.filter(exp__id=exp.id)]
                [sharedExpense(exp=exp,wit=User.objects.get(id=i)).save() for i in requestData['value']]
            else:
                setattr(exp,requestData['name'],requestData['value'])
                exp.save()
        except Exception, err:
            response['success']=False
            response['msg']=str(err)
            return HttpResponseBadRequest(json.dumps(response),content_type="text/html")
    return HttpResponse(json.dumps(response),content_type="text/html")

def simple(request):
    expenses = Expenses.objects.filter(spender_id=1)
    all_tag = json.dumps(list(set(",".join([t.tag for t in Expenses.objects.filter(spender_id=1)]).split(','))))
    many_friends = json.dumps({frnd.id:frnd.email for frnd in User.objects.get(id=1).many_friends.all()})
    return render(request, 'simple_expense_table.html',{'expenses':expenses, 'all_tag':all_tag,'many_friends':many_friends})

