import graphene
from graphene_django import DjangoObjectType
from posts.models import Category, Topic, Post
from django.contrib.auth.models import User



class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ("id", "name")


class TopicType(DjangoObjectType):
    class Meta:
        model = Topic
        fields = ("id", "name", "category")

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "username", "email")

class PostType(DjangoObjectType):
    class Meta:
        model = Post
        fields = ("id", "title", "text", "slug", "topic", "created_by", "created_at")



class Query(graphene.ObjectType):
    all_posts = graphene.List(PostType)
    post_by_id = graphene.Field(PostType, id=graphene.Int(required=True))

    all_categories = graphene.List(CategoryType)
    category_by_id = graphene.Field(CategoryType, id=graphene.Int(required=True))

    all_topics = graphene.List(TopicType)
    topic_by_id = graphene.Field(TopicType, id=graphene.Int(required=True))
    topics_by_category = graphene.List(TopicType, category_id=graphene.Int(required=True))

    def resolve_all_posts(root, info):
        return Post.objects.select_related("topic", "created_by").all()

    def resolve_post_by_id(root, info, id):
        try:
            return Post.objects.get(pk=id)
        except Post.DoesNotExist:
            raise Exception("Nie ma posta o tym id")

    def resolve_all_categories(root, info):
        return Category.objects.all()

    def resolve_category_by_id(root, info, id):
        try:
            return Category.objects.get(pk=id)
        except Category.DoesNotExist:
            raise Exception("Nie ma kategorii o tym id")

    def resolve_all_topics(root, info):
        return Topic.objects.select_related("category").all()

    def resolve_topic_by_id(root, info, id):
        try:
            return Topic.objects.get(pk=id)
        except Topic.DoesNotExist:
            raise Exception("Nie ma tematu o tym id")

    def resolve_topics_by_category(root, info, category_id):
        return Topic.objects.filter(category_id=category_id)



class CreatePost(graphene.Mutation):
    post = graphene.Field(PostType)
    success = graphene.Boolean()
    message = graphene.String()

    class Arguments:
        title = graphene.String(required=True)
        text = graphene.String(required=True)
        topic_id = graphene.Int(required=True)
        slug = graphene.String(required=True)
        created_by_id = graphene.Int(required=True)

    def mutate(self, info, title, text, topic_id, slug, created_by_id):
        try:
            post = Post.objects.create(
                title=title,
                text=text,
                topic_id=topic_id,
                slug=slug,
                created_by_id=created_by_id,
            )
            return CreatePost(post=post, success=True, message="Post created successfully")
        except Exception as e:
            return CreatePost(post=None, success=False, message=str(e))


class UpdatePost(graphene.Mutation):
    post = graphene.Field(PostType)
    success = graphene.Boolean()
    message = graphene.String()

    class Arguments:
        id = graphene.Int(required=True)
        title = graphene.String()
        text = graphene.String()
        topic_id = graphene.Int()
        slug = graphene.String()

    def mutate(self, info, id, title=None, text=None, topic_id=None, slug=None):
        try:
            post = Post.objects.get(pk=id)
            if title is not None:
                post.title = title
            if text is not None:
                post.text = text
            if topic_id is not None:
                post.topic_id = topic_id
            if slug is not None:
                post.slug = slug
            post.save()
            return UpdatePost(post=post, success=True, message="Post updated successfully")
        except Post.DoesNotExist:
            return UpdatePost(post=None, success=False, message="Post not found")
        except Exception as e:
            return UpdatePost(post=None, success=False, message=str(e))


class DeletePost(graphene.Mutation):
    success = graphene.Boolean()
    message = graphene.String()

    class Arguments:
        id = graphene.Int(required=True)

    def mutate(self, info, id):
        try:
            post = Post.objects.get(pk=id)
            post.delete()
            return DeletePost(success=True, message="Post deleted successfully")
        except Post.DoesNotExist:
            return DeletePost(success=False, message="Post not found")
        except Exception as e:
            return DeletePost(success=False, message=str(e))


class Mutation(graphene.ObjectType):
    create_post = CreatePost.Field()
    update_post = UpdatePost.Field()
    delete_post = DeletePost.Field()



schema = graphene.Schema(query=Query, mutation=Mutation)