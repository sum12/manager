from django.db import models
from datetime import datetime
# Create your models here.

from user_management.models import User

class Expenses(models.Model):
    dateAdded = models.DateField(auto_now_add=True, default=datetime(1,1,1))
    amount = models.IntegerField(default=0)
    sharedWith = models.ForeignKey('user_management.User', default=None, related_name='+', null=True)
    spender = models.ForeignKey('user_management.User', null=False)
    tag = models.CharField(max_length=10, default=None)


    def __unicode__(self):
        return '<td> >{dateAdded} </td>'\
            '<td> <a href="#"  data-type="text" class="{objId}-expense" > {amount} </a> </td>'\
            '<td> {spender} </td>'\
            '<td> <a href="#" data-type="text" class="{objId}-expense" > {tag} </a> </td>'.format(**{
                                        'dateAdded': self.dateAdded.strftime("%d-%b-%y %H:%M"),
                                        'amount': self.amount,
                                        'spender': self.spender.username,
                                        'tag':self.tag,
                                        'objId': self.id})
                
