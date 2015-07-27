from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from rest_framework import viewsets, authentication, permissions, filters
from .serializers import PersonSerializer, FriendSerializer
from .models import Friend
import json

Person = get_user_model()

def get_friends(request,user_id):
    response = {'success':True}
    response['msg']=''
    try:
        response['data']=[{'id':frnd.id,'text':frnd.email} for frnd in Person.objects.get(id=user_id).many_friends.all()]
    except Exception, fault:
        response['msg']=str(fault)
        response['success']=False
    return HttpResponse(json.dumps(response['data']),content_type="text/html")

def index(request):
     return HttpResponse('Persons are being resurected!!!')


class DefaultsMixin(object):
    authetication_classes = (
            authentication.BasicAuthentication,
            authentication.TokenAuthentication,
            )
    permission_classes = (
            #permissions.IsAuthenticated,
            )
    paginate_by = 25
    pagination_param = 'page_size'
    max_paginate = 100
    filter_backends=(
            filters.SearchFilter,
            filters.OrderingFilter,
            )


class PersonViewSet(DefaultsMixin, viewsets.ModelViewSet):
   lookup_field = Person.USERNAME_FIELD
   lookup_url_kwargs = Person.USERNAME_FIELD
   queryset = Person.objects.order_by(Person.USERNAME_FIELD)
   serializer_class = PersonSerializer
   search_fields = (Person.USERNAME_FIELD, )


class FriendViewSet(DefaultsMixin, viewsets.ModelViewSet):
   lookup_field = Person.USERNAME_FIELD
   lookup_url_kwargs = Person.USERNAME_FIELD
   queryset = Friend.objects.all()
   serializer_class = FriendSerializer
   search_fields = ('=f1__id',)

