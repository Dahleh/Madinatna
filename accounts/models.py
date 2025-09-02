from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models import ManyToManyField


class User(AbstractUser):
	class Roles(models.TextChoices):
		ADMIN = 'admin', 'Admin'
		MANAGER = 'manager', 'Manager'
		OWNER = 'owner', 'Owner'
		TENANT = 'tenant', 'Tenant'
		USER = 'user', 'User'

	role = models.CharField(max_length=20, choices=Roles.choices, default=Roles.USER)
	# favorites
	favorite_facilities = ManyToManyField(
		'facilities.Facility', related_name='favorited_by', blank=True
	)

	def is_admin(self):
		return self.role == self.Roles.ADMIN or self.is_superuser

	def __str__(self):
		return f"{self.username} ({self.role})"

# Create your models here.
