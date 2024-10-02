from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from .models import User


class UserTests(APITestCase):
    def setUp(self):
        user1 = {'email': 'testuser@example.com', 'name': 'Test User', 'password': 'testpassword', 'role': 'user'}
        user2_admin = {'email': 'testuseradmin@example.com', 'name': 'Test Admin User', 'password': 'testpassword',
                       'role': 'admin'}
        User.objects.create_user(**user1)
        User.objects.create_user(**user2_admin)

    def test_register_user(self):
        """ Регистрация пользователя """
        url = reverse('register')
        data = {'email': 'testuser1@example.com', 'name': 'Test User1', 'password': 'testpassword', 'role': 'user'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_user_by_admin(self):
        """ Создание пользователя адинистратором """
        admin_user = User.objects.get(email='testuseradmin@example.com')
        self.client.force_authenticate(user=admin_user)

        url = reverse('user-list')
        data = {'email': 'testuser2@example.com', 'name': 'Test User2', 'password': 'testpassword', 'role': 'user'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_user_by_admin(self):
        """ Редактирование пользователя """
        admin_user = User.objects.get(email='testuseradmin@example.com')
        self.client.force_authenticate(user=admin_user)

        url = reverse('user-detail', kwargs={'pk': admin_user.id})
        data = {'name': 'Changed Administrator'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_user_by_user(self):
        """ Создание пользователя обычным пользователем """
        url = reverse('user-list')

        user = User.objects.get(email='testuser@example.com')
        self.client.force_authenticate(user=user)

        data = {'email': 'testuser3@example.com', 'name': 'Test User3', 'password': 'testpassword', 'role': 'user'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_login(self):
        """ Авторизация """
        url = reverse('token_obtain_pair')
        data = {'email': 'testuser@example.com', 'password': 'testpassword'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
