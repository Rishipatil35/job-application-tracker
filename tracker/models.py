from django.conf import settings
from django.db import models

class JobApplication(models.Model):
    class Status(models.TextChoices):
        APPLIED = 'applied', 'Applied'
        INTERVIEW = 'interview', 'Interview'
        OFFER = 'offer', 'Offer'
        REJECTED = 'rejected', 'Rejected'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='applications')
    company = models.CharField(max_length=150)
    role = models.CharField(max_length=150)
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.APPLIED)
    applied_date = models.DateField()
    job_url = models.URLField(blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-applied_date', '-created_at']

    def __str__(self):
        return f'{self.company} - {self.role}'
