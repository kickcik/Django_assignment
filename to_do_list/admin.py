from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from to_do_list.models import ToDoList, Comment


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    fields = ('content', 'author')

@admin.register(ToDoList)
class TodoAdmin(SummernoteModelAdmin):
    list_display = ('title', 'description', 'is_complete', 'start_date', 'end_date')
    list_filter = ('is_complete',)
    search_fields = ('title',)
    ordering = ('-created_at',)
    fieldsets = (
        ('Todo Info', {
            'fields': ('title', 'description', 'is_complete', 'author')
        }),
        ('Date Range', {
            'fields': ('start_date', 'end_date')
        }),
    )
    inlines = [CommentInline]

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'todo', 'author', 'content', 'created_at')
    list_filter = ('todo', 'author')
    search_fields = ('content', 'author__username')
    ordering = ('-created_at',)
    list_display_links = ('content',)
    fieldsets = (
        ('Comment Info', {
            'fields': ('todo', 'author', 'content')
        }),
    )