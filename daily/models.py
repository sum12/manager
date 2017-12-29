from django.db import models
from django.utils import timezone


class typeorder(models.Model):
    type = models.CharField(max_length=255, null=False)
    order = models.PositiveIntegerField(null=False)


class activity(models.Model):
    on = models.DateTimeField(default=timezone.now)
    type_order = models.ForeignKey(typeorder)
    data = models.TextField(default='')

    class Meta:
        ordering = ('-on', )
