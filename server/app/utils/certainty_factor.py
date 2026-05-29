"""
Certainty Factor (CF) Expert System Engine
Sistem Deteksi Dini Tingkat Stres Karyawan - CC26-PSU196
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional

# ─────────────────────────────────────────
# KNOWLEDGE BASE (Basis Pengetahuan)
# ─────────────────────────────────────────

# CF nilai pakar per gejala per diagnosis
KNOWLEDGE_BASE: Dict[str, Dict[str, float]] = {
    # Beban dan Tekanan Kerja
    "G1":  {"D2": 1.0},
    "G2":  {"D2": 1.0, "D3": 1.0},
    "G3":  {"D2": 1.0, "D3": 1.0},
    "G4":  {"D2": 0.8, "D3": 0.8},
    "G5":  {"D2": 1.0},
    "G6":  {"D2": 0.8, "D3": 0.8},
    "G7":  {"D1": 0.4, "D2": 0.4},
    "G8":  {"D1": 0.8, "D2": 0.8},
    "G9":  {"D2": 0.8, "D3": 0.8},
    "G10": {"D2": 0.9},
    # Konflik Peran dan Penugasan
    "G11": {"D1": 0.5, "D2": 0.5},
    "G12": {"D2": 0.6, "D3": 0.6},
    "G13": {"D2": 0.8, "D3": 0.8},
    "G14": {"D2": 0.6, "D3": 0.6},
    "G15": {"D2": 0.8, "D3": 0.8},
    "G16": {"D2": 1.0, "D3": 1.0},
    "G17": {"D2": 1.0, "D3": 1.0},
    # Hubungan Interpersonal
    "G18": {"D1": 1.0},
    "G19": {"D1": 0.8, "D2": 0.8, "D3": 0.8},
    "G20": {"D2": 0.7, "D3": 0.7},
    "G21": {"D1": 0.8, "D2": 0.8, "D3": 0.8},
    "G22": {"D2": 0.8, "D3": 0.8},
    # Kejelasan Peran
    "G23": {"D2": 1.0},
    "G24": {"D1": 0.6, "D2": 0.6},
    "G25": {"D1": 0.5, "D2": 0.5, "D3": 0.5},
    "G26": {"D2": 1.0, "D3": 1.0},
    "G27": {"D1": 0.7, "D2": 0.7},
    "G28": {"D2": 0.8, "D3": 0.8},
    "G29": {"D2": 0.8},
    # Gaya Kepemimpinan
    "G30": {"D2": 0.4, "D3": 0.4, "D4": 0.4},
    "G31": {"D2": 0.7, "D3": 0.7},
    "G32": {"D2": 0.8, "D3": 0.8},
    "G33": {"D1": 0.9, "D2": 0.9, "D3": 0.9},
    "G34": {"D2": 0.6, "D3": 0.6},
    "G35": {"D2": 0.9, "D3": 0.9},
    "G36": {"D1": 0.8, "D2": 0.8, "D3": 0.8},
    # Pengembangan Karir
    "G37": {"D2": 0.9},
    "G38": {"D2": 1.0},
    "G39": {"D2": 0.4, "D4": 0.4},
    "G40": {"D1": 0.4, "D3": 0.4},
    "G41": {"D1": 0.6, "D2": 0.6},
    "G42": {"D2": 0.8, "D3": 0.8},
    "G43": {"D2": 0.4, "D4": 0.4},
}

# Mapping nilai jawaban user (uncertain terms)
USER_CF_MAP: Dict[str, float] = {
    "tidak_pernah":  0.0,
    "jarang":        0.25,
    "kadang_kadang": 0.5,
    "sering":        0.75,
    "selalu":        1.0,
}

DIAGNOSES = {
    "D1": "Tidak Stres",
    "D2": "Stres Ringan",
    "D3": "Stres Sedang",
    "D4": "Stres Berat",
}

NUMERIC_ANSWER_MAP = {
    0: "tidak_pernah",
    1: "jarang",
    2: "kadang_kadang",
    3: "sering",
    4: "selalu",
}


# ─────────────────────────────────────────
# CORE CF CALCULATION
# ─────────────────────────────────────────

def cf_single(cf_pakar: float, cf_user: float) -> float:
    """CF untuk satu gejala: CF_pakar × CF_user"""
    return cf_pakar * cf_user


def cf_combine(cf_old: float, cf_new: float) -> float:
    """Kombinasi dua CF menggunakan rumus CF kombinasi sequential."""
    if cf_old >= 0 and cf_new >= 0:
        return cf_old + cf_new * (1 - cf_old)
    elif cf_old < 0 and cf_new < 0:
        return cf_old + cf_new * (1 + cf_old)
    else:
        return (cf_old + cf_new) / (1 - min(abs(cf_old), abs(cf_new)))


def compute_cf_scores(symptom_answers: Dict[str, float]) -> Dict[str, float]:
    """
    Hitung CF score untuk setiap diagnosis.

    Args:
        symptom_answers: dict {gejala_code: cf_user_value}
                         e.g. {"G1": 0.75, "G2": 0.5, ...}
                         cf_user_value antara 0.0 s/d 1.0

    Returns:
        dict {diagnosis_code: cf_combined_score}
    """
    cf_scores: Dict[str, float] = {d: 0.0 for d in DIAGNOSES}

    for gejala_code, cf_user in symptom_answers.items():
        if gejala_code not in KNOWLEDGE_BASE:
            continue
        if cf_user == 0.0:
            continue  # "Tidak Pernah" tidak berkontribusi

        for diag_code, cf_pakar in KNOWLEDGE_BASE[gejala_code].items():
            cf_g = cf_single(cf_pakar, cf_user)
            cf_scores[diag_code] = cf_combine(cf_scores[diag_code], cf_g)

    return cf_scores


def get_diagnosis(cf_scores: Dict[str, float]) -> Dict:
    """
    Tentukan diagnosis berdasarkan CF score tertinggi.

    Returns:
        dict dengan hasil diagnosis lengkap
    """
    max_diag = max(cf_scores, key=cf_scores.get)
    max_score = cf_scores[max_diag]

    # Jika semua CF = 0, tidak ada gejala signifikan
    if max_score == 0.0:
        return {
            "diagnosis_code": "D1",
            "diagnosis_label": "Tidak Stres",
            "cf_score": 0.0,
            "cf_percentage": 0.0,
            "all_scores": cf_scores,
        }

    return {
        "diagnosis_code": max_diag,
        "diagnosis_label": DIAGNOSES[max_diag],
        "cf_score": round(max_score, 4),
        "cf_percentage": round(max_score * 100, 2),
        "all_scores": {k: round(v, 4) for k, v in cf_scores.items()},
    }


# ─────────────────────────────────────────
# HELPER: Convert questionnaire answers
# ─────────────────────────────────────────

def answers_from_text(raw_answers: Dict[str, str]) -> Dict[str, float]:
    """
    Convert jawaban teks ke nilai CF user.
    e.g. {"G1": "sering", "G2": "selalu"} → {"G1": 0.75, "G2": 1.0}
    """
    return {
        code: USER_CF_MAP.get(answer.lower().replace(" ", "_"), 0.0)
        for code, answer in raw_answers.items()
    }


def answers_from_numeric(raw_answers: Dict[str, int]) -> Dict[str, float]:
    """
    Convert jawaban numerik (0-4) ke nilai CF user.
    0=tidak pernah, 1=jarang, 2=kadang, 3=sering, 4=selalu
    """
    converted = {}
    for code, val in raw_answers.items():
        term = NUMERIC_ANSWER_MAP.get(val, "tidak_pernah")
        converted[code] = USER_CF_MAP[term]
    return converted


# ─────────────────────────────────────────
# FULL CF DIAGNOSIS FUNCTION
# ─────────────────────────────────────────

def diagnose(symptom_answers: Dict[str, float]) -> Dict:
    """
    Fungsi utama: jalankan CF diagnosis.

    Args:
        symptom_answers: {gejala_code: cf_user (0.0-1.0)}

    Returns:
        hasil diagnosis lengkap
    """
    cf_scores = compute_cf_scores(symptom_answers)
    return get_diagnosis(cf_scores)


# ─────────────────────────────────────────
# DEMO / TEST
# ─────────────────────────────────────────
if __name__ == "__main__":
    # Contoh: user menjawab beberapa gejala
    sample_answers = {
        "G1": 0.75,   # Sering: tugas terasa berlebihan
        "G2": 1.0,    # Selalu: tanggung jawab memberatkan
        "G3": 0.75,   # Sering: dikejar deadline
        "G6": 0.5,    # Kadang: kurang istirahat
        "G16": 0.75,  # Sering: tekanan dari atasan langsung
        "G19": 0.25,  # Jarang: konflik dengan rekan kerja
        "G30": 0.5,   # Kadang: micromanaging
        "G42": 0.5,   # Kadang: feedback tidak sesuai harapan
    }

    result = diagnose(sample_answers)
    print("=" * 50)
    print("HASIL DIAGNOSIS CF")
    print("=" * 50)
    print(f"Diagnosis : {result['diagnosis_label']} ({result['diagnosis_code']})")
    print(f"CF Score  : {result['cf_score']} ({result['cf_percentage']}%)")
    print("\nSemua CF Scores:")
    for code, score in result['all_scores'].items():
        label = DIAGNOSES[code]
        bar = "█" * int(score * 20)
        print(f"  {code} ({label:15s}): {score:.4f}  {bar}")
