from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from joberia.apps.job.models import Job, Comment, Bonus, OfferedItem, Tag, DesiredProfileItem
from joberia.apps.user.serializers import UserSerializer


class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    comment_replies = RecursiveField(many=True)

    class Meta:
        model = Comment
        fields = (
            'id',
            'author',
            'text',
            'comment_replies'
        )


class BonusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bonus
        fields = ('name', 'value')


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferedItem
        fields = ('label',)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('type', 'name')


class DesiredProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DesiredProfileItem
        fields = ('name',)


class JobSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True)
    bonuses = BonusSerializer(many=True)
    offers = serializers.ListSerializer(child=serializers.CharField())
    location_tags = SerializerMethodField()
    skill_tags = SerializerMethodField()
    created_by = UserSerializer()
    desired_profile = serializers.ListSerializer(child=serializers.CharField())

    class Meta:
        model = Job
        fields = (
            'id',
            'title',
            'description',
            'short_description',
            'status',
            'desired_profile',
            'offers',
            'bonuses',
            'offers',
            'expires_at',
            'created_by',
            'comments',
            'location_tags',
            'skill_tags',
            'created_by'
        )

    def get_tag(self, type, obj):
        tags = obj.tags.filter(type=type).all()
        data = serializers.ListSerializer(instance=tags, child=serializers.CharField())
        return data.data

    def get_location_tags(self, job):
        return self.get_tag('loc', job)

    def get_skill_tags(self, job):
        return self.get_tag('skill', job)
