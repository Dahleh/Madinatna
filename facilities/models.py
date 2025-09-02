from django.db import models
from django.conf import settings


class Category(models.Model):
	name = models.CharField(max_length=100, unique=True)
	description = models.TextField(blank=True)

	def __str__(self):
		return self.name


class Cluster(models.Model):
	name = models.CharField(max_length=100, unique=True)
	description = models.TextField(blank=True)

	def __str__(self):
		return self.name


class Facility(models.Model):
	name = models.CharField(max_length=150)
	description = models.TextField(blank=True)
	category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='facilities')
	cluster = models.ForeignKey(Cluster, on_delete=models.PROTECT, related_name='facilities')
	address = models.CharField(max_length=255, blank=True)
	phone = models.CharField(max_length=50, blank=True)
	email = models.EmailField(blank=True)
	is_active = models.BooleanField(default=True)
	owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name='owned_facilities')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		unique_together = ("name", "cluster")

	def __str__(self):
		return f"{self.name} - {self.cluster}"


class FacilityImage(models.Model):
	facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name='images')
	image = models.ImageField(upload_to='facility_images/')
	caption = models.CharField(max_length=200, blank=True)
	order = models.PositiveIntegerField(default=0)

	class Meta:
		ordering = ["order", "id"]

	def __str__(self):
		return f"Image for {self.facility}"

"""Models end."""

# Create your models here.
