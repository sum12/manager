from rest_framework import serializers
from rest_framework.reverse import  reverse

from django.contrib.auth import get_user_model

Person = get_user_model()


class PersonSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source="get_full_name", read_only=True)
    links = serializers.SerializerMethodField()

    def get_links(self, obj):
        request =  self.context['request']
        return {
                'self': reverse("person-detail", request=request, kwargs={Person.USERNAME_FIELD:obj.get_username()}),
                }

    class Meta:
        model = Person
        fields = (Person.USERNAME_FIELD, 'full_name', 'is_active', 'links')
