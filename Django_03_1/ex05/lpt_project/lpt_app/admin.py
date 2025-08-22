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
        "has_downvote_permission",
        "date_joined",
    ]
    list_filter = ["is_staff", "is_superuser", "is_active", "date_joined"]
    search_fields = ["username", "email", "first_name", "last_name"]
    ordering = ["-date_joined"]
    actions = ["grant_downvote_permission", "revoke_downvote_permission"]

    def has_downvote_permission(self, obj):
        if obj.is_superuser:
            return "👑 Admin (All permissions)"
        elif obj.has_perm("lpt_app.can_downvote_tips"):
            return "🔑 Moderator (Can downvote)"
        else:
            return "👤 User (Own tips only)"

    has_downvote_permission.short_description = "Downvote Permission"  # type: ignore

    def grant_downvote_permission(self, request, queryset):
        from django.contrib.auth.models import Permission
        from django.contrib.contenttypes.models import ContentType

        content_type = ContentType.objects.get_for_model(Tip)
        permission = Permission.objects.get(
            codename="can_downvote_tips",
            content_type=content_type,
        )

        count = 0
        for user in queryset:
            if not user.user_permissions.filter(pk=permission.pk).exists():
                user.user_permissions.add(permission)
                count += 1

        self.message_user(
            request, f"Permission de downvote accordée à {count} utilisateur(s)."
        )

    grant_downvote_permission.short_description = "🔑 Accorder permission de downvote"  # type: ignore

    def revoke_downvote_permission(self, request, queryset):
        """Retire la permission de downvote aux utilisateurs sélectionnés"""
        from django.contrib.auth.models import Permission
        from django.contrib.contenttypes.models import ContentType

        content_type = ContentType.objects.get_for_model(Tip)
        permission = Permission.objects.get(
            codename="can_downvote_tips",
            content_type=content_type,
        )

        count = 0
        for user in queryset:
            if user.user_permissions.filter(pk=permission.pk).exists():
                user.user_permissions.remove(permission)
                count += 1

        self.message_user(
            request, f"Permission de downvote retirée à {count} utilisateur(s)."
        )

    revoke_downvote_permission.short_description = "❌ Retirer permission de downvote"  # type: ignore


@admin.register(Tip)
class TipAdmin(admin.ModelAdmin):
    list_display = [
        "content_preview",
        "author",
        "date",
        "upvote_count",
        "downvote_count",
        "net_votes",
        "has_downvotes",
    ]
    list_filter = ["date", "author"]
    search_fields = ["content", "author__username"]
    ordering = ["-date"]
    readonly_fields = ["date"]

    def content_preview(self, obj):
        return obj.content[:100] + "..." if len(obj.content) > 100 else obj.content

    content_preview.short_description = "Content Preview"  # type: ignore

    def has_downvotes(self, obj):
        count = obj.downvote_count()
        if count > 0:
            return f"👎 {count}"
        return "✅ No downvotes"

    has_downvotes.short_description = "Downvote Status"  # type: ignore

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
