from django.db import models
from django.utils import timezone


class activity(models.Model):
    on = models.DateField(default=timezone.now)
    type = models.CharField(max_length=255, null=False)
    data = models.TextField(default='')
