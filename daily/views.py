from rest_framework import viewsets
from .models import activity
from .serializers import ActivitySerializer
from rest_framework import viewsets, authentication, permissions, filters

import cStringIO
import datetime as dt

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
    search_fields = ("type",)

    def get_queryset(self):
        until = dt.datetime.today() - dt.timedelta(days=7)
        qry = activity.objects
        qry = qry.filter(on__gte=until)
        return qry.all()

