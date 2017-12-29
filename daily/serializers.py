
from rest_framework import serializers

import datetime as dt
from .models import activity,typeorder


class TypeOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = typeorder
        fields = ('id', 'type','order')

class ActivitySerializer(serializers.ModelSerializer):

    daysbefore = serializers.SerializerMethodField()
    donetoday = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    order = serializers.SerializerMethodField()
    type_order = TypeOrderSerializer(many=False)

    def get_daysbefore(self, obj):
        today = dt.datetime.today().date()
        return (today - obj.on.date()).days

    def get_donetoday(self, obj):
        today = dt.datetime.today().date()
        return (today - obj.on.date()).days == 0

    def get_type(self, obj):
        return obj.type_order.type

    def get_order(self, obj):
        return obj.type_order.order

    class Meta:
        model = activity
#        fields = ('id', 'type_order_id', 'type', 'order', 'on', 'data', 'daysbefore', 'donetoday')
#        fields = ('id', 'type_order', 'on', 'data', 'daysbefore', 'donetoday')
        fields = ('id', 'type', 'order', 'type_order', 'on', 'data', 'daysbefore', 'donetoday')
