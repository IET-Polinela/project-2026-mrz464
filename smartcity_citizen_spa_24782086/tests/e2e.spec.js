const { test, expect } = require('@playwright/test');

const BASE_URL = 'http://localhost:8000';
const SPA_URL = 'http://localhost:5500/index.html';

const TEST_ADMIN_USERNAME  = 'admin';
const TEST_ADMIN_PASSWORD  = 'admin';

const EXPIRED_ACCESS_TOKEN  = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjAwMDAwMDAwLCJpYXQiOjE2MDAwMDAwMDAsImp0aSI6ImZha2VfYWNjZXNzX2lkIiwidXNlcl9pZCI6MX0.fake_signature_for_testing';
const EXPIRED_REFRESH_TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYwMDAwMDAwMCwiaWF0IjoxNjAwMDAwMDAwLCJqdGkiOiJmYWtlX3JlZnJlc2hfaWQiLCJ1c2VyX2lkIjoxfQ.fake_signature_for_testing';
const VALID_ACCESS_TOKEN    = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjo5OTk5OTk5OTk5LCJpYXQiOjE2MDAwMDAwMDAsImp0aSI6InZhbGlkX2FjY2Vzc19pZCIsInVzZXJfaWQiOjF9.fake_valid_signature';

async function loginSPA(page, username, password) {
    await page.goto(`${SPA_URL}#login`);
    await page.waitForSelector('#loginForm', { state: 'visible', timeout: 10000 });
    await page.locator('#loginUsername').fill(username);
    await page.locator('#loginPassword').fill(password);
    await page.locator('#loginForm button[type="submit"]').click();
}

async function loginAdmin(page, username, password) {
    await page.goto(`${BASE_URL}/login/`);
    await page.waitForSelector('form', { state: 'visible', timeout: 10000 });
    await page.locator('input[name="username"]').fill(username);
    await page.locator('input[name="password"]').fill(password);
    await Promise.all([
        page.waitForNavigation({ waitUntil: 'networkidle', timeout: 15000 }),
        page.locator('button[type="submit"]').click()
    ]);
}

async function setupAuthTokens(page, accessToken, refreshToken, username = 'testwarga') {
    await page.evaluate(
        ({ access, refresh, user }) => {
            localStorage.setItem('access_token', access);
            localStorage.setItem('refresh_token', refresh);
            localStorage.setItem('username', user);
        },
        { access: accessToken, refresh: refreshToken, user: username }
    );
}

async function clearAuthTokens(page) {
    await page.evaluate(() => {
        localStorage.clear();
    });
}

async function mockSPAApiUrl(page) {
    await page.route('**/api/**', async (route) => {
        const originalUrl = route.request().url();
        if (originalUrl.startsWith(BASE_URL)) {
            return route.continue();
        }
        const urlObj = new URL(originalUrl);
        const newUrl = `${BASE_URL}${urlObj.pathname}${urlObj.search}`;
        await route.continue({ url: newUrl });
    });
}

test.describe('Modul 1: Otorisasi & Sesi (AUTH-04, AUTH-05, AUTH-06)', () => {
    test.beforeEach(async ({ page }) => {
        await page.goto(SPA_URL);
        await clearAuthTokens(page);
        await mockSPAApiUrl(page);
    });

    test('AUTH-04: Akses #dashboard tanpa token → redirect ke #login', async ({ page }) => {
        const tokenBefore = await page.evaluate(() => localStorage.getItem('access_token'));
        expect(tokenBefore).toBeNull();
        await page.goto(`${SPA_URL}#dashboard`);
        await page.waitForFunction(() => window.location.hash === '#login', null, { timeout: 5000 });
        await expect(page).toHaveURL(/#login/);
        await expect(page.locator('#loginForm')).toBeVisible({ timeout: 5000 });
    });

    test('AUTH-05: Token kadaluarsa → interceptor menangani 401 dan redirect ke #login', async ({ page }) => {
        await setupAuthTokens(page, EXPIRED_ACCESS_TOKEN, EXPIRED_REFRESH_TOKEN);
        await page.unroute('**/api/**');
        await page.route('**/api/**', async (route) => {
            await route.fulfill({
                status: 401,
                contentType: 'application/json',
                body: JSON.stringify({ detail: 'Given token not valid', code: 'token_not_valid' })
            });
        });
        page.on('dialog', async (dialog) => await dialog.accept());
        await page.goto(`${SPA_URL}#dashboard`);
        await page.waitForTimeout(2000);
        await page.waitForFunction(() => window.location.hash === '#login', null, { timeout: 10000 });
        await expect(page).toHaveURL(/#login/);
        const tokenAfter = await page.evaluate(() => localStorage.getItem('access_token'));
        expect(tokenAfter).toBeNull();
    });

    test('AUTH-06: Kedua token kadaluarsa → localStorage dibersihkan, redirect ke #login', async ({ page }) => {
        await setupAuthTokens(page, EXPIRED_ACCESS_TOKEN, EXPIRED_REFRESH_TOKEN);
        await page.unroute('**/api/**');
        await page.route('**/api/**', async (route) => {
            await route.fulfill({
                status: 401,
                contentType: 'application/json',
                body: JSON.stringify({ detail: 'Token is invalid', code: 'token_not_valid' })
            });
        });
        page.on('dialog', async (dialog) => await dialog.accept());
        await page.goto(`${SPA_URL}#dashboard`);
        await page.waitForTimeout(2000);
        await page.waitForFunction(() => window.location.hash === '#login', null, { timeout: 10000 });
        await expect(page).toHaveURL(/#login/);
        const accessAfter = await page.evaluate(() => localStorage.getItem('access_token'));
        expect(accessAfter).toBeNull();
    });
});

test.describe('Modul 5: Interaktivitas UI (UI-01 through UI-06)', () => {
    test('UI-01: Chart.js di Dashboard Admin ter-render dengan benar', async ({ page }) => {
        await loginAdmin(page, TEST_ADMIN_USERNAME, TEST_ADMIN_PASSWORD);
        await page.goto(`${BASE_URL}/dashboard/`);
        await page.waitForLoadState('networkidle');
        
        await expect(page.locator('#statusChart')).toBeVisible({ timeout: 15000 });
        await expect(page.locator('#categoryChart')).toBeVisible({ timeout: 15000 });

        const chartsRendered = await page.evaluate(() => {
            if (typeof Chart === 'undefined') return false;
            return Object.keys(Chart.instances || {}).length >= 2;
        });
        expect(chartsRendered).toBe(true);
        await expect(page.locator('#reportedTable')).toBeVisible();
    });

    test('UI-02: Live Search pada daftar laporan admin berfungsi', async ({ page }) => {
        await loginAdmin(page, TEST_ADMIN_USERNAME, TEST_ADMIN_PASSWORD);
        await page.goto(`${BASE_URL}/laporan/`);
        await page.waitForLoadState('networkidle');
        
        const searchInput = page.locator('#searchInput');
        const tableBody = page.locator('#searchResults');
        await expect(searchInput).toBeVisible({ timeout: 10000 });
        
        const searchKeyword = 'Lampu';
        const responsePromise = page.waitForResponse(
            (response) => response.url().includes(`/dashboard/api/search/?q=${searchKeyword}`) && response.status() === 200,
            { timeout: 15000 }
        );
        await searchInput.click();
        await searchInput.fill('');
        await searchInput.type(searchKeyword, { delay: 100 });
        
        const searchResponse = await responsePromise;
        expect(searchResponse.status()).toBe(200);
        await page.waitForTimeout(1000);
    });

    test('UI-03: Pagination Feed Kota — maks 10 kartu', async ({ page }) => {
        await page.goto(SPA_URL);
        await mockSPAApiUrl(page);
        
        const mockReports = Array.from({ length: 25 }, (_, i) => ({
            id: i + 1, title: `Laporan #${i+1}`, category: 'Infrastruktur', location: 'Loc', status: 'REPORTED'
        }));
        
        await page.route('**/api/reports/**', async (route) => {
            const pageNum = parseInt((route.request().url().match(/page=(\d+)/) || [0, 1])[1]);
            const startIdx = (pageNum - 1) * 10;
            await route.fulfill({
                status: 200,
                contentType: 'application/json',
                body: JSON.stringify({
                    count: 25,
                    results: mockReports.slice(startIdx, startIdx + 10)
                })
            });
        });
        
        await setupAuthTokens(page, VALID_ACCESS_TOKEN, EXPIRED_REFRESH_TOKEN);
        page.on('dialog', async (dialog) => await dialog.accept());
        await page.goto(`${SPA_URL}#dashboard`);
        await page.waitForSelector('button[data-bs-target="#reportModal"]', { state: 'visible', timeout: 10000 });
        
        await page.locator('#tabFeed').click();
        await page.waitForTimeout(2000);
        
        const cardCount = await page.locator('#listContainer .col').count();
        expect(cardCount).toBeLessThanOrEqual(10);
        
        const paginationCount = await page.locator('#paginationContainer .page-item').count();
        expect(paginationCount).toBeGreaterThanOrEqual(3);
    });

    test('UI-04: Klik tombol Buat Laporan → modal #reportModal muncul', async ({ page }) => {
        await page.goto(SPA_URL);
        await setupAuthTokens(page, VALID_ACCESS_TOKEN, EXPIRED_REFRESH_TOKEN);
        await mockSPAApiUrl(page);
        
        await page.route('**/api/**', async (route) => {
            await route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ count: 0, results: [] }) });
        });
        
        await page.goto(`${SPA_URL}#dashboard`);
        await page.waitForSelector('button[data-bs-target="#reportModal"]', { state: 'visible', timeout: 10000 });
        await page.locator('button[data-bs-target="#reportModal"]').click();
        
        await page.waitForTimeout(500);
        await expect(page.locator('#reportModal')).toHaveClass(/show/);
        await expect(page.locator('#reportModal')).toBeVisible();
    });

    test('UI-05: Mengisi form aduan baru dan menyimpan sebagai draf', async ({ page }) => {
        await page.goto(SPA_URL);
        await setupAuthTokens(page, VALID_ACCESS_TOKEN, EXPIRED_REFRESH_TOKEN);
        await mockSPAApiUrl(page);
        
        await page.route('**/api/**', async (route) => {
            await route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ count: 0, results: [] }) });
        });
        
        await page.route('**/api/reports/', async (route) => {
            if (route.request().method() === 'POST') {
                await route.fulfill({ status: 201, contentType: 'application/json', body: JSON.stringify({ id: 99, status: 'DRAFT' }) });
            }
        });
        
        await page.goto(`${SPA_URL}#dashboard`);
        await page.waitForSelector('button[data-bs-target="#reportModal"]', { state: 'visible', timeout: 10000 });
        await page.locator('button[data-bs-target="#reportModal"]').click();
        
        await page.locator('#reportTitle').fill('Jalan Rusak');
        await page.locator('#reportDescription').fill('Ada lubang besar');
        await page.locator('#reportCategory').selectOption('Infrastruktur');
        await page.locator('#reportLocation').fill('Jalan Mawar');
        
        page.on('dialog', async (dialog) => await dialog.accept());
        await page.locator('#btnDraft').click();
        
        await page.waitForTimeout(1000);
        await expect(page.locator('#reportModal')).not.toHaveClass(/show/);
    });

    test('UI-06: Merubah ukuran viewport ke mobile (400x800) → tombol hamburger', async ({ page }) => {
        await page.goto(SPA_URL);
        await setupAuthTokens(page, VALID_ACCESS_TOKEN, EXPIRED_REFRESH_TOKEN);
        await mockSPAApiUrl(page);
        await page.goto(`${SPA_URL}#dashboard`);
        
        await page.setViewportSize({ width: 400, height: 800 });
        await page.waitForTimeout(1000);
        
        const toggler = page.locator('.navbar-toggler').first();
        await expect(toggler).toBeVisible();
        const navbarNav = page.locator('#navbarNav').first();
        await expect(navbarNav).not.toBeVisible();
    });
});
