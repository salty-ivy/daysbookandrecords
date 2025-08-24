# wagtail_hooks.py

from wagtail_modeladmin.options import (
    ModelAdmin,
    ModelAdminGroup,
    modeladmin_register
)

from .models import Book, Record, NewsPage


class BookAdmin(ModelAdmin):
    model = Book
    menu_label = "Books"
    menu_icon = "pick"
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ['title', 'author', 'genre', 'price', 'status', 'created_at', 'featured']
    list_filter = ['genre', 'condition', 'status', 'created_at']
    search_fields = ['title', 'author', 'isbn']
    readonly_fields = ['created_at', 'updated_at']

class RecordAdmin(ModelAdmin):
    model = Record
    menu_label = "Records"
    menu_icon = "pick"
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ['title', 'artist', 'genre', 'condition', 'format', 'price', 'status', 'created_at', 'featured']
    list_filter = ['genre', 'condition', 'format', 'status', 'created_at']
    search_fields = ['title', 'artist', 'cat_number']
    readonly_fields = ['created_at', 'updated_at']


modeladmin_register(BookAdmin)
modeladmin_register(RecordAdmin)

class NewsPageAdmin(ModelAdmin):
    model = NewsPage
    menu_label = "News Pages"
    menu_icon = "doc-full"
    menu_order = 300
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ['title', 'slug', 'first_published_at']
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title',)}

modeladmin_register(NewsPageAdmin)