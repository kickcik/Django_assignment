from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User


@admin.register(User)
class UserAdmin(UserAdmin):
    model = User
    # 리스트 화면에서 보이는 컬럼들
    list_display = ("email", "name", "is_staff", "is_active")
    list_filter = ("is_staff", "is_active")

    # admin에서 편집할 때 폼에 보이는 필드 그룹
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("name",)}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login",)}),
    )

    # 새 유저 추가할 때 보이는 필드
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "name", "password1", "password2", "is_staff", "is_active")}
        ),
    )

    search_fields = ("email", "name")
    ordering = ("email",)

    class Meta:
        verbose_name = '유저'
        verbose_name_plural = f'{verbose_name} 목록'
