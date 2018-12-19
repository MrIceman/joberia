from rest_framework import serializers

from .models import Platform


class PlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platform
        fields = ('id', 'theme', 'platform_name', 'home_text_header', 'home_text_body', 'footer_about_text')
