from datetime import date
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from .models import JobApplication

class TrackerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='alice', password='StrongPass123!')
        self.other = User.objects.create_user(username='bob', password='StrongPass123!')
        self.job = JobApplication.objects.create(user=self.user, company='Example', role='Developer', applied_date=date.today())

    def test_dashboard_requires_login(self):
        self.assertEqual(self.client.get(reverse('dashboard')).status_code, 302)

    def test_user_cannot_edit_another_users_job(self):
        self.client.force_login(self.other)
        response = self.client.get(reverse('edit_application', args=[self.job.pk]))
        self.assertEqual(response.status_code, 404)

    def test_user_cannot_delete_another_users_job(self):
        self.client.force_login(self.other)
        response = self.client.post(reverse('delete_application', args=[self.job.pk]))
        self.assertEqual(response.status_code, 404)
        self.assertTrue(JobApplication.objects.filter(pk=self.job.pk).exists())

    def test_add_application(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('add_application'), {
            'company': 'New Co', 'role': 'Intern', 'status': 'applied', 'applied_date': '2026-11-01'})
        self.assertRedirects(response, reverse('dashboard'))
        self.assertTrue(JobApplication.objects.filter(company='New Co', user=self.user).exists())
