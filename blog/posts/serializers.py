from django.template.defaultfilters import title
from rest_framework import serializers
from .models import Category, Topic, Post
from django.utils import timezone

class CategorySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=60)
    description = serializers.CharField(default="No description")

    def create(self, validated_data):
        return Category.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['name', 'category', 'created']

class PostSerializer(serializers.ModelSerializer):
    def validate_title(self, value):
        if not value.isalpha():
            raise serializers.ValidationError("Title can't contain anything but letters")
        return value

    def validate_created_at(self, value):
        tim = timezone.now()
        if value > tim:
            raise serializers.ValidationError("Creation date can't be from the future")
        return value


    class Meta:
        model = Post
        fields = ['title', 'text', 'topic', 'slug', 'created_at', 'updated_at', 'created_by']



