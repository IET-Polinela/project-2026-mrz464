let currentTab = 'my_reports';
let currentPage = 1;

function initDashboard() {
    loadDashboardData();
    setupModalActions();
}

function switchTab(tab) {
    currentTab = tab;
    currentPage = 1;

    if (tab === 'my_reports') {
        document.getElementById('tabMyReports').className = 'nav-link active fw-bold';
        document.getElementById('tabFeed').className = 'nav-link fw-bold text-muted';
    } else {
        document.getElementById('tabMyReports').className = 'nav-link fw-bold text-muted';
        document.getElementById('tabFeed').className = 'nav-link active fw-bold';
    }

    loadDashboardData();
}

function goToPage(pageNumber) {
    currentPage = pageNumber;
    loadDashboardData();
}

function setupRegisterForm() {
    const regForm = document.getElementById('registerForm');
    if (!regForm) return;

    regForm.onsubmit = async (e) => {
        e.preventDefault();

        const username = document.getElementById('regUsername').value;
        const email = document.getElementById('regEmail').value;
        const password = document.getElementById('regPassword').value;

        if (password.length < 8) {
            alert('Password terlalu pendek geh! Minimal harus 8 karakter.');
            return;
        }

        try {
            const response = await fetch('http://103.151.63.88:8004/api/register/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ username, email, password })
            });

            if (response.status === 201 || response.status === 200) {
                alert('Selamat Rez, Akun Warga Baru Berhasil Terdaftar! Silakan login.');
                window.location.hash = '#login';
            } else {
                const errData = await response.json();
                alert('Pendaftaran Gagal: ' + (errData.username || errData.email || 'Data tidak valid!'));
            }
        } catch (error) {
            alert('Gangguan koneksi ke server backend.');
        }
    };
}

// ====================================================================
// PERBAIKAN UTAMA: FILTER BERBASIS KEPEMILIKAN DARI BACKEND JWT (is_owner)
// ====================================================================
async function loadDashboardData() {
    const listContainer = document.getElementById('reportList');
    listContainer.className = "d-flex flex-column gap-3";
    listContainer.innerHTML = `<div class="text-center py-5 w-100"><div class="spinner-border text-primary"></div><p class="mt-2 text-muted">Memuat data dari server...</p></div>`;

    try {
        const response = await requestAPI(`/api/reports/?page=${currentPage}`);

        if (response.status === 200) {
            const data = await response.json();

            console.log("ISI DATA SATU LAPORAN:", data.results[0]);

            let rawReports = data.results;
            let filteredReports = [];

            if (currentTab === 'my_reports') {
                // AMAN: Menyaring laporan milik user aktif secara dinamis berdasarkan data token JWT Backend
                filteredReports = rawReports.filter(report => report.is_owner === true);
            } else if (currentTab === 'feed') {
                // Feed Kota hanya menampilkan laporan yang sudah resmi diajukan publik (Bukan Draf)
                filteredReports = rawReports.filter(report => {
                    let st = report.status ? report.status.toUpperCase() : '';
                    return st !== 'DRAFT' && st !== 'DRAF';
                });
            }

            renderReports(filteredReports);
            updateSidebarSummary(filteredReports);
            updatePaginationUI(data.count, data.next, data.previous);

        } else if (response.status === 401) {
            alert('Sesi login kamu sudah habis nih, Rez. Yuk login ulang dulu!');
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            window.location.hash = '#login';
            return;
        } else {
            listContainer.innerHTML = `<div class="alert alert-danger shadow-sm w-100">Gagal memuat data laporan dari server.</div>`;
        }
    } catch (error) {
        listContainer.innerHTML = `<div class="alert alert-danger shadow-sm w-100">Terjadi kesalahan koneksi internet atau server mati.</div>`;
    }
}

function updatePaginationUI(totalCount, hasNext, hasPrev) {
    const container = document.getElementById('paginationContainer');
    if (!container) return;

    const pageSize = 10;
    const totalPages = Math.ceil(totalCount / pageSize) || 1;

    let paginationHtml = `
        <nav aria-label="Navigasi Halaman Portal">
            <ul class="pagination shadow-sm mb-0">
                <li class="page-item ${!hasPrev ? 'disabled' : ''}">
                    <button class="page-link fw-semibold px-3" onclick="goToPage(${currentPage - 1})" ${!hasPrev ? 'disabled' : ''}>Sebelumnya</button>
                </li>
    `;

    let maxVisiblePages = 5;
    let startPage = Math.max(1, currentPage - Math.floor(maxVisiblePages / 2));
    let endPage = Math.min(totalPages, startPage + maxVisiblePages - 1);

    if (endPage - startPage + 1 < maxVisiblePages) {
        startPage = Math.max(1, endPage - maxVisiblePages + 1);
    }

    for (let i = startPage; i <= endPage; i++) {
        paginationHtml += `
            <li class="page-item ${i === currentPage ? 'active' : ''}">
                <button class="page-link fw-bold px-3" onclick="goToPage(${i})">${i}</button>
            </li>
        `;
    }

    paginationHtml += `
                <li class="page-item ${!hasNext ? 'disabled' : ''}">
                    <button class="page-link fw-semibold px-3" onclick="goToPage(${currentPage + 1})" ${!hasNext ? 'disabled' : ''}>Selanjutnya</button>
                </li>
            </ul>
        </nav>
    `;

    container.innerHTML = paginationHtml;
}

function updateSidebarSummary(results) {
    let draft = 0, reported = 0, progress = 0, resolved = 0;

    results.forEach(r => {
        let currentStatus = r.status ? r.status.toUpperCase() : '';
        if (currentStatus === 'DRAFT' || currentStatus === 'DRAF') draft++;
        if (currentStatus === 'REPORTED' || currentStatus === 'DIAJUKAN' || currentStatus === 'VERIFIED') reported++;
        if (currentStatus === 'IN_PROGRESS' || currentStatus === 'IN PROGRESS' || currentStatus === 'PROGRESS' || currentStatus === 'DIPROSES') progress++;
        if (currentStatus === 'RESOLVED' || currentStatus === 'SELESAI') resolved++;
    });

    if (document.getElementById('countDraft')) document.getElementById('countDraft').innerText = draft;
    if (document.getElementById('countReported')) document.getElementById('countReported').innerText = reported;
    if (document.getElementById('countProgress')) document.getElementById('countProgress').innerText = progress;
    if (document.getElementById('countResolved')) document.getElementById('countResolved').innerText = resolved;
}

function renderReports(reports) {
    const listContainer = document.getElementById('reportList');
    listContainer.innerHTML = '';
    listContainer.className = "row g-3 row-cols-1 row-cols-md-2";

    if (reports.length === 0) {
        listContainer.innerHTML = `
            <div class="col-12 text-center py-5 bg-white rounded shadow-sm border">
                <i class="bi bi-inbox fs-1 text-muted"></i>
                <p class="mt-3 text-muted mb-0">Belum ada data laporan di tab ini.</p>
            </div>`;
        return;
    }

    reports.forEach(report => {
        let progressHtml = '';
        let badgeHtml = '';
        let currentStatus = report.status ? report.status.toUpperCase() : '';
        let categoryText = report.category ? report.category.charAt(0).toUpperCase() + report.category.slice(1).toLowerCase() : 'Fasilitas Umum';

        if (currentStatus === 'DRAFT' || currentStatus === 'DRAF') {
            badgeHtml = `<span class="badge bg-secondary text-white px-2 py-1 fs-6 fw-bold rounded">DRAFT</span>`;
            progressHtml = `
                <div class="d-flex justify-content-between align-items-center mb-1 mt-2">
                    <span class="text-muted small" style="font-size: 0.85rem;">Progress Laporan:</span>
                    <span class="text-secondary small fw-bold" style="font-size: 0.85rem;">Draf (10%)</span>
                </div>
                <div class="progress" style="height: 6px;">
                    <div class="progress-bar bg-secondary" style="width: 10%"></div>
                </div>`;
        } else if (currentStatus === 'REPORTED' || currentStatus === 'DIAJUKAN') {
            badgeHtml = `<span class="badge bg-warning text-dark px-2 py-1 fs-6 fw-bold rounded">REPORTED</span>`;
            progressHtml = `
                <div class="d-flex justify-content-between align-items-center mb-1 mt-2">
                    <span class="text-muted small" style="font-size: 0.85rem;">Progress Laporan:</span>
                    <span class="text-warning small fw-bold" style="font-size: 0.85rem;">Diajukan (25%)</span>
                </div>
                <div class="progress" style="height: 6px;">
                    <div class="progress-bar bg-warning" style="width: 25%"></div>
                </div>`;
        } else if (currentStatus === 'VERIFIED') {
            badgeHtml = `<span class="badge bg-info text-white px-2 py-1 fs-6 fw-bold rounded" style="background-color: #0dcaf0 !important;">VERIFIED</span>`;
            progressHtml = `
                <div class="d-flex justify-content-between align-items-center mb-1 mt-2">
                    <span class="text-muted small" style="font-size: 0.85rem;">Progress Laporan:</span>
                    <span class="text-info small fw-bold" style="font-size: 0.85rem; color: #0dcaf0 !important;">Diverifikasi (50%)</span>
                </div>
                <div class="progress" style="height: 6px;">
                    <div class="progress-bar bg-info" style="width: 50%"></div>
                </div>`;
        } else if (currentStatus === 'IN_PROGRESS' || currentStatus === 'IN PROGRESS' || currentStatus === 'PROGRESS' || currentStatus === 'DIPROSES') {
            badgeHtml = `<span class="badge bg-primary text-white px-2 py-1 fs-6 fw-bold rounded" style="background-color: #0d6efd !important;">IN_PROGRESS</span>`;
            progressHtml = `
                <div class="d-flex justify-content-between align-items-center mb-1 mt-2">
                    <span class="text-muted small" style="font-size: 0.85rem;">Progress Laporan:</span>
                    <span class="text-primary small fw-bold" style="font-size: 0.85rem; color: #0d6efd !important;">Diproses (75%)</span>
                </div>
                <div class="progress" style="height: 6px;">
                    <div class="progress-bar bg-primary progress-bar-striped progress-bar-animated" style="width: 75%"></div>
                </div>`;
        } else if (currentStatus === 'RESOLVED' || currentStatus === 'SELESAI') {
            badgeHtml = `<span class="badge bg-success text-white px-2 py-1 fs-6 fw-bold rounded">RESOLVED</span>`;
            progressHtml = `
                <div class="d-flex justify-content-between align-items-center mb-1 mt-2">
                    <span class="text-muted small" style="font-size: 0.85rem;">Progress Laporan:</span>
                    <span class="text-success small fw-bold" style="font-size: 0.85rem;">Selesai (100%)</span>
                </div>
                <div class="progress" style="height: 6px;">
                    <div class="progress-bar bg-success" style="width: 100%"></div>
                </div>`;
        }

        let actionButtons = '';
        if (report.is_owner && (currentStatus === 'DRAFT' || currentStatus === 'DRAF')) {
            actionButtons = `
                <button class="btn btn-sm btn-outline-primary mt-3 fw-bold px-3 w-100" onclick="editReport(${report.id})">
                    <i class="bi bi-pencil-square me-1"></i> Edit Laporan
                </button>`;
        }

        const cardHtml = `
            <div class="col">
                <div class="card border-0 shadow-sm h-100 bg-white rounded-3">
                    <div class="card-body p-4 d-flex flex-column justify-content-between">
                        <div>
                            <div class="d-flex justify-content-between align-items-center mb-3">
                                ${badgeHtml}
                                <span class="text-muted small fw-semibold" style="font-size: 0.8rem;">${categoryText}</span>
                            </div>
                            <h4 class="fw-bold text-dark mb-2" style="font-size: 1.35rem; font-family: sans-serif;">${report.title}</h4>
                            <p class="text-muted mb-3" style="font-size: 0.95rem; line-height: 1.4;">${report.description}</p>
                            <hr class="text-muted opacity-25 my-3">
                            <p class="mb-4 text-secondary" style="font-size: 0.9rem; line-height: 1.6;">
                                <strong>Lokasi:</strong> ${report.location}<br>
                                <strong>Oleh:</strong> ${report.reporter}
                            </p>
                        </div>
                        <div>
                            ${progressHtml}
                            ${actionButtons}
                        </div>
                    </div>
                </div>
            </div>`;

        listContainer.insertAdjacentHTML('beforeend', cardHtml);
    });
}

function resetForm() {
    document.getElementById('reportId').value = '';
    document.getElementById('reportTitle').value = '';
    document.getElementById('reportCategory').value = 'INFRASTRUKTUR';
    document.getElementById('reportDescription').value = '';
    document.getElementById('reportLocation').value = '';
}

function logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    window.location.hash = '#login';
}

async function editReport(id) {
    try {
        const response = await requestAPI(`/api/reports/${id}/`);
        if (response.status === 200) {
            const data = await response.json();

            document.getElementById('reportId').value = data.id;
            document.getElementById('reportTitle').value = data.title;
            document.getElementById('reportCategory').value = data.category;
            document.getElementById('reportDescription').value = data.description;
            document.getElementById('reportLocation').value = data.location;

            const modal = new bootstrap.Modal(document.getElementById('reportModal'));
            modal.show();
        }
    } catch (error) {
        alert('Gagal mengambil data laporan dari server.');
    }
}

function setupModalActions() {
    const btnDraft = document.getElementById('btnDraft');
    const btnSubmit = document.getElementById('btnSubmit');

    const saveReport = async (targetStatus) => {
        const reportId = document.getElementById('reportId').value;

        const payload = {
            title: document.getElementById('reportTitle').value,
            category: document.getElementById('reportCategory').value.toUpperCase(),
            description: document.getElementById('reportDescription').value,
            location: document.getElementById('reportLocation').value,
            status: targetStatus.toUpperCase()
        };

        if (!payload.title || !payload.description || !payload.location) {
            alert('Harap isi Judul, Deskripsi, dan Lokasi dengan lengkap!');
            return;
        }

        const method = reportId ? 'PATCH' : 'POST';
        const endpoint = reportId ? `/api/reports/${reportId}/` : '/api/reports/';

        try {
            const response = await requestAPI(endpoint, method, payload);
            if (response.status === 200 || response.status === 201) {
                alert('Laporan sukses disimpan ke server!');

                const modalEl = document.getElementById('reportModal');
                const modalInstance = bootstrap.Modal.getInstance(modalEl) || new bootstrap.Modal(modalEl);
                modalInstance.hide();

                loadDashboardData();
            } else {
                const rawErrorText = await response.text();
                alert(`Django Menolak!\nStatus: ${response.status}\nPesan Validasi: ${rawErrorText}`);
            }
        } catch (error) {
            alert('Gangguan koneksi internet atau server mati.');
        }
    };

    if (btnDraft) btnDraft.onclick = () => saveReport('DRAFT');
    if (btnSubmit) btnSubmit.onclick = () => saveReport('REPORTED');
}