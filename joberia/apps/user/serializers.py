from rest_framework import serializers

from joberia.apps.user.models import User


class AuthUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'role', 'first_name', 'last_name', 'platform', 'password')
