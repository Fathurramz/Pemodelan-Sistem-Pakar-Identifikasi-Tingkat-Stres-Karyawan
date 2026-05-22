"""
Expert System — Forward Chaining untuk Analisis Tingkat Stres Karyawan.

Logika:
1. Jawaban dikelompokkan per kategori (beban_kerja, lingkungan_kerja, kesehatan)
2. Skor rata-rata per kategori dihitung (skala 1-5 → dinormalisasi ke 0-100%)
3. Skor total = weighted average dari semua faktor
4. Rules forward chaining menentukan level stres
5. Rekomendasi otomatis berdasarkan level + faktor dominan

NOTE: Fungsi `predict_with_ml()` adalah placeholder.
      Ganti dengan model ML (.pkl/.h5) yang sebenarnya saat sudah siap.
"""


def analyze_stress(answers, questions):
    """
    Analisis tingkat stres berdasarkan jawaban kuesioner.

    Args:
        answers: dict {question_id: score (1-5)}
        questions: list of Question objects dari database

    Returns:
        dict: {score, stress_level, factors, recommendations}
    """

    # --- STEP 1: Kelompokkan jawaban per kategori ---
    category_scores = {
        "beban_kerja": [],
        "lingkungan_kerja": [],
        "kesehatan": [],
    }

    for question in questions:
        q_id = str(question.id)
        if q_id in answers:
            score = int(answers[q_id])
            category_scores[question.category].append(score)

    # --- STEP 2: Hitung rata-rata per kategori (normalisasi ke 0-100%) ---
    factors = []
    category_labels = {
        "beban_kerja": "Beban Kerja",
        "lingkungan_kerja": "Lingkungan Kerja",
        "kesehatan": "Kesehatan & Gaya Hidup",
    }
    category_colors = {
        "beban_kerja": "bg-red-500",
        "lingkungan_kerja": "bg-yellow-500",
        "kesehatan": "bg-green-500",
    }

    total_score = 0
    total_count = 0

    for category, scores in category_scores.items():
        if scores:
            avg = sum(scores) / len(scores)
            # Normalisasi: (avg - 1) / (5 - 1) * 100 → skala 1-5 ke 0-100%
            normalized = round(((avg - 1) / 4) * 100)
            factors.append(
                {
                    "label": category_labels[category],
                    "value": normalized,
                    "color": category_colors[category],
                }
            )
            total_score += sum(scores)
            total_count += len(scores)

    # --- STEP 3: Hitung skor total stres ---
    if total_count > 0:
        overall_avg = total_score / total_count
        overall_score = round(((overall_avg - 1) / 4) * 100)
    else:
        overall_score = 0

    # --- STEP 4: Forward Chaining Rules ---
    stress_level = _determine_stress_level(overall_score)

    # --- STEP 5: Generate rekomendasi ---
    recommendations = _generate_recommendations(stress_level, factors)

    # --- PLACEHOLDER ML: uncomment saat model sudah siap ---
    # ml_prediction = predict_with_ml(answers)
    # if ml_prediction:
    #     overall_score = ml_prediction["score"]
    #     stress_level = ml_prediction["level"]

    return {
        "score": overall_score,
        "stress_level": stress_level,
        "factors": factors,
        "recommendations": recommendations,
    }


def _determine_stress_level(score):
    """
    Forward Chaining Rules — menentukan level stres berdasarkan skor.

    Rules:
        R1: IF skor <= 30 THEN level = "Rendah"
        R2: IF skor > 30 AND skor <= 60 THEN level = "Sedang"
        R3: IF skor > 60 THEN level = "Tinggi"
    """
    if score <= 30:
        return "Rendah"
    elif score <= 60:
        return "Sedang"
    else:
        return "Tinggi"


def _generate_recommendations(stress_level, factors):
    """
    Generate rekomendasi berdasarkan level stres dan faktor dominan.
    """

    # Cari faktor dengan skor tertinggi
    dominant_factor = None
    if factors:
        dominant_factor = max(factors, key=lambda f: f["value"])

    recommendations = []

    # Rekomendasi berdasarkan level stres
    if stress_level == "Rendah":
        recommendations.append(
            "Tingkat stres Anda tergolong rendah. Pertahankan pola hidup sehat Anda!"
        )
        recommendations.append(
            "Tetap jaga keseimbangan antara pekerjaan dan kehidupan pribadi."
        )
        recommendations.append(
            "Lakukan aktivitas relaksasi ringan seperti jalan pagi atau meditasi."
        )

    elif stress_level == "Sedang":
        recommendations.append(
            "Ambil jeda istirahat 5-10 menit setiap 2 jam bekerja."
        )
        recommendations.append(
            "Coba teknik pernapasan kotak (box breathing) saat merasa cemas."
        )
        recommendations.append(
            "Komunikasikan beban kerja dengan atasan atau rekan tim."
        )

    elif stress_level == "Tinggi":
        recommendations.append(
            "Segera konsultasikan kondisi Anda dengan profesional kesehatan mental."
        )
        recommendations.append(
            "Kurangi beban kerja dan delegasikan tugas yang memungkinkan."
        )
        recommendations.append(
            "Prioritaskan tidur yang cukup (7-9 jam) dan pola makan teratur."
        )

    # Rekomendasi tambahan berdasarkan faktor dominan
    if dominant_factor:
        if dominant_factor["label"] == "Beban Kerja" and dominant_factor["value"] > 50:
            recommendations.append(
                "Faktor utama stres Anda adalah beban kerja. "
                "Coba buat daftar prioritas tugas harian dan fokus pada yang paling penting."
            )
        elif (
            dominant_factor["label"] == "Lingkungan Kerja"
            and dominant_factor["value"] > 50
        ):
            recommendations.append(
                "Lingkungan kerja menjadi pemicu utama. "
                "Cobalah untuk membangun komunikasi yang lebih terbuka dengan rekan kerja."
            )
        elif (
            dominant_factor["label"] == "Kesehatan & Gaya Hidup"
            and dominant_factor["value"] > 50
        ):
            recommendations.append(
                "Kesehatan dan gaya hidup perlu diperhatikan. "
                "Mulailah rutin berolahraga minimal 30 menit, 3 kali seminggu."
            )

    return recommendations


def predict_with_ml(answers):
    """
    PLACEHOLDER untuk prediksi menggunakan model Machine Learning.

    TODO: Ganti dengan implementasi model ML yang sebenarnya.

    Contoh implementasi nanti:
        import joblib
        model = joblib.load("model/stress_model.pkl")
        features = preprocess(answers)
        prediction = model.predict([features])
        return {"score": prediction[0], "level": map_level(prediction[0])}
    """
    return None
