from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Tip


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = [
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "date_joined",
    ]
    list_filter = ["is_staff", "is_superuser", "is_active", "date_joined"]
    search_fields = ["username", "email", "first_name", "last_name"]
    ordering = ["-date_joined"]


@admin.register(Tip)
class TipAdmin(admin.ModelAdmin):
    list_display = [
        "content_preview",
        "author",
        "date",
        "upvote_count",
        "downvote_count",
        "net_votes",
    ]
    list_filter = ["date", "author"]
    search_fields = ["content", "author__username"]
    ordering = ["-date"]
    readonly_fields = ["date"]

    def content_preview(self, obj):
        return obj.content[:100] + "..." if len(obj.content) > 100 else obj.content

    content_preview.short_description = "Content Preview"  # type: ignore

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs

        return qs.filter(author=request.user)

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj and obj.author == request.user:
            return True
        return request.user.has_perm("lpt_app.delete_tip")

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj and obj.author == request.user:
            return True
        return super().has_change_permission(request, obj)
