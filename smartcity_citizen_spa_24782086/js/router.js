// Objek penampung template tampilan komponen UI/UX Portal Warga
const routes = {
    '#login': `
        <div class="row justify-content-center mt-5">
            <div class="col-12 col-md-6 col-lg-4">
                <div class="card shadow-sm border-0 p-4 bg-white rounded-3">
                    <h4 class="text-center fw-bold mb-4 text-dark" style="font-family: sans-serif;">Login Warga</h4>
                    <form id="loginForm">
                        <div class="mb-3">
                            <label class="form-label fw-semibold text-muted small">Username</label>
                            <input type="text" id="loginUsername" class="form-control form-control-lg fs-6 bg-light" placeholder="Masukkan username" required>
                        </div>
                        <div class="mb-3">
                            <label class="form-label fw-semibold text-muted small">Password</label>
                            <input type="password" id="loginPassword" class="form-control form-control-lg fs-6 bg-light" placeholder="Masukkan password" required>
                        </div>
                        <button type="submit" class="btn btn-primary btn-lg w-100 fw-bold fs-6 shadow-sm mt-3">
                            Masuk
                        </button>
                    </form>
                </div>
            </div>
        </div>
    `,
    '#register': `
        <div class="row justify-content-center mt-5">
            <div class="col-12 col-md-6 col-lg-5">
                <div class="card shadow-sm border-0 p-4 bg-white rounded-3">
                    <h4 class="text-center fw-bold mb-4 text-dark" style="font-family: sans-serif;">Daftar Akun Baru</h4>
                    <form id="registerForm">
                        <div class="mb-3">
                            <label class="form-label fw-semibold text-muted small">Username</label>
                            <input type="text" id="regUsername" class="form-control form-control-lg fs-6 bg-light" placeholder="Buat username baru" required>
                        </div>
                        <div class="mb-3">
                            <label class="form-label fw-semibold text-muted small">Email</label>
                            <input type="email" id="regEmail" class="form-control form-control-lg fs-6 bg-light" placeholder="Masukkan alamat email aktif" required>
                        </div>
                        <div class="mb-3">
                            <label class="form-label fw-semibold text-muted small">Password</label>
                            <input type="password" id="regPassword" class="form-control form-control-lg fs-6 bg-light" placeholder="Buat password minimal 8 karakter" required>
                        </div>
                        <button type="submit" class="btn btn-success btn-lg w-100 fw-bold fs-6 shadow-sm mt-3" style="background-color: #198754 !important; border-color: #198754 !important;">
                            Daftar Sekarang
                        </button>
                    </form>
                </div>
            </div>
        </div>
    `,
    '#dashboard': `
        <div class="row g-4">
            <aside class="col-12 col-lg-3">
                <div class="card border-0 p-3 shadow-sm sticky-top" style="top: 90px;">
                    <button class="btn btn-primary btn-lg w-100 fw-bold shadow-sm mb-4" data-bs-toggle="modal" data-bs-target="#reportModal" onclick="resetForm()">
                        <i class="bi bi-plus-circle-fill me-2"></i>Buat Laporan Baru
                    </button>
                    
                    <div class="mb-2">
                        <h6 class="fw-bold text-muted mb-3 text-uppercase" style="font-size: 0.8rem; letter-spacing: 1px;">
                            <i class="bi bi-activity me-2"></i>Status Laporan Anda
                        </h6>
                        <ul class="list-group list-group-flush small" id="statusSummary">
                            <li class="list-group-item d-flex justify-content-between align-items-center px-0 bg-transparent">
                                <span><i class="bi bi-pencil-square me-2 text-secondary"></i>Draf</span> 
                                <span class="badge bg-secondary rounded-pill" id="countDraft">0</span>
                            </li>
                            <li class="list-group-item d-flex justify-content-between align-items-center px-0 bg-transparent">
                                <span><i class="bi bi-send-fill me-2 text-warning"></i>Diajukan</span> 
                                <span class="badge bg-warning text-dark rounded-pill" id="countReported">0</span>
                            </li>
                            <li class="list-group-item d-flex justify-content-between align-items-center px-0 bg-transparent">
                                <span><i class="bi bi-gear-fill me-2 text-info"></i>Diproses</span> 
                                <span class="badge bg-info rounded-pill" id="countProgress">0</span>
                            </li>
                            <li class="list-group-item d-flex justify-content-between align-items-center px-0 bg-transparent">
                                <span><i class="bi bi-check-circle-fill me-2 text-success"></i>Selesai</span> 
                                <span class="badge bg-success rounded-pill" id="countResolved">0</span>
                            </li>
                        </ul>
                    </div>
                </div>
            </aside>

            <section class="col-12 col-lg-6">
                <ul class="nav nav-pills nav-fill bg-white shadow-sm p-2 rounded mb-4" id="reportTabs">
                    <li class="nav-item">
                        <button class="nav-link active fw-bold" id="tabMyReports" onclick="switchTab('my_reports')">
                            Laporan Saya
                        </button>
                    </li>
                    <li class="nav-item">
                        <button class="nav-link fw-bold text-muted" id="tabFeed" onclick="switchTab('feed')">
                            Feed Kota (Publik)
                        </button>
                    </li>
                </ul>

                <div id="reportList" class="row g-3 row-cols-1 row-cols-md-2">
                    <div class="col-12 text-center text-muted py-5">
                        <div class="spinner-border text-primary" role="status"></div>
                        <p class="mt-2">Memuat data dari server...</p>
                    </div>
                </div>
                
                <div id="paginationContainer" class="d-flex justify-content-center mt-5 mb-5"></div>
            </section>

            <aside class="col-12 col-lg-3 d-none d-lg-block">
                <div class="card border-0 p-3 shadow-sm sticky-top" style="top: 90px;">
                    <h6 class="fw-bold text-primary mb-3">
                        <i class="bi bi-info-circle-fill me-2"></i>Informasi Proyek
                    </h6>
                    <p class="small text-muted mb-0">Portal ini menggunakan Fetch API dan JWT untuk mengelola laporan kerusakan fasilitas secara real-time.</p>
                </div>
            </aside>
        </div>
    `
};

// MANAJEMEN INJEKSI NAVBAR DINAMIS PERSIS DOSEN (IMAGE_F4951C & IMAGE_F5115E)
function updateGlobalNavbar(hash) {
    let navbarEl = document.getElementById('spa-global-navbar');
    const token = localStorage.getItem('access_token');

    // Jika wadah navbar belum ada di index.html, kita buat otomatis di atas app-content
    if (!navbarEl) {
        const contentDiv = document.getElementById('app-content');
        navbarEl = document.createElement('div');
        navbarEl.id = 'spa-global-navbar';
        contentDiv.parentNode.insertBefore(navbarEl, contentDiv);
    }

    if (token && hash === '#dashboard') {
        // Style Navbar Saat Logged In (Ada Nama User & Tombol Keluar)
        navbarEl.innerHTML = `
            <nav class="navbar navbar-expand-lg navbar-dark bg-primary shadow-sm mb-4 py-3" style="background-color: #0d6efd !important;">
                <div class="container">
                    <a class="navbar-brand fw-bold fs-4 text-white" href="#dashboard">Smart City Portal</a>
                    <div class="d-flex align-items-center gap-3 ms-auto text-white">
                        <span class="fw-semibold"><i class="bi bi-person-circle me-1"></i>Halo, Warga!</span>
                        <button onclick="logout()" class="btn btn-outline-light fw-bold btn-sm px-3 rounded"><i class="bi bi-box-arrow-right me-1"></i>Keluar</button>
                    </div>
                </div>
            </nav>
        `;
    } else {
        // Style Navbar Saat Logged Out (Ada Tombol Masuk & Daftar Menghadap Kanan)
        navbarEl.innerHTML = `
            <nav class="navbar navbar-expand-lg navbar-dark bg-primary shadow-sm mb-4 py-3" style="background-color: #0d6efd !important;">
                <div class="container">
                    <a class="navbar-brand fw-bold fs-4 text-white" href="#login">Smart City Portal</a>
                    <div class="d-flex gap-2 ms-auto">
                        <a href="#login" class="btn ${hash === '#login' ? 'btn-light text-primary' : 'btn-primary text-white border-light'} fw-bold btn-sm px-3 rounded">Masuk</a>
                        <a href="#register" class="btn ${hash === '#register' ? 'btn-light text-primary' : 'btn-primary text-white border-light'} fw-bold btn-sm px-3 rounded">Daftar</a>
                    </div>
                </div>
            </nav>
        `;
    }
}

function handleRouting() {
    const hash = window.location.hash || '#login';
    const contentDiv = document.getElementById('app-content');

    // Pengaman Akses Rute Token
    if (hash === '#dashboard' && !localStorage.getItem('access_token')) {
        window.location.hash = '#login';
        return;
    }
    if ((hash === '#login' || hash === '#register') && localStorage.getItem('access_token')) {
        window.location.hash = '#dashboard';
        return;
    }

    // Jalankan pembaruan struktur navbar
    updateGlobalNavbar(hash);

    // Tampilkan Konten Inti Halaman
    contentDiv.innerHTML = routes[hash] || routes['#login'];

    // Pemicu Setup Fungsi Halaman Aktif
    if (hash === '#login' && typeof setupLoginForm === 'function') {
        setupLoginForm();
    } else if (hash === '#register' && typeof setupRegisterForm === 'function') {
        setupRegisterForm();
    } else if (hash === '#dashboard' && typeof initDashboard === 'function') {
        initDashboard();
    }
}

window.addEventListener('hashchange', handleRouting);
window.addEventListener('DOMContentLoaded', handleRouting);