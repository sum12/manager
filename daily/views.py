from django.shortcuts import render_to_response
from django.http import HttpResponse

from rest_framework import viewsets
from .models import activity
from .serializers import ActivitySerializer
from rest_framework import viewsets, authentication, permissions, filters

import cStringIO
import matplotlib
import datetime as dt
matplotlib.use("Agg")
import matplotlib.pyplot as plt

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



def getGraph(request, *args, **kwargs):
    plt.close()
    fig, ax= plt.subplots(1)
    activity_type = kwargs['activity_type']
    obs = activity.objects.filter(type = activity_type).order_by('on')
    dates = []
    if activity_type == 'exercise':
        totals = []
        counts = []
        for ob in obs:
            dates.append(ob.on)
            splitted = ob.data.split(',')
            counts.append(len(splitted))
            totals.append(sum(int(i or 0) for i in splitted))
        ax.plot(dates, totals,'r-' , dates, counts, 'bs')
    fig.autofmt_xdate()
    graph_file = cStringIO.StringIO()
    fig.savefig(graph_file, format='png')
    return HttpResponse(graph_file.getvalue(), content_type="image/png")

