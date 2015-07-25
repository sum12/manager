from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from rest_framework import viewsets, authentication, permissions, filters
from .serializers import UserSerializer
import json

User = get_user_model()

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
     return HttpResponse('Users are being resurected!!!')


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


class UserViewSet(DefaultsMixin, viewsets.ReadOnlyModelViewSet):
   lookup_field = User.USERNAME_FIELD
   lookup_url_kwargs = User.USERNAME_FIELD
   queryset = User.objects.order_by(User.USERNAME_FIELD)
   serializer_class = UserSerializer
   search_fields = (User.USERNAME_FIELD, )
