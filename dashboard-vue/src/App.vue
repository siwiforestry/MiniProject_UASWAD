<script setup>
import { ref, computed, onMounted } from 'vue'

// API Base URL
const API_URL = 'http://127.0.0.1:8000/produk'

// State Data dari Backend (ref)
const produkList = ref([])
const isLoading = ref(false)
const isError = ref(false)
const errorMessage = ref('')

// State Pencarian dan Pengurutan
const searchQuery = ref('')
const sortOrder = ref('asc') // 'asc' atau 'desc'

// State Form (Tambah & Edit)
const formProduct = ref({
  id: null,
  nama_produk: '',
  kategori: '',
  stok: 0,
  harga: 0
})
const isEditing = ref(false)

// 1. Konsumsi API: Get Produk
const fetchProduk = async () => {
  isLoading.value = true
  isError.value = false
  try {
    const res = await fetch(API_URL)
    if (!res.ok) throw new Error('Gagal mengambil data dari server')
    const data = await res.json()
    produkList.value = data
  } catch (err) {
    isError.value = true
    errorMessage.value = err.message || 'Terjadi kesalahan saat terhubung ke backend.'
  } finally {
    isLoading.value = false
  }
}

// 2. Computed Filter & Sort Berantai (ES6 Native)
const filteredAndSortedProduk = computed(() => {
  // Filter pencarian berdasarkan nama_produk atau kategori
  const query = searchQuery.value.toLowerCase().trim()
  let result = produkList.value.filter(item => 
    item.nama_produk.toLowerCase().includes(query) ||
    item.kategori.toLowerCase().includes(query)
  )

  // Pengurutan A-Z / Z-A berdasarkan nama_produk
  return result.sort((a, b) => {
    if (sortOrder.value === 'asc') {
      return a.nama_produk.localeCompare(b.nama_produk)
    } else {
      return b.nama_produk.localeCompare(a.nama_produk)
    }
  })
})

// 3. Computed 4 Tile Statistik (Native ES6 Array Methods)
const totalProduk = computed(() => produkList.value.length)

const totalStokMenipisDanHabis = computed(() => {
  return produkList.value.filter(item => item.stok < 10).length
})

const jumlahKategoriUnik = computed(() => {
  const kategoriArray = produkList.value.map(item => item.kategori)
  return new Set(kategoriArray).size
})

const totalUnitStok = computed(() => {
  return produkList.value.reduce((total, item) => total + Number(item.stok), 0)
})

// Visualisasi CSS Bar Stok per Kategori
const stokPerKategori = computed(() => {
  const mapKategori = {}
  produkList.value.forEach(item => {
    mapKategori[item.kategori] = (mapKategori[item.kategori] || 0) + item.stok
  })
  
  const total = totalUnitStok.value || 1
  return Object.keys(mapKategori).map(kat => ({
    kategori: kat,
    stok: mapKategori[kat],
    persentase: Math.round((mapKategori[kat] / total) * 100)
  }))
})

// Helper Function: Badge Class Status Stok
const getStatusBadge = (stok) => {
  if (stok >= 10) return { text: 'Tersedia', class: 'badge-aman' }
  if (stok > 0) return { text: 'Menipis', class: 'badge-menipis' }
  return { text: 'Stok Habis', class: 'badge-habis' }
}

// Format Rupiah
const formatRupiah = (angka) => {
  return new Intl.NumberFormat('id-ID', { style: 'currency', currency: 'IDR', maximumFractionDigits: 0 }).format(angka)
}

// 4. Form Submission (Tambah / Edit)
const handleSubmit = async () => {
  if (!formProduct.value.nama_produk || !formProduct.value.kategori) {
    alert('Nama produk dan kategori wajib diisi!')
    return
  }

  try {
    if (isEditing.value) {
      // PUT: Update Data
      const res = await fetch(`${API_URL}/${formProduct.value.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          nama_produk: formProduct.value.nama_produk,
          kategori: formProduct.value.kategori,
          stok: Number(formProduct.value.stok),
          harga: Number(formProduct.value.harga)
        })
      })
      if (!res.ok) throw new Error('Gagal memperbarui produk')
    } else {
      // POST: Tambah Data Baru
      const res = await fetch(API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          nama_produk: formProduct.value.nama_produk,
          kategori: formProduct.value.kategori,
          stok: Number(formProduct.value.stok),
          harga: Number(formProduct.value.harga)
        })
      })
      if (!res.ok) throw new Error('Gagal menambah produk baru')
    }

    resetForm()
    await fetchProduk()
  } catch (err) {
    alert(err.message)
  }
}

// Set Data untuk Edit
const handleEdit = (item) => {
  isEditing.value = true
  formProduct.value = { ...item }
}

// Reset Form State
const resetForm = () => {
  isEditing.value = false
  formProduct.value = { id: null, nama_produk: '', kategori: '', stok: 0, harga: 0 }
}

// 5. DELETE Produk
const handleDelete = async (id) => {
  if (!confirm('Apakah Anda yakin ingin menghapus produk ini?')) return

  try {
    const res = await fetch(`${API_URL}/${id}`, { method: 'DELETE' })
    if (!res.ok) throw new Error('Gagal menghapus produk')
    await fetchProduk()
  } catch (err) {
    alert(err.message)
  }
}

onMounted(() => {
  fetchProduk()
})
</script>

<template>
  <div class="dashboard-container">
    <!-- Header -->
    <header class="header">
      <h1>⚡ Dashboard Toko Elektronik</h1>
      <p>Sistem Manajemen Inventaris Full-Stack (Vue 3 + FastAPI)</p>
    </header>

    <!-- 4 Tile Statistik Ringkasan -->
    <section class="stats-grid">
      <div class="stat-card">
        <h3>Total Jenis Produk</h3>
        <p class="stat-value">{{ totalProduk }}</p>
      </div>
      <div class="stat-card warning">
        <h3>Stok Menipis + Habis</h3>
        <p class="stat-value">{{ totalStokMenipisDanHabis }}</p>
      </div>
      <div class="stat-card">
        <h3>Jumlah Kategori</h3>
        <p class="stat-value">{{ jumlahKategoriUnik }}</p>
      </div>
      <div class="stat-card">
        <h3>Total Unit Stok</h3>
        <p class="stat-value">{{ totalUnitStok }}</p>
      </div>
    </section>

    <!-- Visualisasi CSS Bar Stok per Kategori -->
    <section class="category-visualization">
      <h3>📊 Distribusi Stok per Kategori</h3>
      <div class="bars-container">
        <div v-for="cat in stokPerKategori" :key="cat.kategori" class="bar-item">
          <div class="bar-info">
            <span>{{ cat.kategori }}</span>
            <span>{{ cat.stok }} Unit ({{ cat.persentase }}%)</span>
          </div>
          <div class="bar-bg">
            <div class="bar-fill" :style="{ width: cat.persentase + '%' }"></div>
          </div>
        </div>
      </div>
    </section>

    <!-- Form Tambah / Edit Data -->
    <section class="form-card">
      <h3>{{ isEditing ? '✏️ Edit Produk Elektronik' : '➕ Tambah Produk Elektronik Baru' }}</h3>
      <form @submit.prevent="handleSubmit" class="form-grid">
        <div class="form-group">
          <label>Nama Produk</label>
          <input v-model="formProduct.nama_produk" type="text" placeholder="Contoh: Laptop Asus ROG" required />
        </div>
        <div class="form-group">
          <label>Kategori</label>
          <input v-model="formProduct.kategori" type="text" placeholder="Contoh: Laptop, Smartphone" required />
        </div>
        <div class="form-group">
          <label>Jumlah Stok</label>
          <input v-model.number="formProduct.stok" type="number" min="0" required />
        </div>
        <div class="form-group">
          <label>Harga (IDR)</label>
          <input v-model.number="formProduct.harga" type="number" min="0" step="1000" required />
        </div>
        <div class="form-actions">
          <button type="submit" class="btn-primary">
            {{ isEditing ? 'Simpan Perubahan' : 'Tambah Produk' }}
          </button>
          <button v-if="isEditing" type="button" @click="resetForm" class="btn-secondary">
            Batal
          </button>
        </div>
      </form>
    </section>

    <!-- Toolbar: Search & Sort -->
    <section class="toolbar">
      <div class="search-box">
        <input 
          v-model="searchQuery" 
          type="text" 
          placeholder="🔍 Cari nama produk atau kategori..." 
        />
      </div>
      <div class="sort-box">
        <label>Urutkan Nama: </label>
        <button @click="sortOrder = sortOrder === 'asc' ? 'desc' : 'asc'" class="btn-sort">
          {{ sortOrder === 'asc' ? 'A-Z ⬇️' : 'Z-A ⬆️' }}
        </button>
      </div>
    </section>

    <!-- State UI: Loading & Error -->
    <div v-if="isLoading" class="state-msg info">⏳ Memuat data produk elektronik...</div>
    <div v-else-if="isError" class="state-msg error">❌ Error: {{ errorMessage }}</div>

    <!-- Tabel Produk -->
    <section v-else class="table-wrapper">
      <table v-if="filteredAndSortedProduk.length > 0" class="data-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Nama Produk</th>
            <th>Kategori</th>
            <th>Harga</th>
            <th>Stok</th>
            <th>Status</th>
            <th>Aksi</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in filteredAndSortedProduk" :key="item.id">
            <td>#{{ item.id }}</td>
            <td class="font-bold">{{ item.nama_produk }}</td>
            <td><span class="category-tag">{{ item.kategori }}</span></td>
            <td>{{ formatRupiah(item.harga) }}</td>
            <td>{{ item.stok }} unit</td>
            <td>
              <span :class="['badge', getStatusBadge(item.stok).class]">
                {{ getStatusBadge(item.stok).text }}
              </span>
            </td>
            <td>
              <div class="action-btns">
                <button @click="handleEdit(item)" class="btn-edit">Edit</button>
                <button @click="handleDelete(item.id)" class="btn-delete">Hapus</button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- State UI: Data Kosong -->
      <div v-else class="state-msg empty">
        📭 Tidak ada produk yang sesuai dengan kata kunci pencarian.
      </div>
    </section>
  </div>
</template>

<style scoped>
/* Styling Dasar & CSS Grid Responsif */
.dashboard-container {
  max-width: 1100px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  color: #2c3e50;
}

.header {
  text-align: center;
  margin-bottom: 25px;
}
.header h1 {
  margin: 0;
  color: #1a252f;
}
.header p {
  color: #7f8c8d;
  margin-top: 5px;
}

/* 4 Tile Ringkasan */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 15px;
  margin-bottom: 25px;
}
.stat-card {
  background: #f8f9fa;
  border-left: 5px solid #3498db;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}
.stat-card.warning {
  border-left-color: #e67e22;
}
.stat-card h3 {
  font-size: 0.85rem;
  color: #7f8c8d;
  margin: 0 0 5px 0;
  text-transform: uppercase;
}
.stat-value {
  font-size: 1.8rem;
  font-weight: bold;
  margin: 0;
  color: #2c3e50;
}

/* CSS Bar Visualisasi */
.category-visualization {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 15px 20px;
  margin-bottom: 25px;
}
.category-visualization h3 {
  margin-top: 0;
  font-size: 1rem;
}
.bars-container {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.bar-info {
  display: flex;
  justify-content: space-between;
  font-size: 0.85rem;
  margin-bottom: 3px;
}
.bar-bg {
  background: #edf2f7;
  height: 10px;
  border-radius: 5px;
  overflow: hidden;
}
.bar-fill {
  background: #3498db;
  height: 100%;
  border-radius: 5px;
  transition: width 0.3s ease;
}

/* Card Form */
.form-card {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 25px;
}
.form-card h3 {
  margin-top: 0;
  margin-bottom: 15px;
}
.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 15px;
}
.form-group {
  display: flex;
  flex-direction: column;
}
.form-group label {
  font-size: 0.85rem;
  margin-bottom: 5px;
  font-weight: 600;
}
.form-group input {
  padding: 8px 12px;
  border: 1px solid #cbd5e1;
  border-radius: 5px;
}
.form-actions {
  grid-column: span 2;
  display: flex;
  gap: 10px;
}

/* Toolbar Search & Sort */
.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 15px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}
.search-box {
  flex: 1;
  min-width: 250px;
}
.search-box input {
  width: 100%;
  padding: 10px 14px;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
  box-sizing: border-box;
}
.btn-sort {
  padding: 8px 16px;
  background: #2c3e50;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

/* Tabel Styling */
.table-wrapper {
  overflow-x: auto;
}
.data-table {
  width: 100%;
  border-collapse: collapse;
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}
.data-table th, .data-table td {
  padding: 12px 15px;
  text-align: left;
  border-bottom: 1px solid #e2e8f0;
}
.data-table th {
  background: #f1f5f9;
  font-weight: 600;
}
.font-bold {
  font-weight: 600;
}
.category-tag {
  background: #e2e8f0;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.8rem;
}

/* Conditional Badges */
.badge {
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: bold;
}
.badge-aman {
  background: #d1fae5;
  color: #065f46;
}
.badge-menipis {
  background: #fef3c7;
  color: #92400e;
}
.badge-habis {
  background: #fee2e2;
  color: #991b1b;
}

/* Tombol Aksi */
.action-btns {
  display: flex;
  gap: 6px;
}
.btn-primary {
  background: #2563eb;
  color: white;
  border: none;
  padding: 9px 18px;
  border-radius: 5px;
  cursor: pointer;
}
.btn-secondary {
  background: #64748b;
  color: white;
  border: none;
  padding: 9px 18px;
  border-radius: 5px;
  cursor: pointer;
}
.btn-edit {
  background: #f59e0b;
  color: white;
  border: none;
  padding: 5px 10px;
  border-radius: 4px;
  cursor: pointer;
}
.btn-delete {
  background: #ef4444;
  color: white;
  border: none;
  padding: 5px 10px;
  border-radius: 4px;
  cursor: pointer;
}

/* State Messages */
.state-msg {
  padding: 15px;
  border-radius: 6px;
  text-align: center;
  margin: 15px 0;
}
.state-msg.info { background: #e0f2fe; color: #0369a1; }
.state-msg.error { background: #fee2e2; color: #b91c1c; }
.state-msg.empty { background: #f3f4f6; color: #4b5563; }

/* Breakpoints Media Queries untuk Responsivitas UI */
@media (max-width: 1023px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 767px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
  .form-grid {
    grid-template-columns: 1fr;
  }
  .form-actions {
    grid-column: span 1;
  }
  .toolbar {
    flex-direction: column;
    align-items: stretch;
  }
}
</style>