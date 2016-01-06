from django.shortcuts import render_to_response

from rest_framework import viewsets
from .models import activity
from .serializers import ActivitySerializer
from rest_framework import viewsets, authentication, permissions, filters

import logging
logger = logging.getLogger(__name__)

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

class DailyActivityViewSet(DefaultsMixin, viewsets.ModelViewSet):
    serializer_class = ActivitySerializer
    queryset = activity.objects.all()
    search_fields = ("type",)

