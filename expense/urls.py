from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from rest_framework.routers import SimpleRouter
from .views import ExpenseViewSet


router = SimpleRouter(trailing_slash=False)
router.register(r'expense', ExpenseViewSet, base_name='expense')
#router.register(r'sharedexpense', ExpenseViewSet)

urlparams = dict(year='(?P<year>[0-9]{4})',
                 month='(?P<month>[0-9]{1,2})',
                 day='(?P<day>[0-9]{1,2})',
                 base='expenses'
                 )


apiView = ExpenseViewSet.as_view({'get': 'list'})
loggedinView = login_required(apiView)
expenseView = loggedinView
urls = [url(r'^{base}/{year}/{month}/{day}$'.format(**urlparams), expenseView),
        url(r'^{base}/{year}/{month}$'.format(**urlparams), expenseView),
        url(r'^{base}/{year}$'.format(**urlparams), expenseView)
        ]

urls += router.urls
urlpatterns = urls
