from django.contrib import admin
from .models import Author,Category,Book ,Favorite

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display=["name","country","birth_year"]
    search_fields=["name","country"]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields=["name"]

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_filter=["category","is_active","publication_year"]
    search_fields=["title","author__name","category__name"]

admin.site.register(Favorite)
