from django.template.defaultfilters import title
from rest_framework import serializers
from .models import Category, Topic, Post

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
    class Meta:
        model = Post
        fields = ['title', 'text', 'topic', 'slug', 'created_at', 'updated_at', 'created_by']
