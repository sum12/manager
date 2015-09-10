
from rest_framework import serializers
from .models import Expenses, sharedExpense


class ExpenseSerializer(serializers.ModelSerializer):
    shared =  serializers.SerializerMethodField()

    def get_shared(self,obj):
        return True  if obj.sharedexpense_set is () else False

    def get_amount_info(self,metadata):
        return {'cellEnableEditing':False,'name':'Amount'}

    def get_spender_info(self,metadata):
        return {'enableSorting':False}

    class Meta:
        model = Expenses
        fields = ("id", "amount", 'spender','tag', 'dateAdded', 'shared', 'pinned')


class ShareExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = sharedExpense
        fields = ('id', 'wid', 'exp')
