from django.db import models
from django.conf import settings
from django.utils import timezone

User = settings.AUTH_USER_MODEL


class Friend(models.Model):
    f1 = models.ForeignKey(User, related_name='friends_with', null=False)
    f2 = models.ForeignKey(User, related_name='friends_of', null=False)
    since = models.DateField(null=False, default=timezone.now)

    @property
    def name2(self):
        return self.f2
    
    @property
    def name1(self):
        return self.f1

    class Meta:
        unique_together = (('f1','f2'),)
