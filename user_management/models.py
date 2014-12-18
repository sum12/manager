from django.db import models

from django.contrib.auth.models import User as Duser

# Create your models here.

class User(Duser):
    friends = models.ForeignKey('self', default=None, null=True)
    many_friends = models.ManyToManyField('self',default=None,blank=True)
    def __unicode__(self):
        return u'%s'%self.email
