from django.contrib import admin

from .models import Card, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ("word", "translation", "category", "created_at")
    list_filter = ("category", "created_at")
    search_fields = ("word", "translation", "example")
    autocomplete_fields = ("category",)
