from rest_framework import viewsets, authentication, permissions, filters
from rest_framework.decorators import list_route
from rest_framework.response import Response

from .models import Expenses
from .serializers import ExpenseSerializer


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


class ExpenseViewSet(DefaultsMixin, viewsets.ModelViewSet):

    serializer_class = ExpenseSerializer
    search_fields = ("tag",)

    def get_queryset(self):
        qry = Expenses.objects
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        if year:
            qry = qry.filter(dateAdded__year=int(year))
        if month:
            qry = qry.filter(dateAdded__month=int(month))
        if day:
            qry = qry.filter(dateAdded__day=int(day))
        return qry.all()

    @list_route(methods=['get'])
    def tagsums(self, request):
        qry = Expenses.objects.order_by('dateAdded')
        year = self.request.query_params.get('year')
        month = self.request.query_params.get('month')
        day = self.request.query_params.get('day')
        if year:
            qry = qry.filter(dateAdded__year=int(year))
        if month:
            qry = qry.filter(dateAdded__month=int(month))
        if day:
            qry = qry.filter(dateAdded__day=int(day))
        rows = list(qry.all())
        alltags = set(",".join(r.tag for r in rows).split(','))
        tagsums = dict((t, {}) for t in alltags)
        previousAdded = {}
        for row in rows:
            for tag in alltags:
                tagsumlist = tagsums[tag]
                rowdate = str(row.dateAdded)
                tagsumlist[rowdate] = tagsumlist.get(previousAdded.get(tag, None), 0)
                previousAdded[tag] = str(row.dateAdded)
                if tag in row.tags:
                    tagsumlist[rowdate] += row.amount
        return Response(tagsums)
