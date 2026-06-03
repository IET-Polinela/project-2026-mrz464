from rest_framework import generics, permissions
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    """
    View API untuk mengizinkan Citizen melakukan registrasi akun secara mandiri via REST API.
    """
    queryset = User.objects.all()
    # Menggunakan AllowAny agar endpoint dapat diakses oleh publik tanpa token
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer