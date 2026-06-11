// Deklarasi URL utama dari Backend Django Rest Framework (DRF)
const BASE_URL = 'http://103.151.63.88:8004';

/**
 * Fungsi Pembungkus HTTP Request menggunakan Fetch API secara Global.
 * Otomatis menyertakan Bearer Token jika user sudah terautentikasi.
 */
async function requestAPI(endpoint, method = 'GET', bodyData = null) {
    const headers = {
        'Content-Type': 'application/json'
    };

    // Ambil access token dari localStorage browser
    const accessToken = localStorage.getItem('access_token');

    // Jika token ditemukan di memori, sisipkan ke komponen Header Authorization
    if (accessToken) {
        headers['Authorization'] = `Bearer ${accessToken}`;
    }

    const config = {
        method: method,
        headers: headers
    };

    // Masukkan payload body JSON jika metode HTTP berupa POST, PUT, atau PATCH
    if (bodyData && (method === 'POST' || method === 'PUT' || method === 'PATCH')) {
        config.body = JSON.stringify(bodyData);
    }

    try {
        const response = await fetch(`${BASE_URL}${endpoint}`, config);
        return response;
    } catch (error) {
        console.error('Terjadi Kegagalan Request API:', error);
        throw error;
    }
}