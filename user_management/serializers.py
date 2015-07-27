from rest_framework import serializers
from rest_framework.reverse import  reverse
from django.contrib.auth import get_user_model

from .models import Friend

Person = get_user_model()


class PersonSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source="get_full_name", read_only=True)
    links = serializers.SerializerMethodField()

    def get_links(self, obj):
        request =  self.context['request']
        return {
                'self': reverse("user-detail", request=request, kwargs={Person.USERNAME_FIELD:obj.get_username()}),
                'friends_with' :  "{url}?search={key}".format(url=reverse('friend-list',request=request),key=obj.id)
                }

    class Meta:
        model = Person
        fields = ('id', Person.USERNAME_FIELD, 'full_name', 'is_active', 'links' )


class FriendSerializer(serializers.ModelSerializer):
    name1 = serializers.CharField(read_only=True)
    name2 = serializers.CharField(read_only=True)
    f1 = serializers.PrimaryKeyRelatedField(queryset=Person.objects.all())
    f2 = serializers.PrimaryKeyRelatedField(queryset=Person.objects.all())
    class Meta:
        model = Friend
        fields = ('id', "f1", "f2", 'name1', 'name2')
