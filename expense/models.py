from django.db import models
from datetime import datetime
from django.conf import settings
from django.conf import settings
import json

User = settings.AUTH_USER_MODEL

class Expenses(models.Model):
    dateAdded = models.DateField(auto_now_add=True)
    amount = models.PositiveIntegerField(default=0)
    #saharedExpense = models.ForeignKey('expense.sharedExpense', default=None, related_name='+', blank=True, null=True)
    spender = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, on_delete=models.PROTECT)
    tag = models.CharField(max_length=100, default=None)
    pinned = models.BooleanField(default=False)

    def _split_tags(self):
        return self.tag.split(',')

    tags = property(_split_tags)

    class Meta:
        ordering = ( 'dateAdded', )



class sharedExpense(models.Model):
    wit = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, on_delete=models.PROTECT)
    exp = models.ForeignKey(Expenses,null=False, on_delete=models.PROTECT)
    returned = models.BooleanField(default=False,null=False)
