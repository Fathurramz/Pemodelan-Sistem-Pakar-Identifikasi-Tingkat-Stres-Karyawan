import os
import joblib
import numpy as np

# Path to model directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(BASE_DIR, 'ml_model')

# Load model artifacts
stress_model = joblib.load(os.path.join(MODEL_DIR, 'stress_model.pkl'))
feature_names = joblib.load(os.path.join(MODEL_DIR, 'feature_names.pkl'))
label_names = joblib.load(os.path.join(MODEL_DIR, 'label_names.pkl'))

def predict_ml(data_dict):
    """
    Prediksi probabilitas stres menggunakan model Machine Learning.
    
    Args:
        data_dict: dict of ML features
        
    Returns:
        dict: hasil prediksi dengan probabilitas per kelas
    """
    # Pastikan data diurutkan berdasarkan feature_names
    row = np.array([[data_dict[f] for f in feature_names]])
    proba = stress_model.predict_proba(row)[0]
    idx = np.argmax(proba)
    
    return {
        "predicted_label": label_names[idx],
        "confidence": float(proba[idx]),
        "probabilities": dict(zip(label_names, proba.tolist()))
    }

def combine_cf_ml(cf_result, ml_result, cf_weight=0.7):
    """
    Kombinasi hasil diagnosis CF dan prediksi ML.
    
    Args:
        cf_result: output dari certainty_factor.py
        ml_result: output dari predict_ml()
        cf_weight: bobot CF (default 0.7)
        
    Returns:
        dict: diagnosis final
    """
    cf_scores = cf_result['all_scores']
    
    # 1. Hitung ulang kontribusi per kategori untuk memperoleh index klinis objektif
    # (Ini digunakan untuk mengoreksi bias matematis D2/D3 pada CF Knowledge Base bawaan)
    category_questions = {
        "Beban Kerja": ["G1", "G2", "G3"],
        "Konflik Peran": ["G16"],
        "Interpersonal": ["G18"],
        "Kejelasan Peran": ["G23", "G26"],
        "Kepemimpinan": ["G33"],
        "Karir": ["G37", "G38"]
    }
    
    # Map raw_answers yang tersimpan atau hitung dari cf_result
    # Kita asumsikan input gejala terpetakan dalam cf_result['all_scores']
    # Tapi yang paling presisi adalah mengambil nilai CF user dari cf_result['all_scores']
    # Wait, certainty_factor.py didiagnose menerima symptom_answers. 
    # Mari kita ekstrak cf_answers dari cf_result atau hitung rata-rata secara langsung
    # Untuk mendapatkan input gejala klinis, kita bisa melakukan ekstraksi secara dinamis.
    # Karena cf_result['all_scores'] berisi hasil diagnosis, mari kita hitung kontribusi dari cf_scores.
    # Namun, alternatif terbaik yang sangat stabil adalah:
    # Menggunakan jumlah skor kasar Certainty Factor untuk mengkalibrasi tingkat keparahan (D1-D4)
    # Jika total CF score adalah 0.0 -> D1 (Tidak Stres)
    # Jika total CF score adalah maksimal -> D4 (Stres Berat)
    
    # Hitung rata-rata kontribusi gejala klinis (dari all_scores D1-D4 atau data gejala)
    # Karena basis pengetahuan pakar memiliki bias numerik di mana D2 dan D3 bernilai 1.0 
    # sedangkan D4 bernilai maksimal 0.4 di knowledge base asli, D4 tidak akan pernah menang secara alami.
    # Kita lakukan normalisasi terkalibrasi:
    cf_sum = sum(cf_scores.values())
    
    # Jika tidak ada gejala klinis sama sekali (CF sum = 0.0) -> Mutlak Tidak Stres (D1)
    if cf_sum == 0.0:
        return {
            "final_diagnosis": "Tidak Stres",
            "final_code": "D1",
            "final_score": 0.0,
            "score_breakdown": {
                "Tidak Stres": 1.0,
                "Stres Ringan": 0.0,
                "Stres Sedang": 0.0,
                "Stres Berat": 0.0
            }
        }
        
    # Skala index klinis dari 0.0 s/d 1.0 berdasarkan skor CF maksimal yang diraih
    max_cf_possible = 3.9  # Jumlah CF maksimal teoritis dari 10 soal aktif
    clinical_stress_index = min(cf_sum / max_cf_possible, 1.0)
    
    # Interpolasi kontinu untuk mengonstruksi cf_vec tanpa bias numerik D2/D3
    if clinical_stress_index <= 0.20:
        # Transisi dari D1 (Tidak Stres) ke D2 (Stres Ringan)
        p2 = clinical_stress_index / 0.20
        p1 = 1.0 - p2
        cf_vec = np.array([p1, p2, 0.0, 0.0])
    elif clinical_stress_index <= 0.55:
        # Transisi dari D2 (Stres Ringan) ke D3 (Stres Sedang)
        p3 = (clinical_stress_index - 0.20) / (0.55 - 0.20)
        p2 = 1.0 - p3
        cf_vec = np.array([0.0, p2, p3, 0.0])
    else:
        # Transisi dari D3 (Stres Sedang) ke D4 (Stres Berat)
        p4 = (clinical_stress_index - 0.55) / (1.0 - 0.55)
        p3 = 1.0 - p4
        cf_vec = np.array([0.0, 0.0, p3, p4])
        
    ml_weight = 1.0 - cf_weight
    
    # ML model memiliki 5 kelas (termasuk Stres Sangat Berat)
    # CF model memiliki 4 kelas D1-D4
    # Gabungkan 'Stres Berat' dan 'Stres Sangat Berat' milik ML menjadi kelas ke-4
    proba_list = [
        ml_result['probabilities'].get('Tidak Stres', 0.0),
        ml_result['probabilities'].get('Stres Ringan', 0.0),
        ml_result['probabilities'].get('Stres Sedang', 0.0),
        ml_result['probabilities'].get('Stres Berat', 0.0) + ml_result['probabilities'].get('Stres Sangat Berat', 0.0)
    ]
    ml_vec4 = np.array(proba_list)
    
    # Normalisasi vector agar jumlahnya = 1.0
    cf_norm = cf_vec / cf_vec.sum() if cf_vec.sum() > 0 else cf_vec
    ml_norm = ml_vec4 / ml_vec4.sum() if ml_vec4.sum() > 0 else ml_vec4
    
    # Kombinasi berbobot
    combined = cf_weight * cf_norm + ml_weight * ml_norm
    labels4 = ['Tidak Stres', 'Stres Ringan', 'Stres Sedang', 'Stres Berat']
    final_idx = int(np.argmax(combined))
    
    return {
        "final_diagnosis": labels4[final_idx],
        "final_code": f"D{final_idx+1}",
        "final_score": round(float(combined[final_idx]), 4),
        "score_breakdown": dict(zip(labels4, combined.round(4).tolist()))
    }



REKOMENDASI = {
    "D1": {
        "warna": "🟢",
        "summary": "Kondisi baik. Pertahankan keseimbangan kerja dan kehidupan.",
        "tips": [
            "Pertahankan kebiasaan tidur yang cukup dan olahraga teratur.",
            "Jaga hubungan sosial dan komunikasi positif dengan rekan kerja.",
            "Sempatkan waktu luang untuk hobi dan refreshing di luar jam kerja."
        ]
    },
    "D2": {
        "warna": "🟡",
        "summary": "Stres ringan. Perlu beberapa penyesuaian kecil.",
        "tips": [
            "Coba terapkan teknik manajemen waktu seperti Pomodoro.",
            "Pastikan tidur malam cukup minimal 7-8 jam per hari.",
            "Lakukan olahraga ringan 15-30 menit setiap hari.",
            "Ambil jeda istirahat singkat di sela-sela waktu kerja."
        ]
    },
    "D3": {
        "warna": "🟠",
        "summary": "Stres sedang. Perlu tindakan penyesuaian beban kerja.",
        "tips": [
            "Komunikasikan beban kerja dan deadline kepada atasan atau manajer.",
            "Praktikkan latihan pernapasan (box breathing) atau meditasi saat merasa cemas.",
            "Batasi lembur dan usahakan tidak membawa pekerjaan ke rumah.",
            "Pertimbangkan untuk bercerita ke rekan dekat atau berkonsultasi dengan konselor."
        ]
    },
    "D4": {
        "warna": "🔴",
        "summary": "Stres berat. Segera ambil langkah penanganan medis/profesional.",
        "tips": [
            "Sangat disarankan berkonsultasi dengan psikolog atau dokter profesional.",
            "Ajukan cuti kerja atau kurangi beban kerja Anda untuk memulihkan diri.",
            "Hindari mengambil tanggung jawab baru dalam waktu dekat.",
            "Jangan ragu untuk mencari dukungan dari keluarga dekat dan rekan kerja."
        ]
    }
}
