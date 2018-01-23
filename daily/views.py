from rest_framework import viewsets, authentication, permissions, filters
from django.utils import timezone
from .models import activity, typeorder
from .serializers import ActivitySerializer, TypeOrderSerializer

import datetime as dt


class DefaultsMixin(object):
    authetication_classes = (
            authentication.BasicAuthentication,
            authentication.TokenAuthentication,
            )
    permission_classes = (
            permissions.IsAuthenticated,
            )
#    paginate_by = 25
#    pagination_param = 'page_size'
#    max_paginate = 100
    filter_backends = (
            filters.SearchFilter,
            filters.OrderingFilter,
            )


class DailyActivityViewSet(DefaultsMixin, viewsets.ModelViewSet):
    serializer_class = ActivitySerializer
    search_fields = ("type_order__type",)

    def get_queryset(self):
        try:
            days = int(self.request.query_params.get('days', 7))
        except:
            days = 7
        until = timezone.localtime() - dt.timedelta(days=days)
        qry = activity.objects
        qry = qry.filter(on__gte=until)
        return qry.all()


class TypeViewSet(DefaultsMixin, viewsets.ModelViewSet):
    serializer_class = TypeOrderSerializer
    queryset = typeorder.objects.all()
    search_fields = ("type",)
