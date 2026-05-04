import random
from django.core.management.base import BaseCommand
from faker import Faker
from main_app.models import Report

# Inisialisasi Faker dengan lokalisasi Indonesia
fake = Faker('id_ID')

class Command(BaseCommand):
    help = 'Generate contextual fake reports for Pasir Sakti'

    def add_arguments(self, parser):
        parser.add_argument('num_records', type=int, help='Jumlah data yang ingin dibuat')

    def handle(self, *args, **kwargs):
        num_records = kwargs['num_records']

        # 1. MENGHAPUS DATA LAMA (Agar grafik langsung terlihat perbedaannya)
        self.stdout.write(self.style.WARNING('Menghapus data laporan lama...'))
        Report.objects.all().delete()
        
        # 2. Mapping Kategori dengan judul dan deskripsi
        context_data = {
            'Jalan Rusak': {
                'titles': ['Lubang Besar', 'Aspal Mengelupas', 'Jalan Bergelombang', 'Ambles'],
                'desc': 'Ditemukan kerusakan jalan yang cukup dalam di area ini.'
            },
            'Sampah': {
                'titles': ['Tumpukan Sampah', 'Bau Menyengat', 'TPS Melebihi Kapasitas'],
                'desc': 'Warga mengeluhkan penumpukan sampah yang belum diangkut.'
            },
            'Drainase': {
                'titles': ['Saluran Mampet', 'Drainase Meluap', 'Tutup Got Pecah'],
                'desc': 'Saluran air tersumbat sehingga air meluap saat hujan.'
            },
            'Lampu Mati': {
                'titles': ['Lampu Jalan Mati', 'Penerangan Redup', 'Kabel Putus'],
                'desc': 'Lampu jalan di area ini mati total, membahayakan pengguna jalan.'
            },
            'Keamanan': {
                'titles': ['Aksi Vandalisme', 'Pencurian Kabel', 'Aktivitas Mencurigakan'],
                'desc': 'Dibutuhkan patroli tambahan di area ini terkait ketertiban umum.'
            }
        }

        # --- PENGATURAN BOBOT (AGAR GRAFIK TIDAK RATA) ---
        categories = list(context_data.keys())
        # Bobot Kategori: Jalan Rusak (40%), Sampah (30%), Drainase (15%), Lampu (10%), Keamanan (5%)
        category_weights = [40, 30, 15, 10, 5] 

        status_choices = ['REPORTED', 'VERIFIED', 'IN_PROGRESS', 'RESOLVED']
        # Bobot Status: RESOLVED (45%), REPORTED (35%), VERIFIED (10%), IN_PROGRESS (10%)
        status_weights = [35, 10, 10, 45]

        for _ in range(num_records):
            # Memilih kategori dan status berdasarkan BOBOT (bukan acak rata)
            category = random.choices(categories, weights=category_weights, k=1)[0]
            status = random.choices(status_choices, weights=status_weights, k=1)[0]

            title_template = random.choice(context_data[category]['titles'])
            description_base = context_data[category]['desc']

            # Membuat baris data baru di tabel Report
            Report.objects.create(
                title=f"{title_template} di {fake.street_name()}",
                category=category,
                description=f"{description_base} Detail: {fake.street_address()}.",
                location=f"Kecamatan {fake.city()}, {fake.address()}",
                status=status
            )

        self.stdout.write(self.style.SUCCESS(f'Berhasil membuat {num_records} laporan dengan pola distribusi yang realistis!'))