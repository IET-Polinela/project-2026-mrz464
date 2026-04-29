from django.contrib.auth.models import AbstractUser
from django.db import models

# Pastikan nama kelasnya 'User' dengan 'U' besar
class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_member = models.BooleanField(default=True)