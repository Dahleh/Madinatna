from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Category, Cluster, Facility
from rest_framework_simplejwt.tokens import RefreshToken


User = get_user_model()


class FacilitiesApiTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(username='admin', password='pass', role='admin')
        self.cat = Category.objects.create(name='Sports')
        self.cluster = Cluster.objects.create(name='Cluster A')
        # issue JWT for admin to use on requests
        access = str(RefreshToken.for_user(self.admin).access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')

    def test_list_facilities_empty(self):
        url = '/api/facilities/'
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.json(), [])

    def test_create_facility_admin(self):
        url = '/api/facilities/'
        payload = {
            'name': 'Tennis Court',
            'description': 'Outdoor court',
            'category_id': self.cat.id,
            'cluster_id': self.cluster.id,
            'is_active': True,
        }
        res = self.client.post(url, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Facility.objects.count(), 1)
