# Link Demo : https://sistem-pakar-stres-seven.vercel.app/

# 🧠 Sistem Pakar & Machine Learning: Pendeteksi Tingkat Stres Karyawan

**Proyek Capstone Tim CC26-PSU196 | Coding Camp 2026 powered by DBS Foundation**

Repositori ini berisi implementasi sistem deteksi dini tingkat stres karyawan berbasis **Hybrid AI**: penggabungan metode **Certainty Factor (Expert System)** sebagai komponen utama (bobot 70%) dan **Machine Learning (Random Forest Classifier)** sebagai komponen pendukung (bobot 30%).

Sistem telah disesuaikan menjadi **20 pertanyaan kuesioner** agar efisien untuk diisi pengguna namun tetap mendapatkan seluruh input aktivitas yang dibutuhkan oleh model inferensi Machine Learning.

---

## 🌟 Fitur Unggulan

1. **Hybrid AI Engine**: Penggabungan sequential Certainty Factor (`certainty_factor.py`) dan model Random Forest Classifier (`stress_model.pkl`) menghasilkan diagnosis yang lebih objektif dan kontekstual.
2. **Defensive Database Fallback**: Server Flask secara otomatis mendeteksi ketersediaan server MySQL lokal pada port 3306. Jika MySQL tidak aktif/ditemukan, server akan otomatis beralih menggunakan **SQLite local database** (`server/stress_detection.db`) sehingga aplikasi siap ditesting secara instan.
3. **Interactive Questionnaire Wizard**: Form kuesioner interaktif di frontend yang dinamis, membagi 20 pertanyaan menjadi 2 bagian:
   - *Bagian 1*: 10 Gejala Stres (menggunakan frekuensi: *Tidak Pernah* s.d. *Selalu*).
   - *Bagian 2*: 10 Aktivitas Harian (menggunakan slider numerik jam kerja, seleksi biner/opsi lokasi, dan skala 1-5 kebiasaan).
4. **Faktor Pemicu Stres**: Dashboard menampilkan analisis visual persentase untuk 6 kategori pemicu stres (Beban Kerja, Konflik Peran, Interpersonal, Kejelasan Informasi, Gaya Kepemimpinan, dan Karir).
5. **Rekomendasi Langkah Awal**: Tips penanganan stres terpersonalisasi yang dirumuskan langsung oleh pakar berdasarkan level stres final.

---

## 📂 Struktur Proyek

- `/client` : React Frontend (Vite)
  - `/src/pages/Assessment.jsx` : Halaman kuesioner dinamis (mengambil pertanyaan dari API dan mengirimkan jawaban hybrid).
  - `/src/pages/Dashboard.jsx` : Visualisasi analisis tingkat stres, faktor pemicu, dan rekomendasi pakar.
- `/server` : Flask Backend (Python)
  - `/app/ml_model/` : Menyimpan model Random Forest terlatih (`stress_model.pkl`, `feature_names.pkl`, `label_names.pkl`).
  - `/app/utils/certainty_factor.py` : Engine Certainty Factor.
  - `/app/utils/ml_stress.py` : Logika prediksi ML & kombinasi bobot sequential hybrid.
  - `/app/routes/assessments.py` : Endpoint untuk memproses submit jawaban, normalisasi CF/ML, dan perhitungan pemicu stres.
- `/AI Model Capstone Project DBS` : File original riset, dataset, dan notebook Jupyter dari tim AI.

---

## 🚀 Cara Menjalankan Aplikasi

### 1. Backend - Flask Server

1. Masuk ke folder server:

   ```bash
   cd server
   ```
2. Pastikan virtual environment aktif (jika ada) dan install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

   *(Mengunduh library Flask, PyMySQL, Cryptography, scikit-learn, joblib, pandas, dan numpy).*
3. Jalankan server lokal:

   ```bash
   python run.py
   ```

   *Secara otomatis database akan dimigrasi dan di-seed dengan 20 pertanyaan baru.*

### 2. Frontend - React client

1. Masuk ke folder client:
   ```bash
   cd ../client
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Jalankan server lokal:
   ```bash
   npm run dev
   ```
4. Buka tautan **[http://localhost:5173](http://localhost:5173)** pada browser Anda untuk mencoba langsung.

---

## 👥 Kontributor (CC26-PSU196)

- **Ahmad Reyhan Maghribi** (Fullstack Developer)
- **Fathur Ramantha** (Fullstack Developer)
- **Elan Nurhaliza** (AI Engineer)
- **Muhammad Khafidz Miftakhurrohman** (AI Engineer)
- **Putri Handayani** (Data Scientist)
- **Stephen Lionel Halim** (Data Scientist)
