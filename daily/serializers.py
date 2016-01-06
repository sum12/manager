
from rest_framework import serializers
from .models import activity


class ActivitySerializer(serializers.ModelSerializer):

    class Meta:
        model = activity
        fields = ('id', 'type', 'on')
