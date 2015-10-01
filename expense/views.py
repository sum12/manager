from django.shortcuts import render, render_to_response
from django.http import HttpResponse,HttpResponseBadRequest,HttpResponseNotFound
from django.contrib.auth import get_user_model
import json
import re
import random

from expense.models import *
User = get_user_model()

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
    requestData = request.POST.copy()
    #logger.error(requestData.lists())
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
            requestData['value']=[User.objects.get(id=int(i)) for i in ([y for x,y in requestData.lists() if x =='value[]'][0])]
        else:
            requestData['value']=[]
    if 'returned' in requestData['name']:
        if 'value[]' in requestData:
            requestData['value']=[User.objects.get(id=int(i)) for i in ([y for x,y in requestData.lists() if x =='value[]'][0])]
        else:
            requestData['value']=[]
    if requestData['pk'] and requestData['name']:
        logger.error('name = %s'%requestData['name'])
        logger.error('value = %s'%requestData['value'])
        exp=Expenses.objects.get(id=int(requestData['pk']))
        try:
            if 'sharedWith' in requestData['name']: 
                deleteWits = set([u.wit for u in exp.sharedexpense_set.all()]) - set(requestData['value'])
                addWits = set(requestData['value']) - set([u.wit for u in exp.sharedexpense_set.all()]) 
                [sharedExpense.objects.get(exp__id=exp.id,wit__id=u.id).delete() for u in deleteWits]
                [sharedExpense(exp=exp,wit=u).save() for u in addWits]
            elif 'returned' in requestData['name']:
                try: 
                    map(lambda x :setattr(x,requestData['name'],False), exp.sharedexpense_set.all()) 
                except: 
                   raise Exception('Expense is not shared')
                try:
                    for u in requestData['value']:
                        sharedexp = sharedExpense.objects.get(exp__id=exp.id,wit__id=u.id)
                        setattr(sharedexp,requestData['name'],True)
                        sharedexp.save()
                except: 
                    raise Exception('Expense not shared with that person %s'%u.email)
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


from rest_framework import viewsets
from .models import Expenses
from .serializers import ExpenseSerializer
from rest_framework import viewsets, authentication, permissions, filters

class DefaultsMixin(object):
    authetication_classes = (
            authentication.BasicAuthentication,
            authentication.TokenAuthentication,
            )
    permission_classes = (
            #permissions.IsAuthenticated,
            )
#    paginate_by = 25
#    pagination_param = 'page_size'
#    max_paginate = 100
    filter_backends=(
            filters.SearchFilter,
            filters.OrderingFilter,
            )

class ExpenseViewSet(DefaultsMixin, viewsets.ModelViewSet):

    serializer_class = ExpenseSerializer
    search_fields = ("tag",)

    def get_queryset(self):
        qry = Expenses.objects
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        if year: qry=qry.filter(dateAdded__year=int(year))
        if month: qry=qry.filter(dateAdded__month=int(month))
        if day: qry=qry.filter(dateAdded__day=int(day))
        return qry.all()
        


def expense_csv(request, year=None, month=None, day=None):
    qry = Expenses.objects.filter(tag__contains="shared")
    if year: qry=qry.filter(dateAdded__year=int(year))
    if month: qry=qry.filter(dateAdded__month=int(month))
    if day: qry=qry.filter(dateAdded__day=int(day))
    return render_to_response('exp.csv', {'expenses': qry }, content_type="text/csv")



