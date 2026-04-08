from django import forms
from .models import Report

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        # Field yang akan muncul di halaman web untuk diisi user
        fields = ['title', 'category', 'description', 'location']