from django.db import models
from datetime import datetime
from django.core.urlresolvers import reverse
# Create your models here.

from user_management.models import User

class Expenses(models.Model):
    dateAdded = models.DateField(auto_now_add=True, default=datetime(1,1,1))
    amount = models.IntegerField(default=0)
    sharedWith = models.ForeignKey('user_management.User', default=None, related_name='+', blank=True, null=True)
    spender = models.ForeignKey('user_management.User', null=False)
    tag = models.CharField(max_length=100, default=None)


    def __unicode__(self):
        return '<td> {dateAdded} </td>'\
                '<td> <a href="#" '\
                        ' data-url={url}'\
                        ' data-param={csrf}'\
                        ' data-pk={objId}'\
                        ' data-name="amount"'\
                        ' old-value="{amount}"'\
                        ' data-type="text"'\
                        ' class="{objId}-expense">' \
                        ' {amount}'\
                      ' </a>'\
                 '</td>'\
                 '<td> {spender} </td>'\
                 '<td> <a href="#" '\
                           ' data-url={url}'\
                           ' data-pk={objId}'\
                           ' data-param={csrf}'\
                           ' data-type="text"'\
                           ' data-name="tag"'\
                           ' class="{objId}-expense"'\
                           ' old-value="{tag}"> '\
                           ' {tag} '\
                           '</a> '\
                  '</td>'.format(**{
                      'dateAdded': self.dateAdded.strftime("%d-%b-%y %H:%M"), 
                      'amount': self.amount, 
                      'spender': self.spender.username, 
                      'tag':self.tag, 
                      'objId': self.id, 
                      'url': reverse('expense.save'),
                      'csrf': '"{srfmiddlewaretoken: {%csrf_token%}" '})

