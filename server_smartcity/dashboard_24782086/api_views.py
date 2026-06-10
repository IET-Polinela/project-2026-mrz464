from rest_framework import viewsets, permissions
from main_app.models import Report  # FIX: Ambil dari main_app yang punya kolom reporter!
from .serializers import ReportSerializer
from .permissions import IsOwnerAndDraftOrReadOnly 

class ReportViewSet(viewsets.ModelViewSet):
    """
    ViewSet untuk REST API Laporan Smart City Pasir Sakti (Refactoring Lab 10).
    Mendukung CRUD otomatis aman berbasis JWT Token.
    """
    # Ditambahkan .order_by('-id') agar data terbaru Rez selalu muncul paling atas
    queryset = Report.objects.all().order_by('-id')
    serializer_class = ReportSerializer

    def get_permissions(self):
        """
        Mengatur hak akses dinamis secara ketat (Aturan Lab 10):
        - Edit (update, partial_update) dan Hapus (destroy) wajib pemilik & status DRAFT.
        - Akses lainnya (List, Detail, Create) hanya butuh login umum (IsAuthenticated).
        """
        if self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsOwnerAndDraftOrReadOnly()]
        
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        """
        Mengunci otomatis field reporter dari user token yang aktif (request.user)
        mencegah celah ID spoofing dari Postman.
        """
        serializer.save(reporter=self.request.user)