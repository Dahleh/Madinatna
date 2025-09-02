from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from facilities.models import Category, Cluster, Facility
from rest_framework_simplejwt.tokens import RefreshToken


User = get_user_model()


class SignupAndFavoritesTests(TestCase):
	def setUp(self):
		self.client = APIClient()
		self.cat = Category.objects.create(name='Food')
		self.cluster = Cluster.objects.create(name='B')
		self.facility = Facility.objects.create(
			name='Cafe', category=self.cat, cluster=self.cluster
		)

	def test_signup(self):
		res = self.client.post('/api/auth/signup/', {
			'username': 'newuser',
			'email': 'new@user.com',
			'password': 'secret123'
		}, format='json')
		self.assertEqual(res.status_code, 201)
		u = User.objects.get(username='newuser')
		self.assertEqual(u.role, 'user')

	def test_favorite_flow(self):
		user = User.objects.create_user(username='fav', password='pass')
		# Use JWT for auth
		access = RefreshToken.for_user(user).access_token
		self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(access)}')
		# add favorite
		res = self.client.post(f'/api/facilities/{self.facility.id}/favorite/')
		self.assertEqual(res.status_code, 200)
		# list favorites
		res = self.client.get('/api/facilities/favorites/')
		self.assertEqual(res.status_code, 200)
		self.assertEqual(len(res.json()), 1)
		# remove favorite
		res = self.client.post(f'/api/facilities/{self.facility.id}/unfavorite/')
		self.assertEqual(res.status_code, 200)
		res = self.client.get('/api/facilities/favorites/')
		self.assertEqual(len(res.json()), 0)

	def test_jwt_signin(self):
		user = User.objects.create_user(username='jwtuser', password='pass')
		res = self.client.post('/api/auth/signin/', {
			'username': 'jwtuser',
			'password': 'pass'
		}, format='json')
		self.assertEqual(res.status_code, 200)
		access = res.json()['access']
		# call an authed endpoint with bearer
		client = APIClient()
		client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')
		res = client.get('/api/facilities/favorites/')
		self.assertEqual(res.status_code, 200)
