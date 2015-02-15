from django.db import models
from datetime import datetime
from django.core.urlresolvers import reverse

from user_management.models import User

import json
class Expenses(models.Model):
    dateAdded = models.DateField(auto_now_add=True, default=datetime(1,1,1))
    amount = models.PositiveIntegerField(default=0)
    #saharedExpense = models.ForeignKey('expense.sharedExpense', default=None, related_name='+', blank=True, null=True)
    spender = models.ForeignKey('user_management.User', null=False)
    tag = models.CharField(max_length=100, default=None)


    def __unicode__(self):
        return self.dump()

#TODO: this is a bad, mixing UI and functionality
#      may be return a json or something, so api can be easy
#      ' data-source="/user/{spender_id}/friends"'\
    def dump(self,useTheseValues={}):
        formatDict = {'dateAdded': self.dateAdded.strftime("%d-%b-%y %H:%M"), 
                      'amount': self.amount, 
                      'spender': self.spender.username,
                      'spender_id':self.spender.id,
                      'tag':self.tag, 
                      'objId': self.id,
                      'refBy':json.dumps([i.wit.id for i in self.sharedexpense_set.all() if i.returned]),
                      'wit':json.dumps([i.wit.id for i in self.sharedexpense_set.all()]),
                      'url': reverse('expense.save')}
        formatDict.update(useTheseValues)    
        return '<td> {dateAdded} </td>'\
                '<td> <a href="#" '\
                        ' data-url={url}'\
                        ' data-pk={objId}'\
                        ' data-name="amount"'\
                        ' data-type="text"'\
                        ' class="{objId}-expense expense">' \
                        ' {amount}'\
                      ' </a>'\
                 '</td>'\
                 '<td> <a href="#" '\
                           ' data-url={url}'\
                           ' data-pk={objId}'\
                           ' data-type="select2"'\
                           ' data-name="tag"'\
                           ' class="mytag">'\
                           ' {tag}'\
                           '</a> '\
                  '</td>'\
                  '<td> <a href="#" class="friendadder"'\
                        ' data-type="select2"'\
                           ' data-url={url}'\
                           ' data-pk={objId}'\
                        ' data-value="{wit}"'\
                        ' data-name="sharedWith"'\
                        ' data-title="Divide Among Friends">'\
                        ''\
                        '</a>'\
                  '</td>'\
                  '<td> <a href="#" class="friendadder"'\
                        ' data-type="select2"'\
                        ' data-url={url}'\
                           ' data-pk={objId}'\
                        ' data-value="{refBy}"'\
                        ' data-name="returned"'\
                        ' data-title="People Who Have Paid">'\
                        ''\
                        '</a>'\
                  '</td>'.format(**formatDict)

class sharedExpense(models.Model):
    wit = models.ForeignKey(User, null=False)
    exp = models.ForeignKey(Expenses,null=False)
    returned = models.BooleanField(default=False,null=False)
