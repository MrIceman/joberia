from rest_framework import serializers

from joberia.apps.job.models import Job, Comment, Bonus, Tag
from joberia.apps.user.serializers import UserSerializer


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer()

    class Meta:
        model = Comment
        fields = (
            'author',
            'text',
        )


class BonusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bonus
        fields = ('entries')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('')


class JobSerializers(serializers.ModelSerializer):
    comments = CommentSerializer(many=True)
    bonuses = BonusSerializer(many=True)
    tags = serializers.ListField(child=serializers.CharField())

    class Meta:
        model = Job
        fields = (
            'id',

            'title',
            'description',
            'short_description',
            'status',
            'tags',
            'desired_profile',
            'offered_items',
            'bonuses',
            'expires_at',
            'created_by',
            'picture',
            'comments'
        )
