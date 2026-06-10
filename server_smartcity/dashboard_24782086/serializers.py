from rest_framework import serializers
from django.contrib.auth import get_user_model
from main_app.models import Report  # Memastikan mengambil model utama yang sama

User = get_user_model()

class ReportSerializer(serializers.ModelSerializer):
    # Menggunakan SerializerMethodField untuk anonimitas warga (Tugas Lab)
    reporter = serializers.SerializerMethodField()
    
    # Penanda pemilik data berbasis Token JWT
    is_owner = serializers.SerializerMethodField()

    # Trik Lab: Mengalihkan updated_at membaca created_at karena di DB tidak ada
    updated_at = serializers.DateTimeField(source='created_at', read_only=True)

    class Meta:
        model = Report
        fields = ['id', 'title', 'category', 'description', 'location', 'status', 'reporter', 'created_at', 'updated_at', 'is_owner']

    def get_reporter(self, obj):
        # Menjaga privasi warga di tab Feed Kota
        return "Warga Anonim"

    def get_is_owner(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            # Mengembalikan True hanya jika user yang login adalah pemilik asli di database
            return obj.reporter == request.user
        return False

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