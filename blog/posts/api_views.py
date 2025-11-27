from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Category, Topic, Post
from .serializers import CategorySerializer, TopicSerializer, PostSerializer
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse

# category --------------------------------------------------------------------------------------------

@api_view(['GET'])
def category_list(request):
    if request.method == 'GET':
        categorys = Category.objects.all()
        serializer = CategorySerializer(categorys, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def category_search(request, value):
    if request.method == 'GET':
        categorys = Category.objects.filter(name__contains=value)
        serializer = CategorySerializer(categorys, many=True)
        return Response(serializer.data)

@api_view(['POST'])
def category_create(request):
    if request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def category_detail(request, pk):

    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CategorySerializer(category)
        return Response(serializer.data)

@api_view(['PUT', 'DELETE'])
@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def category_update_delete(request, pk):
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def categories_topics(request, pk):
    topics = Topic.objects.filter(category__id = pk)
    serializer = TopicSerializer(topics, many=True)
    return Response(serializer.data)



@permission_required('posts.view_category')
def category_view_details(request, pk):
    try:
        category = Category.objects.get(pk=pk)
        return HttpResponse(f"Kategoria: {category.name}<br>Opis: {category.description}")
    except Category.DoesNotExist:
        return HttpResponse(f"Kategoria nie istnieje.")

# topic --------------------------------------------------------------------------------------------

@api_view(['GET'])
def topic_list(request):
    if request.method == 'GET':
        topics = Topic.objects.all()
        serializer = TopicSerializer(topics, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def topic_search(request, value):
    if request.method == 'GET':
        topics = Topic.objects.filter(name__contains=value)
        serializer = TopicSerializer(topics, many=True)
        return Response(serializer.data)

@api_view(['POST'])
def topic_create(request):
    if request.method == 'POST':
        serializer = TopicSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def topic_detail(request, pk):
    try:
        topic = Topic.objects.get(pk=pk)
    except Topic.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TopicSerializer(topic)
        return Response(serializer.data)

@api_view(['PUT', 'DELETE'])
@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def topic_update_delete(request, pk):
    try:
        topic = Topic.objects.get(pk=pk)
    except Topic.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = TopicSerializer(topic, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        topic.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# post --------------------------------------------------------------------------------------------

@api_view(['GET'])
def post_list(request):
    if request.method == 'GET':
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

@api_view(['POST'])
def post_create(request):
    if request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def post_detail(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response(serializer.data)

@api_view(['PUT'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def post_update(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.user != post.created_by and not request.user.has_perm("posts.can_edit_others_posts"):
        return Response({"error": "Ty możesz edytować tylko swoje posty"},
                        status=status.HTTP_403_FORBIDDEN)

    if request.method == 'PUT':
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def post_delete(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def user_posts(request):
    if request.method == 'GET':
        posts = Post.objects.filter(created_by=request.user)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)