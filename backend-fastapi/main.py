from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
import json
import os

app = FastAPI(
    title="API Dashboard Toko Elektronik",
    description="Backend API untuk manajemen inventaris Toko Elektronik UTS WAD (Soal B)",
    version="1.0.0"
)

# CORS Middleware agar Vue lokal bisa akses
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_FILE = "data_produk.json"

# Skema Pydantic
class Produk(BaseModel):
    id: Optional[int] = None
    nama_produk: str = Field(..., description="Nama produk elektronik")
    kategori: str = Field(..., description="Kategori produk (misal: Smartphone, Laptop, Aksesoris)")
    stok: int = Field(..., ge=0, description="Jumlah stok (harus angka >= 0)")
    harga: int = Field(..., ge=0, description="Harga satuan produk dalam Rupiah")

class ProdukUpdate(BaseModel):
    nama_produk: Optional[str] = None
    kategori: Optional[str] = None
    stok: Optional[int] = Field(None, ge=0)
    harga: Optional[int] = Field(None, ge=0)

# Data Seed Awal (20 Produk Elektronik)
INITIAL_SEED = [
    {"id": 1, "nama_produk": "iPhone 15 Pro", "kategori": "Smartphone", "stok": 12, "harga": 18500000},
    {"id": 2, "nama_produk": "Samsung Galaxy S24", "kategori": "Smartphone", "stok": 8, "harga": 15000000},
    {"id": 3, "nama_produk": "MacBook Pro M3", "kategori": "Laptop", "stok": 5, "harga": 24000000},
    {"id": 4, "nama_produk": "Asus ROG Strix G16", "kategori": "Laptop", "stok": 2, "harga": 21000000},
    {"id": 5, "nama_produk": "Lenovo ThinkPad X1", "kategori": "Laptop", "stok": 0, "harga": 19000000},
    {"id": 6, "nama_produk": "Logitech MX Master 3S", "kategori": "Aksesoris", "stok": 25, "harga": 1500000},
    {"id": 7, "nama_produk": "Keychron K2 Mechanical", "kategori": "Aksesoris", "stok": 14, "harga": 1200000},
    {"id": 8, "nama_produk": "Sony WH-1000XM5", "kategori": "Audio", "stok": 6, "harga": 5200000},
    {"id": 9, "nama_produk": "AirPods Pro 2", "kategori": "Audio", "stok": 18, "harga": 3800000},
    {"id": 10, "nama_produk": "LG UltraWide Monitor 29", "kategori": "Monitor", "stok": 4, "harga": 3500000},
    {"id": 11, "nama_produk": "Dell 24 Monitor", "kategori": "Monitor", "stok": 10, "harga": 2100000},
    {"id": 12, "nama_produk": "Anker PowerBank 20000mAh", "kategori": "Aksesoris", "stok": 30, "harga": 650000},
    {"id": 13, "nama_produk": "SanDisk Extreme 1TB SSD", "kategori": "Penyimpanan", "stok": 7, "harga": 1800000},
    {"id": 14, "nama_produk": "Seagate External HDD 2TB", "kategori": "Penyimpanan", "stok": 9, "harga": 1100000},
    {"id": 15, "nama_produk": "iPad Air M2", "kategori": "Tablet", "stok": 3, "harga": 10500000},
    {"id": 16, "nama_produk": "Samsung Galaxy Tab S9", "kategori": "Tablet", "stok": 0, "harga": 12000000},
    {"id": 17, "nama_produk": "JBL Flip 6 Speaker", "kategori": "Audio", "stok": 15, "harga": 1700000},
    {"id": 18, "nama_produk": "Razer DeathAdder V3", "kategori": "Aksesoris", "stok": 11, "harga": 950000},
    {"id": 19, "nama_produk": "Xiaomi Smart Band 8", "kategori": "Wearable", "stok": 22, "harga": 550000},
    {"id": 20, "nama_produk": "Apple Watch Series 9", "kategori": "Wearable", "stok": 5, "harga": 6500000}
]

def load_data() -> List[dict]:
    if not os.path.exists(DATA_FILE):
        save_data(INITIAL_SEED)
        return INITIAL_SEED
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return INITIAL_SEED

def save_data(data: List[dict]):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

@app.get("/produk", summary="Ambil Semua Produk Elektronik", response_description="Daftar seluruh produk")
def get_produk():
    """Mengambil seluruh data produk elektronik."""
    return load_data()

@app.post("/produk", summary="Tambah Produk Elektronik Baru", response_description="Produk berhasil ditambahkan")
def create_produk(prod: Produk):
    """Menambahkan produk baru ke penyimpanan lokal dan menulis ulang JSON."""
    data = load_data()
    new_id = max([item["id"] for item in data], default=0) + 1
    new_item = {
        "id": new_id,
        "nama_produk": prod.nama_produk,
        "kategori": prod.kategori,
        "stok": prod.stok,
        "harga": prod.harga
    }
    data.append(new_item)
    save_data(data)
    return {"message": "Produk berhasil ditambahkan", "data": new_item}

@app.put("/produk/{produk_id}", summary="Update Produk Elektronik", response_description="Produk berhasil diperbarui")
def update_produk(produk_id: int, prod: ProdukUpdate):
    """Memperbarui data produk berdasarkan ID dan memperbarui JSON lokal."""
    data = load_data()
    for item in data:
        if item["id"] == produk_id:
            if prod.nama_produk is not None:
                item["nama_produk"] = prod.nama_produk
            if prod.kategori is not None:
                item["kategori"] = prod.kategori
            if prod.stok is not None:
                item["stok"] = prod.stok
            if prod.harga is not None:
                item["harga"] = prod.harga
            save_data(data)
            return {"message": "Produk berhasil diperbarui", "data": item}
    raise HTTPException(status_code=404, detail=f"Produk dengan ID {produk_id} tidak ditemukan")

@app.delete("/produk/{produk_id}", summary="Hapus Produk Elektronik", response_description="Produk berhasil dihapus")
def delete_produk(produk_id: int):
    """Menghapus produk berdasarkan ID dan memperbarui JSON lokal."""
    data = load_data()
    filtered_data = [item for item in data if item["id"] != produk_id]
    if len(filtered_data) == len(data):
        raise HTTPException(status_code=404, detail=f"Produk dengan ID {produk_id} tidak ditemukan")
    save_data(filtered_data)
    return {"message": f"Produk dengan ID {produk_id} berhasil dihapus"}