# wagtail_hooks.py

from wagtail_modeladmin.options import (
    ModelAdmin,
    ModelAdminGroup,
    modeladmin_register
)

from .models import Book, Record, NewsArticle


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

class NewsArticleAdmin(ModelAdmin):
    model = NewsArticle
    menu_label = "News Articles"
    menu_icon = "doc-full"
    menu_order = 301
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ['title', 'author', 'publish_date', 'status', 'featured', 'created_at']
    list_filter = ['status', 'featured', 'publish_date', 'created_at']
    search_fields = ['title', 'author', 'content', 'excerpt']
    exclude = ['slug']

modeladmin_register(NewsArticleAdmin)