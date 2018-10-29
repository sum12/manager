
from rest_framework import serializers

import datetime as dt
from .models import activity, typeorder


class TypeOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = typeorder
        fields = ('id', 'type', 'order')


class ActivitySerializer(serializers.ModelSerializer):

    daysbefore = serializers.SerializerMethodField()
    donetoday = serializers.SerializerMethodField()

    def get_daysbefore(self, obj):
        today = dt.datetime.today().date()
        return (today - obj.on.date()).days

    def get_donetoday(self, obj):
        today = dt.datetime.today().date()
        return (today - obj.on.date()).days == 0

    class Meta:
        model = activity
        fields = ('id', 'type_order_id', 'on', 'data', 'daysbefore', 'donetoday')
