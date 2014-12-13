from django.shortcuts import render
from django.http import HttpResponse


from expense.models import *
from user_management.models import User
# Create your views here.


def add(request):
    admin = User.objects.first()
    Expenses.objects.create(amount=111, spender=admin, tag='again,lunch')
    return HttpResponse('added the default expense')

def index(request):
    expenses = Expenses.objects.all()
    return render(request, 'expense_table.html',{'expenses':expenses })
