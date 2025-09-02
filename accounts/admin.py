from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
	fieldsets = BaseUserAdmin.fieldsets + (
		("Roles", {"fields": ("role",)}),
	)
	list_display = ("username", "email", "first_name", "last_name", "role", "is_staff")
	list_filter = BaseUserAdmin.list_filter + ("role",)

# Register your models here.
