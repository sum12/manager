from django.db import models
from datetime import datetime
from django.core.urlresolvers import reverse

from user_management.models import User

class Expenses(models.Model):
    dateAdded = models.DateField(auto_now_add=True, default=datetime(1,1,1))
    amount = models.IntegerField(default=0)
    sharedWith = models.ForeignKey('user_management.User', default=None, related_name='+', blank=True, null=True)
    spender = models.ForeignKey('user_management.User', null=False)
    tag = models.CharField(max_length=100, default=None)

#TODO: this si bad, mixing UI and functionality
#      may be return a json or something, so api can be easy
                        #' data-source="/user/{spender_id}/friends"'\
    def __unicode__(self):
        return '<td> {dateAdded} </td>'\
                '<td> <a href="#" '\
                        ' data-url={url}'\
                        ' data-param={csrf}'\
                        ' data-pk={objId}'\
                        ' data-name="amount"'\
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
                           ' {tag} '\
                           '</a> '\
                  '</td>'\
                  '<td> <a href="#" id="myselect2"'\
                        ' data-type="select2"'\
                        ' data-title="myselection"'\
                        ' data-value="ru">'\
                        ' this si just some text'\
                        '</a>'\
                  '</td>'.format(**{
                      'dateAdded': self.dateAdded.strftime("%d-%b-%y %H:%M"), 
                      'amount': self.amount, 
                      'spender': self.spender.username,
                      'spender_id':self.spender.id,
                      'tag':self.tag, 
                      'objId': self.id, 
                      'data-source':'[{id: 1, text: "text1"}, {id: 2, text: "text2"}]',
                      'url': reverse('expense.save'),
                      'csrf': '"{csrfmiddlewaretoken: {%csrf_token%}" '})

