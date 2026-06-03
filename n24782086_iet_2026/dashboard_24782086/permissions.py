from rest_framework import permissions

class IsOwnerAndDraftOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # Jika metodenya adalah GET, HEAD, atau OPTIONS (Akses Membaca), langsung izinkan
        if request.method in permissions.SAFE_METHODS:
            return True

        # Untuk metode PUT, PATCH, dan DELETE (Akses Mengubah/Menghapus):
        # Jalankan validasi kepemilikan dan status laporan
        return obj.reporter == request.user and obj.status == 'DRAFT'