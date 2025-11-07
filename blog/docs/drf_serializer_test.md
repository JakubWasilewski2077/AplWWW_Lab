Category:

>>> from posts.models import Category, Topic
>>> from posts.serializers import CategorySerializer, TopicSerializer
>>> from rest_framework.renderers import JSONRenderer
>>> from rest_framework.parsers import JSONParser
>>> import io
>>> category = Category(name='KatSer', description='Kategoria_serializertest')
>>> category.save()
>>> serializer_category = CategorySerializer(category)
>>> serializer_category.data
{'name': 'KatSer', 'description': 'Kategoria_serializertest'}
>>> content = JSONRenderer().render(serializer_category.data)
>>> content
b'{"name":"KatSer","description":"Kategoria_serializertest"}'
>>> stream = io.BytesIO(content)
>>> data = JSONParser().parse(stream)
>>> data
{'name': 'KatSer', 'description': 'Kategoria_serializertest'}
>>> deserializer = CategorySerializer(data=data)
>>> deserializer.is_valid()
True
>>> deserializer.validated_data
{'name': 'KatSer', 'description': 'Kategoria_serializertest'}
>>> deserializer.save()
<Category: KatSer>
>>> deserializer.data
{'name': 'KatSer', 'description': 'Kategoria_serializertest'}


Topic:

>>> from posts.models import Category, Topic
>>> from posts.serializers import CategorySerializer, TopicSerializer
>>> from rest_framework.renderers import JSONRenderer
>>> from rest_framework.parsers import JSONParser
>>> category = Category.objects.get(name='Kategoria_A')
>>> topic = Topic(name='Topic_serializ', category=category)
>>> topic.category
<Category: Kategoria_A>
>>> topic.save()
>>> serializer_topic = TopicSerializer(topic)
>>> serializer_topic.data
{'name': 'Topic_serializ', 'category': 3, 'created': '2025-11-07T04:36:21.832431Z'}
>>> content = JSONRenderer().render(serializer_topic.data)
>>> content
b'{"name":"Topic_serializ","category":3,"created":"2025-11-07T04:36:21.832431Z"}'
>>> import io
>>> stream = io.BytesIO(content)
>>> data = JSONParser().parse(stream)
>>> data
{'name': 'Topic_serializ', 'category': 3, 'created': '2025-11-07T04:36:21.832431Z'}
>>> deserializer = CategorySerializer(data=data)
>>> deserializer.is_valid()
True
>>> deserializer.validated_data
{'name': 'Topic_serializ', 'description': 'No description'}
>>> deserializer.save()
<Category: Topic_serializ>
>>> deserializer.data
{'name': 'Topic_serializ', 'description': 'No description'}