from django.test import TestCase
from rest_framework.test import APIRequestFactory

from .serializers import UserSerializer
from .models import User
from .views import GetUserToken

class UserModelTests(TestCase):
    def setUp(self):
        self.test_user = {'username': 'test', 'password': 'test', 'email': 'test@test.com', 'is_admin': False}

        user = UserSerializer(data=self.test_user)
        user.is_valid(raise_exception=True)
        user.save()
        

    def test_create_correctly(self):
        user = User.objects.get(username=self.test_user['username'])

        self.assertEqual(user.username, self.test_user['username'])
        self.assertEqual(user.email, self.test_user['email'])
        self.assertEqual(user.is_admin, self.test_user['is_admin'])
        self.assertNotEqual(user.password, self.test_user['password'])

    def test_updated_correctly(self):
        instance = User.objects.get(username=self.test_user['username'])
        data = {'username': 'tester', 'password': 'test', 'email': 'tester@test.com', 'is_admin': True}

        user = UserSerializer(instance=instance, data=data)
        user.is_valid(raise_exception=True)
        user.save()

        # Updated user
        ud_user = User.objects.get(id=instance.id)

        # Check if username was updated
        self.assertEqual(ud_user.username, data['username'])
        # Check if email was updated
        self.assertEqual(ud_user.email, data['email'])
        # Check if is_admin was not updated
        self.assertNotEqual(ud_user.is_admin, data['is_admin'])
        # Check if password was hashed
        self.assertNotEqual(ud_user.password, data['password'])


class UserApiTests(TestCase):
    def test_token_endpoint_response(self):
        User.objects.create_superuser(email='admin@email.com', password='admin', username='admin')

        factory = APIRequestFactory()
        request = factory.post('/api-auth/', {'username': 'admin@email.com', 'password': 'admin'}, format='json')
        view = GetUserToken.as_view()
        response = view(request)

        self.assertIs(response.status_code, 200)
        self.assertTrue('token' in response.data)
        self.assertTrue('user_id' in response.data)
        self.assertTrue('user_name' in response.data)