
from rest_framework import serializers
from .models import Expenses, sharedExpense


class ExpenseSerializer(serializers.ModelSerializer):
    shared =  serializers.SerializerMethodField()

    def get_shared(self,obj):
        return True  if obj.sharedexpense_set is () else False

    class Meta:
        model = Expenses
        fields = ("id", "amount", 'spender','tag', 'dateAdded', 'shared', 'pinned')


class ShareExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = sharedExpense
        fields = ('id', 'wid', 'exp')
