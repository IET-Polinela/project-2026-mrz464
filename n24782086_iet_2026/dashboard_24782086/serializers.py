from rest_framework import serializers
from .models import Report

class ReportSerializer(serializers.ModelSerializer):
    # Menggunakan SerializerMethodField untuk anonimitas 
    reporter = serializers.SerializerMethodField()

    class Meta:
        model = Report
        fields = ['id', 'title', 'category', 'description', 'location', 'status', 'reporter', 'created_at', 'updated_at']

    def get_reporter(self, obj):
        # Mengembalikan string statis untuk privasi warga [cite: 72, 83]
        return "Warga Anonim"