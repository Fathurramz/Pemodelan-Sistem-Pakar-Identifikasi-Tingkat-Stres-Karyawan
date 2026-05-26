"""
Seed script — Isi database dengan 20 pertanyaan kuesioner tingkat stres karyawan.
10 Pertanyaan Gejala Certainty Factor (CF) dan 10 Pertanyaan Aktivitas/Kondisi Machine Learning (ML).

Jalankan: python -m app.seed
"""

from app import create_app, db
from app.models import Question

SEED_QUESTIONS = [
    # === CERTAINTY FACTOR (10 Gejala Pilihan) ===
    {
        "code": "G1",
        "text": "Tugas yang diberikan perusahaan terasa berlebihan",
        "category": "Beban dan Tekanan Kerja",
        "order_number": 1,
    },
    {
        "code": "G2",
        "text": "Tanggung jawab yang diberikan perusahaan sangat memberatkan saya",
        "category": "Beban dan Tekanan Kerja",
        "order_number": 2,
    },
    {
        "code": "G3",
        "text": "Saya sering dikejar waktu (deadline) dalam menyelesaikan pekerjaan",
        "category": "Beban dan Tekanan Kerja",
        "order_number": 3,
    },
    {
        "code": "G16",
        "text": "Saya merasakan tekanan dari tugas yang dibebankan atasan langsung",
        "category": "Konflik Peran dan Penugasan",
        "order_number": 4,
    },
    {
        "code": "G18",
        "text": "Hubungan saya dengan rekan kerja terasa tidak harmonis atau kurang baik",
        "category": "Hubungan Interpersonal di Tempat Kerja",
        "order_number": 5,
    },
    {
        "code": "G23",
        "text": "Saya merasa kurang jelas dengan informasi dari perusahaan mengenai pekerjaan saya",
        "category": "Kejelasan Peran dan Informasi Kerja",
        "order_number": 6,
    },
    {
        "code": "G26",
        "text": "Saya sulit memperoleh informasi yang dibutuhkan untuk menjalankan pekerjaan",
        "category": "Kejelasan Peran dan Informasi Kerja",
        "order_number": 7,
    },
    {
        "code": "G33",
        "text": "Saya merasa tidak punya peranan dalam pengambilan keputusan di tempat kerja",
        "category": "Gaya Kepemimpinan dan Penilaian Kinerja",
        "order_number": 8,
    },
    {
        "code": "G37",
        "text": "Saya merasa peluang untuk mendapat promosi di perusahaan ini sangat kecil",
        "category": "Pengembangan Karir dan Kepuasan Kerja",
        "order_number": 9,
    },
    {
        "code": "G38",
        "text": "Saya mendapat pekerjaan baru yang memerlukan keterampilan berbeda dari sebelumnya tanpa pelatihan",
        "category": "Pengembangan Karir dan Kepuasan Kerja",
        "order_number": 10,
    },
    # === MACHINE LEARNING (10 Fitur Aktivitas/Kondisi) ===
    {
        "code": "A1",
        "text": "Berapa rata-rata jam kerja Anda per hari?",
        "category": "Data Umum dan Kondisi Kerja",
        "order_number": 11,
    },
    {
        "code": "A2",
        "text": "Di mana Anda biasanya bekerja?",
        "category": "Data Umum dan Kondisi Kerja",
        "order_number": 12,
    },
    {
        "code": "A3",
        "text": "Apakah Anda tinggal bersama keluarga?",
        "category": "Data Umum dan Kondisi Kerja",
        "order_number": 13,
    },
    {
        "code": "A4",
        "text": "Seberapa sosial Anda di lingkungan kerja? (bergaul dan berinteraksi)",
        "category": "Data Umum dan Kondisi Kerja",
        "order_number": 14,
    },
    {
        "code": "A5",
        "text": "Apakah Anda merasa keseimbangan antara pekerjaan dan kehidupan pribadi Anda terjaga?",
        "category": "Data Umum dan Kondisi Kerja",
        "order_number": 15,
    },
    {
        "code": "ML1",
        "text": "Bagaimana kebiasaan tidur Anda akhir-akhir ini?",
        "category": "Kesehatan dan Gaya Hidup",
        "order_number": 16,
    },
    {
        "code": "ML2",
        "text": "Seberapa rutin Anda melakukan aktivitas fisik atau olahraga?",
        "category": "Kesehatan dan Gaya Hidup",
        "order_number": 17,
    },
    {
        "code": "ML3",
        "text": "Seberapa besar tekanan pekerjaan yang Anda rasakan secara keseluruhan?",
        "category": "Kesehatan dan Gaya Hidup",
        "order_number": 18,
    },
    {
        "code": "ML4",
        "text": "Seberapa besar dukungan yang Anda rasakan dari atasan/manajer Anda?",
        "category": "Kesehatan dan Gaya Hidup",
        "order_number": 19,
    },
    {
        "code": "ML5",
        "text": "Seberapa puas Anda dengan pekerjaan yang Anda jalani saat ini?",
        "category": "Kesehatan dan Gaya Hidup",
        "order_number": 20,
    },
]


def seed_questions():
    """Insert pertanyaan ke database. Hapus data lama agar sinkron."""
    # Hapus semua pertanyaan yang ada
    print("[SEED] Mengosongkan data pertanyaan lama...")
    Question.query.delete()
    db.session.commit()

    print("[SEED] Menambahkan pertanyaan baru...")
    for q in SEED_QUESTIONS:
        question = Question(
            code=q["code"],
            text=q["text"],
            category=q["category"],
            order_number=q["order_number"],
        )
        db.session.add(question)

    db.session.commit()
    print(f"[SEED] Berhasil menambahkan {len(SEED_QUESTIONS)} pertanyaan kuesioner!")


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        seed_questions()
