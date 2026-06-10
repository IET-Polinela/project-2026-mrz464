from django.db import models
from django.conf import settings # Wajib di-import untuk memanggil User Model

class Report(models.Model):
    STATUS_CHOICES = [
        ('DRAFT', 'Draft'), 
        ('REPORTED', 'Reported'),
        ('VERIFIED', 'Verified'),
        ('IN_PROGRESS', 'In Progress'),
        ('RESOLVED', 'Resolved'),
    ]

    title = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=200)
    
    # INI DIA YANG WAJIB ADA AGAR TIDAK ATTRIBUTE ERROR:
    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='main_reports', 
        null=True, 
        blank=True
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='REPORTED'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title