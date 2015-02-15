from django.shortcuts import render
from django.http import HttpResponse,HttpResponseBadRequest,HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
import json
import re
import random
#    from django.utils import simplejson as json


from expense.models import *
from user_management.models import User

from django.core import serializers
# Create your views here.
import logging
logger = logging.getLogger(__name__)

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
    requestData = dict(json.loads(request.body))
    logger.error(dict(json.loads(request.body))['pk'])
    #TODO: This is a hack, possible bug in the xeditatble.js
    #      In case when post contains an javascript dict kind
    #      of object it is unable to parse in and sending `value`
    #      dict without any keys, so it has to be retried as a list.
    if requestData['pk'] and requestData['name']:
        logger.error('value = %s'%requestData['value'])
        exp=Expenses.objects.get(id=int(requestData['pk']))
        logger.error(exp)
        try:
            if 'sharedWith' in requestData['name']: 
                requestData['value'] = map(int,requestData['value'])
                deleteWits = list(set([u.wit.id for u in exp.sharedexpense_set.all()]) - set(requestData['value']))
                logger.debug(deleteWits)
                logger.error('value = %s'%requestData['value'])
                addWits = list(set(requestData['value']) - set([u.wit.id for u in exp.sharedexpense_set.all()])) 
                [sharedExpense.objects.get(exp__id=exp.id,wit__id=u).delete() for u in deleteWits]
                for uid in requestData['value']:
                    logger.debug("uid=%s"%uid)
                    usr = User.objects.get(id=int(uid))
                    sharedExpense(exp=exp,wit=usr).save() 
            elif 'returned' in requestData['name']:
                requestData['value'] = map(int,requestData['value'])
                deleteWits = list(set([u.wit.id for u in exp.sharedexpense_set.all()]) - set(requestData['value']))
                addWits = list(set(requestData['value']) - set([u.wit.id for u in exp.sharedexpense_set.all()]))
                try:
                    for u in deleteWits:
                        obj = sharedExpense.objects.get(exp__id=exp.id,wit__id=u)
                        obj.returned = False
                        obj.save()
                    for u in addWits:
                        obj = sharedExpense.objects.get(exp__id=exp.id,wit__id=u)
                        obj.returned = True
                        obj.save()
                except: 
                    email = User.objects.get(id=u)
                    raise Exception('Expense not shared with that person %s'%email)
            else:
                try: 
                    if requestData['name'] == 'amount' and int(requestData['value'])<0:
                        raise Exception('Did you really spend that!!!')
                    setattr(exp,requestData['name'],requestData['value']) 
                except :  
                    raise Exception('WOW!! what a number!!')
                exp.save()
        except Exception, err:
            response['success']=False
            response['msg']=str(err)
            return HttpResponseBadRequest(json.dumps(response['msg']),content_type="text/html")
    return HttpResponse(json.dumps(response),content_type="text/html")

@csrf_exempt
def log(request):
    logger.debug(request.POST)
    return HttpResponse(json.dumps(request.POST),content_type='text/application')


def shared(request,user_id):
    try:
        try:
           nexpenses = reduce(lambda x,y:x.append(y),[Expenses.objects.filter(id=sharedWithMe.exp.id) for sharedWithMe in sharedExpense.objects.filter(wit__id=user_id)])
        except:
            raise Exception('No shared expense with you')
        removeTheseOptions = {}
        removeTheseOptions['objId'] = ''
        removeTheseOptions['url'] = ''
        removeTheseOptions['wit'] = user_id
        #expenses = [exp.dump(removeTheseOptions.append({'amount':exp.amount/len(exp.sharedExpense_set.all())})) for exp in expenses]
        def addAmount(exp):
            subDict=dict(removeTheseOptions.items())
            subDict['amount']=exp.amount/(len(exp.sharedexpense_set.all())+1)
            return  subDict
        expenses = [exp.dump(addAmount(exp)) for exp in nexpenses]
        all_tag = json.dumps(list(set(",".join([t.tag for t in Expenses.objects.filter(spender_id=1)]).split(','))))
        many_friends = json.dumps({frnd.id:frnd.email for frnd in User.objects.get(id=1).many_friends.all()})
    except Exception,e:
        return HttpResponseBadRequest(str(e))

    return render(request, 'simple_expense_table.html',{'nexp':nexpenses,'expenses':expenses, 'all_tag':all_tag,'many_friends':many_friends})
#"/expense/answers/'+str(self.ques_id)+'/'+str(self.counter)+'/" '\

def simple(request):
    expenses = Expenses.objects.filter(spender_id=1)
    all_tag = json.dumps(list(set(",".join([t.tag for t in Expenses.objects.filter(spender_id=1)]).split(','))))
    many_friends = json.dumps({frnd.id:frnd.email for frnd in User.objects.get(id=1).many_friends.all()})
    return render(request, 'simple_expense_table.html',{'expenses':expenses, 'all_tag':all_tag,'many_friends':many_friends})

