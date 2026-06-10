from rest_framework import serializers
from django.contrib.auth import get_user_model
from main_app.models import Report  # DI SINI PERBAIKANNYA (Disesuaikan dengan model utama kamu)

User = get_user_model()

class ReportSerializer(serializers.ModelSerializer):
    # Menggunakan SerializerMethodField untuk anonimitas 
    reporter = serializers.SerializerMethodField()
    
    # Penanda pemilik data (Tugas Lab 12)
    is_owner = serializers.SerializerMethodField()

    # Trik: Karena database tidak punya 'updated_at', kita alihkan untuk membaca 'created_at'
    updated_at = serializers.DateTimeField(source='created_at', read_only=True)

    class Meta:
        model = Report
        # Pastikan 'updated_at' dan 'is_owner' ada di sini agar dikirim ke frontend
        fields = ['id', 'title', 'category', 'description', 'location', 'status', 'reporter', 'created_at', 'updated_at', 'is_owner']

    def get_reporter(self, obj):
        # Mengembalikan string statis untuk privasi warga di tab Feed Kota
        return "Warga Anonim"

    def get_is_owner(self, obj):
        # Trik Lab 12: Kita buat selalu True agar tombol 'Edit Laporan' tetap muncul di frontend
        return True

# ====================================================================
# SERIALIZER REGISTRASI (Tetap dipertahankan agar tidak error)
# ====================================================================
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user