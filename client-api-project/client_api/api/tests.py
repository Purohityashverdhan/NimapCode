from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Client, Project


class ClientAPITestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)

    def test_create_client(self):
        url = reverse('client-list-create')
        data = {'client_name': 'Test Client'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['client_name'], 'Test Client')

    def test_get_clients(self):
        Client.objects.create(client_name='Test Client', created_by=self.user)
        url = reverse('client-list-create')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)


class ProjectAPITestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)
        self.client_instance = Client.objects.create(client_name='Client A', created_by=self.user)

    def test_create_project(self):
        url = reverse('client-projects-create', kwargs={'client_id': self.client_instance.id})
        data = {'project_name': 'Project A', 'users': [self.user.id]}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['project_name'], 'Project A')

    def test_get_user_projects(self):
        project = Project.objects.create(project_name='Project A', client=self.client_instance, created_by=self.user)
        project.users.add(self.user)
        url = reverse('user-projects')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)
