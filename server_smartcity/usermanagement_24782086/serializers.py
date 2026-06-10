from rest_framework import serializers
from django.contrib.auth import get_user_model
from main_app.models import Report  # Mengambil model Report utama

User = get_user_model()

# ====================================================================
# SERIALIZER UNTUK REGISTRASI AKUN BARU
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


# ====================================================================
# SERIALIZER UNTUK DATA LAPORAN (UNTUK API SPA PORTAL WARGA)
# ====================================================================
class ReportSerializer(serializers.ModelSerializer):
    is_owner = serializers.SerializerMethodField()
    reporter = serializers.ReadOnlyField(source='reporter.username')

    class Meta:
        model = Report
        fields = ['id', 'title', 'category', 'description', 'location', 'status', 'reporter', 'is_owner', 'created_at']

    # KUNCI UTAMA: Memeriksa secara real-time apakah baris data ini milik user yang sedang login
    def get_is_owner(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.reporter == request.user  # Bernilai True HANYA jika data di DB cocok dengan user JWT
        return False