import uuid
from django.db import models

class Employee(models.Model):
    # Auto-generated
    employee_id = models.CharField(max_length=20, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    language = models.CharField(max_length=5, default='en', choices=[('en','English'),('zh','Chinese'),('ar','Arabic')])

    # Phase 1: Personal Info
    full_name = models.CharField(max_length=200)
    english_name = models.CharField(max_length=200, blank=True, default='')
    phone = models.CharField(max_length=30, blank=True, default='')
    email = models.EmailField(blank=True, default='')
    role = models.CharField(max_length=200, blank=True, default='')
    id_type = models.CharField(max_length=20, blank=True, default='id')
    id_number = models.CharField(max_length=100, blank=True, default='')
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)

    # Phase 2: Work Responses (JSON)
    role_responsibilities = models.JSONField(default=dict, blank=True)
    workflow_efficiency = models.JSONField(default=dict, blank=True)
    pain_points = models.JSONField(default=dict, blank=True)
    communication = models.JSONField(default=dict, blank=True)
    tools_technology = models.JSONField(default=dict, blank=True)
    ideas_suggestions = models.JSONField(default=dict, blank=True)

    # Trust confirmation
    consent_given = models.BooleanField(default=False)

    # Generated assets
    qr_code = models.ImageField(upload_to='qrcodes/', blank=True, null=True)
    id_card = models.ImageField(upload_to='idcards/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.employee_id:
            self.employee_id = f"BBR-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.full_name} ({self.employee_id})"

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Employee Submission'
        verbose_name_plural = 'Employee Submissions'
