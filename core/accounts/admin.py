from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile
from blog.models import Post, Category
from comment.models import Comment_Like, Comments

# Register your models here.


class AdminCustom(UserAdmin):
    model = User
    list_display = ("email", "is_superuser", "is_active", "is_staff", "is_verified")
    list_filter = ("email", "is_superuser", "is_active", "is_verified")
    search_fields = ("email",)
    ordering = ("email",)
    fieldsets = (
        (
            "Authenticated",
            {
                "fields": (
                    "email",
                    "password",
                ),
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_staff",
                    "is_superuser",
                    "is_active",
                    "is_verified",
                ),
            },
        ),
        (
            "Group Permissions",
            {
                "fields": ("groups", "user_permissions"),
            },
        ),
        (
            "Importent Dates",
            {
                "fields": ("last_login",),
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                    "is_superuser",
                    "is_verified",
                ),
            },
        ),
    )


admin.site.register(Comments)
admin.site.register(Comment_Like)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Profile)
admin.site.register(User, AdminCustom)
