from django.contrib import admin

from .models import Category, Comment, Location, Post


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'text',
        'pub_date',
        'author',
        'location',
        'category',
        'is_published',
        'created_at'
    )
    list_editable = (
        'text',
        'location',
        'category',
        'is_published'
    )
    search_fields = ('title', 'location', 'category',)
    list_filter = ('location', 'category',)
    list_display_links = ('title',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'description',
        'is_published',
        'created_at'
    )
    list_editable = (
        'description',
        'is_published',
    )
    search_fields = ('title',)
    list_display_links = ('title',)


class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'is_published',
        'created_at'
    )
    list_editable = ('is_published',)
    search_fields = ('name',)
    list_display_links = ('name',)


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'text',
        'post',
        'author',
        'is_published',
        'created_at'
    )
    list_editable = ('is_published',)
    search_fields = ('text',)
    list_filter = ('post', 'author',)
    list_display_links = ('text',)


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.empty_value_display = 'Не задано'
