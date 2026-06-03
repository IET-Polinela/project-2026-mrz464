// Objek penampung template tampilan komponen UI/UX Portal Warga
const routes = {
    '#login': `
        <div class="row justify-content-center mt-5">
            <div class="col-12 col-md-6 col-lg-4">
                <div class="card shadow-sm border-0 p-4">
                    <h4 class="text-center fw-bold mb-4 text-primary">Login Warga</h4>
                    <form id="loginForm">
                        <div class="mb-3">
                            <label class="form-label fw-semibold text-muted">Username</label>
                            <input type="text" id="loginUsername" class="form-control form-control-lg fs-6" placeholder="Masukkan username" required>
                        </div>
                        <div class="mb-3">
                            <label class="form-label fw-semibold text-muted">Password</label>
                            <input type="password" id="loginPassword" class="form-control form-control-lg fs-6" placeholder="Masukkan password" required>
                        </div>
                        <button type="submit" class="btn btn-primary btn-lg w-100 fw-bold fs-6 shadow-sm mt-2">
                            <i class="bi bi-box-arrow-in-right me-2"></i>Masuk
                        </button>
                    </form>
                </div>
            </div>
        </div>
    `,
    '#dashboard': `
        <div class="row g-4">
            <aside class="col-12 col-lg-3">
                <div class="card border-0 p-3 shadow-sm sticky-top" style="top: 20px;">
                    <button class="btn btn-primary btn-lg w-100 fw-bold shadow-sm mb-3">
                        <i class="bi bi-plus-circle-fill me-2"></i>Laporan Baru
                    </button>
                    <button onclick="logout()" class="btn btn-outline-danger w-100 fw-bold">
                        <i class="bi bi-box-arrow-right me-2"></i>Keluar
                    </button>
                </div>
            </aside>

            <section class="col-12 col-lg-6">
                <div class="card border-0 p-5 shadow-sm text-center text-muted border-dashed">
                    <i class="bi bi-inbox fs-1 text-primary mb-3"></i>
                    <h5 class="fw-bold text-dark">Selamat Datang di Portal Warga!</h5>
                    <p class="small">Koneksi API data laporan real-time dari backend Django akan diimplementasikan pada Lab 12.</p>
                </div>
            </section>

            <aside class="col-12 col-lg-3 d-none d-lg-block">
                <div class="card border-0 p-3 shadow-sm sticky-top" style="top: 20px;">
                    <h6 class="fw-bold text-primary mb-3">
                        <i class="bi bi-info-circle-fill me-2"></i>Informasi Proyek
                    </h6>
                    <p class="small text-muted mb-0">Gunakan portal headless SPA ini untuk melaporkan kerusakan infrastruktur umum di wilayah Pasir Sakti.</p>
                </div>
            </aside>
        </div>
    `
};

// Fungsi utama penanganan rute navigasi SPA
function handleRouting() {
    // Jika tidak ada hash di URL browser, arahkan default ke #login
    const hash = window.location.hash || '#login';
    const contentDiv = document.getElementById('app-content');

    // Proteksi Keamanan Halaman Dashboard (Wajib Login)
    if (hash === '#dashboard' && !localStorage.getItem('access_token')) {
        window.location.hash = '#login';
        return;
    }

    // Proteksi Halaman Login (Kalau sudah punya token, langsung lempar ke dashboard)
    if (hash === '#login' && localStorage.getItem('access_token')) {
        window.location.hash = '#dashboard';
        return;
    }

    // Suntikkan template HTML ke dalam index.html secara dinamis
    contentDiv.innerHTML = routes[hash] || routes['#login'];

    // Pasang ulang event listener form jika user sedang berada di halaman login
    if (hash === '#login' && typeof setupLoginForm === 'function') {
        setupLoginForm();
    }
}

// Daftarkan fungsi ke event listener browser
window.addEventListener('hashchange', handleRouting);
window.addEventListener('DOMContentLoaded', handleRouting);