# ⚡ Dashboard Toko Elektronik (Full-Stack Vue 3 + FastAPI)

Proyek ini adalah aplikasi web *Mini Dashboard Full-Stack* untuk manajemen inventaris Toko Elektronik (Soal B). Aplikasi ini dibangun dari nol menggunakan **Vue 3 (Composition API)** di sisi *frontend* dan **FastAPI (Python)** di sisi *backend*, dengan penyimpanan data lokal berformat JSON. Seluruh nilai harga menggunakan mata uang **Rupiah (IDR)**.

---

## 🛠️ Spesifikasi & Teknologi

* **Frontend:** Vue 3 (Composition API `<script setup>`), HTML5, CSS Grid/Flexbox Native.
* **Backend:** FastAPI (Python 3), Pydantic Schema, Uvicorn Server, CORS Middleware.
* **Penyimpanan Data:** File JSON lokal (`data_produk.json`) murni tanpa database eksternal.
* **Metode JavaScript Native:** Menggunakan ES6+ Array Methods (`.filter()`, `.sort()`, `.map()`, `.reduce()`) tanpa library eksternal.
* **Komunikasi API:** Fetch API berbasis `async/await` dengan penanganan status (*loading*, *error*, *empty*).

---

## 📊 Ambang Batas (Threshold) Status Stok

Sesuai ketentuan Soal B, status ketersediaan stok produk ditentukan berdasarkan kriteria kuantitas berikut:

| Status Stok | Ambang Batas Stok | Warna Badge | Keterangan |
| :--- | :--- | :--- | :--- |
| **Tersedia** | Stok >= 10 unit | Hijau (`#d1fae5`) | Stok melimpah dan dalam kondisi aman. |
| **Menipis** | 1 - 9 unit | Kuning (`#fef3c7`) | Stok mulai menipis dan perlu reorder. |
| **Stok Habis** | Stok = 0 unit | Merah (`#fee2e2`) | Stok barang kosong sepenuhnya. |

---

## 🚀 Cara Menjalankan Proyek

### 1. Persyaratan Sistem
* Python 3.9+
* Node.js v18+ dan npm

---

### 2. Menjalankan Backend (FastAPI)

1. Buka terminal dan masuk ke folder `backend-fastapi`:
   ```bash
   cd backend-fastapi

2. Buat dan aktifkan virtual environment:
   ```bash
   python3 -m venv venv
source venv/bin/activate  #Untuk macOS/Linux
#venv\Scripts\activate   #Untuk Windows

3. Install modul/dependensi yang dibutuhkan:
   ```bash
   pip install fastapi uvicorn pydantic

4. Jalankan server FastAPI dengan Uvicorn:
   ```bash
   uvicorn main:app --reload --host 127.0.0.1 --port 8000
   Server Backend akan berjalan di: http://127.0.0.1:8000
   Dokumentasi OpenAPI (Swagger UI): http://127.0.0.1:8000/docs

### 2. Menjalankan Frontend (Vue 3)

1. Buka jendela/tab terminal baru dan masuk ke folder dashboard-vue:
   ```bash
   cd dashboard-vue

2. Install dependensi Node.js:
   ```bash
   npm install

3. Jalankan server pengembangan Vue:
   ```bash
   npm run dev

4. Buka URL yang tertera di terminal (biasanya http://localhost:5173) melalui browser Anda.

Struktur Proyek

UTS_TokoElektronik/
├── backend-fastapi/
│   ├── main.py              # Application entrypoint & Endpoint REST API
│   ├── data_produk.json     # File penyimpanan JSON lokal (auto-generated)
│   └── venv/                # Virtual environment Python
├── dashboard-vue/
│   ├── src/
│   │   ├── App.vue          # Main Vue Component (Composition API)
│   │   └── main.js          # Vue App Mount
│   └── package.json
├── .gitignore               # Mengecualikan node_modules, venv, ds_store
└── README.md                # Dokumentasi petunjuk proyek

Fitur-Fitur Utama

1. 4 Tile Ringkasan Statistik: Menampilkan Total Jenis Produk, Total Stok Menipis + Habis, Jumlah Kategori Unik, dan Total Accumulation Unit Stok secara otomatis (computed).
2. Visualisasi CSS Bar: Menampilkan persentase distribusi stok tiap kategori menggunakan bar berbasis CSS Flexbox/Grid murni.
3. Pencarian & Pengurutan: Filter data berdasarkan nama produk/kategori serta pengurutan alfabet (A-Z / Z-A) secara reactive.
4. Operasi CRUD Lengkap:
GET : Mengambil daftar seluruh produk.
POST : Menambah produk baru ke backend.
PUT : Memperbarui/Edit data produk yang ada.
DELETE : Menghapus produk dari backend dan file JSON.
5. Responsif UI: Tampilan fleksibel untuk resolusi Desktop, Tablet, hingga Mobile (375px).