from django.shortcuts import render_to_response

from rest_framework import viewsets
from .models import Expenses
from .serializers import ExpenseSerializer
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
