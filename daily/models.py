from django.conf import settings
from django.db import models
from django.utils import timezone

User = settings.AUTH_USER_MODEL

class typeorder(models.Model):
    type = models.CharField(max_length=255, null=False)
    order = models.PositiveIntegerField(null=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, on_delete=models.PROTECT)


class activity(models.Model):
    on = models.DateTimeField(default=timezone.localtime)
    type_order = models.ForeignKey(typeorder, on_delete=models.PROTECT)
    data = models.TextField(default='')

    class Meta:
        ordering = ('-on', )
