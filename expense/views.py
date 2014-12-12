from django.shortcuts import render
from django.http import HttpResponse


from expense.models import *
# Create your views here.


def index(request):
    return HttpResponse('Hello world')
