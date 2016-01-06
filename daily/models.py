from django.db import models
from datetime import datetime


class activity(models.Model):
    on = models.DateField(auto_now_add=True)
    type = models.CharField(max_length=255, null=False)
    data = models.TextField(default='')
