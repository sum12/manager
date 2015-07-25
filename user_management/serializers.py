from rest_framework import serializers
from rest_framework.reverse import  reverse

from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source="get_full_name", read_only=True)
    links = serializers.SerializerMethodField()

    def get_links(self, obj):
        request =  self.context['request']
        return {
                'self': reverse("user-detail", request=request, kwargs={User.USERNAME_FIELD:obj.get_username()}),
                }

    class Meta:
        model = User
        fields = ('id', User.USERNAME_FIELD, 'full_name', 'is_active', 'links')
