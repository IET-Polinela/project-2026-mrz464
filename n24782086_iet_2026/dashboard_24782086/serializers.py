from rest_framework import serializers
from .models import Report

class ReportSerializer(serializers.ModelSerializer):
    # Menggunakan SerializerMethodField untuk anonimitas 
    reporter = serializers.SerializerMethodField()

    class Meta:
        model = Report
        fields = ['id', 'title', 'category', 'description', 'location', 'status', 'reporter', 'created_at', 'updated_at']

    def get_reporter(self, obj):
        # Mengembalikan string statis untuk privasi warga
        return "Warga Anonim"
    
from rest_framework import serializers
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    # Menambahkan write_only agar password tidak ikut membalas saat data di-return (Aman)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        # Menggunakan create_user bawaan Django agar password otomatis di-hashing di database
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user