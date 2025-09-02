from django.contrib import admin
from .models import Category, Cluster, Facility, FacilityImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ("name", "description")
	search_fields = ("name",)


@admin.register(Cluster)
class ClusterAdmin(admin.ModelAdmin):
	list_display = ("name", "description")
	search_fields = ("name",)


class FacilityImageInline(admin.TabularInline):
	model = FacilityImage
	extra = 1


@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
	list_display = ("name", "category", "cluster", "is_active", "owner")
	list_filter = ("category", "cluster", "is_active")
	search_fields = ("name", "description")
	autocomplete_fields = ("category", "cluster", "owner")
	inlines = [FacilityImageInline]

# Register your models here.
