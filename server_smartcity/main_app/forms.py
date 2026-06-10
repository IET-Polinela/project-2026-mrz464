from django import forms
from .models import Report

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        # Sesuaikan fields dengan yang ada di model kamu
        fields = ['title', 'category', 'description', 'location'] 
        
        # Ini bagian pentingnya: Menambahkan class Bootstrap ke form
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan judul laporan'}),
            'category': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contoh: Infrastruktur, Lingkungan'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Jelaskan detail masalahnya...'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Lokasi spesifik kejadian'}),
        }