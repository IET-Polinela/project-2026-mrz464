/**
 * Fungsi untuk menginisialisasi event listener pada Formulir Login Warga.
 * Dipanggil secara otomatis oleh router.js ketika rute #login aktif.
 */
function setupLoginForm() {
    const form = document.getElementById('loginForm');
    if (!form) return;

    form.addEventListener('submit', async (event) => {
        event.preventDefault(); // Mencegah browser melakukan reload halaman bawaan

        const usernameInput = document.getElementById('loginUsername').value;
        const passwordInput = document.getElementById('loginPassword').value;

        // Amankan data ke dalam format objek payload JSON
        const payload = {
            username: usernameInput,
            password: passwordInput
        };

        try {
            // Mengirim data login ke endpoint JWT token milik backend Django
            const response = await requestAPI('/api/token/', 'POST', payload);

            if (response.status === 200) {
                const data = await response.json();

                // Menyimpan pasangan token JWT ke dalam memori localStorage browser
                localStorage.setItem('access_token', data.access);
                localStorage.setItem('refresh_token', data.refresh);

                alert('Login Berhasil! Selamat Datang di Portal Warga Pasir Sakti.');

                // Alihkan halaman SPA secara instan ke dashboard warga
                window.location.hash = '#dashboard';
            } else {
                alert('Login Gagal! Kombinasi Username atau Password salah.');
            }
        } catch (error) {
            alert('Gagal terhubung dengan server backend Django.');
        }
    });
}

/**
 * Fungsi untuk menghapus sesi login aktif (Aksi Tombol Keluar).
 * Dipanggil lewat atribut onclick="logout()" di template dashboard.
 */
function logout() {
    // Bersihkan token dari penyimpanan lokal browser
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');

    // Kembalikan rute navigasi ke halaman login awal
    window.location.hash = '#login';
    alert('Anda telah keluar dari sistem Portal Warga.');
}