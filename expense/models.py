from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
# Create your models here.

class Expenses(models.Model):
    dateAdded = models.DateField(auto_now_add=True, default=datetime(1,1,1))
    amount = models.IntegerField(default=0)
    sharedWith = models.ForeignKey(User, default=None, related_name='+')
    spender = models.ForeignKey(User, null=False)
    tag = models.CharField(max_length=10, default=None)

