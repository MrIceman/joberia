from rest_framework import serializers

from joberia.apps.user.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'role', 'organization', 'first_name', 'last_name')
