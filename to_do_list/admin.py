from django.contrib import admin
from django.contrib.auth.models import User

from to_do_list.models import ToDoList


@admin.register(ToDoList)
class TodoAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'is_complete', 'start_date', 'end_date')
    list_filter = ('is_complete',)
    search_fields = ('title',)
    ordering = ('start_date',)
    fieldsets = (
        ('Todo Info', {
            'fields': ('title', 'description', 'is_complete')
        }),
        ('Date Range', {
            'fields': ('start_date', 'end_date')
        }),
    )
