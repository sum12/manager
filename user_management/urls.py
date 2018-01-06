from django.contrib import admin

from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter(trailing_slash=False)
router.register(r'person', views.PersonViewSet)
router.register(r'friend', views.FriendViewSet)
