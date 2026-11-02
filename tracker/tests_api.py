from datetime import date
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from django.urls import reverse
from .models import JobApplication


class ApplicationAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='one', password='StrongPass123!')
        self.other = User.objects.create_user(username='two', password='StrongPass123!')
        self.job = JobApplication.objects.create(user=self.user, company='Alpha', role='Backend', applied_date=date(2026, 11, 1))
        JobApplication.objects.create(user=self.other, company='Private', role='Engineer', applied_date=date(2026, 11, 1))

    def test_login_required(self):
        response = self.client.get('/api/applications/')
        self.assertIn(response.status_code, [401, 403])

    def test_only_my_jobs_in_list(self):
        self.client.force_authenticate(self.user)
        response = self.client.get('/api/applications/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['company'], 'Alpha')

    def test_cannot_read_or_modify_another_users_job(self):
        self.client.force_authenticate(self.other)
        detail = f'/api/applications/{self.job.pk}/'
        self.assertEqual(self.client.get(detail).status_code, 404)
        self.assertEqual(self.client.patch(detail, {'status': 'offer'}).status_code, 404)
        self.assertEqual(self.client.delete(detail).status_code, 404)

    def test_create_and_filter(self):
        self.client.force_authenticate(self.user)
        response = self.client.post('/api/applications/', {'company': 'New Place', 'role': 'Intern', 'status': 'interview', 'applied_date': '2026-11-02'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(JobApplication.objects.get(pk=response.data['id']).user, self.user)
        filtered = self.client.get('/api/applications/?status=interview&q=New')
        self.assertEqual(filtered.data['count'], 1)

    def test_stats_scoped_to_user(self):
        self.client.force_authenticate(self.user)
        data = self.client.get('/api/applications/stats/').data
        self.assertEqual(data['total'], 1)
        self.assertEqual(data['applied'], 1)

    def test_invalid_status_is_rejected(self):
        self.client.force_authenticate(self.user)
        response = self.client.patch(f'/api/applications/{self.job.pk}/', {'status': 'fake'})
        self.assertEqual(response.status_code, 400)

    def test_csrf_required_on_session_write(self):
        from rest_framework.test import APIClient
        client = APIClient(enforce_csrf_checks=True)
        client.force_login(self.user)
        response = client.post('/api/applications/', {'company':'Test', 'role':'Intern', 'applied_date':'2026-11-01'})
        self.assertEqual(response.status_code, 403)
