from django.contrib import admin

from .models import Article, UserFavouriteArticle


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "created", "synopsis")
    list_filter = ("created", "author")
    search_fields = ("title", "synopsis", "content")
    readonly_fields = ("created",)
    ordering = ("-created",)


@admin.register(UserFavouriteArticle)
class UserFavouriteArticleAdmin(admin.ModelAdmin):
    list_display = ("user", "article")
    list_filter = ("user", "article__author")
    search_fields = ("user__username", "article__title")
