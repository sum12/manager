from django.shortcuts import render
from django.http import HttpResponse
import json
#    from django.utils import simplejson as json


from expense.models import *
from user_management.models import User

from django.core import serializers
# Create your views here.


def add(request):
    admin = User.objects.first()
    Expenses.objects.create(amount=111, spender=admin, tag='again,lunch')
    return HttpResponse('added the default expense')

def index(request):
    expenses = Expenses.objects.all()
    expenses_json = serializers.serialize('json',expenses)
    return render(request, 'expense_table.html',{'expenses':expenses, 'expenses_json':expenses_json})

def save(request):
    response = {'success': True}
    #requestData = json.loads(request.body)
    requestData = request.POST
    if requestData['pk'] and requestData['name']:
        exp = Expenses.objects.get(id=requestData['pk'])
        setattr(exp,requestData['name'],requestData['value'])
        try:
            exp.save()
        except ValidationError, err:
            response['success']=False
            response['msg']=err[requestData['name']]
    return HttpResponse(json.dumps(response),content_type="text/html")

def simple(request):
    expenses = Expenses.objects.all()
    expenses_json = serializers.serialize('json',expenses)
    return render(request, 'simple_expense_table.html',{'expenses':expenses, 'expenses_json':expenses_json})

