# admin.py
from django.contrib import admin
from .models import Book, Record

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'genre', 'condition', 'price', 'status', 'created_at']
    list_filter = ['genre', 'condition', 'status', 'created_at']
    search_fields = ['title', 'author', 'isbn']
    readonly_fields = ['created_at', 'updated_at']

    def save_model(self, request, obj, form, change):
        if not change:  # Creating new object
            obj.added_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = ['title', 'artist', 'genre', 'condition', 'price', 'status', 'created_at']
    list_filter = ['genre', 'condition', 'status', 'created_at']
    search_fields = ['title', 'artist', 'cat_number']
    readonly_fields = ['created_at', 'updated_at']

    def save_model(self, request, obj, form, change):
        if not change:  # Creating new object
            obj.added_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)
