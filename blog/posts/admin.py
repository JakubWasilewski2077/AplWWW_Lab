from django.contrib import admin
from .models import Category, Topic, Post

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']

class TopicAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    search_fields = ['name']

class PostAdmin(admin.ModelAdmin):
    readonly_fields = ["created_at"]
    list_display = ['title', 'tekstskr', 'topic_category', 'created_by', 'created_at', 'updated_at']
    list_filter = ['topic', 'topic__category', 'created_by']
    prepopulated_fields = {"slug": ["title"]}

    def tekstskr(self, obj):
        text_skr = obj.text.split()
        if len(text_skr) <= 5:
            return obj.text
        return " ".join(text_skr[:5]) + "..."

    @admin.display(description="Topic (Category)")
    def topic_category(self, obj):
        return f"{obj.topic.name} ({obj.topic.category.name})"



admin.site.register(Category, CategoryAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Post, PostAdmin)
