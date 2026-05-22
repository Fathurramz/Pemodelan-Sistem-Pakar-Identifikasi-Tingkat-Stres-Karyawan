"""
Seed script — Isi database dengan 15 pertanyaan kuesioner stres karyawan.

Jalankan: python -m app.seed
"""

from app import create_app, db
from app.models import Question


SEED_QUESTIONS = [
    # === BEBAN KERJA (5 soal) ===
    {
        "text": "Seberapa sering Anda merasa kewalahan dengan jumlah tugas yang harus diselesaikan?",
        "category": "beban_kerja",
        "order_number": 1,
    },
    {
        "text": "Apakah deadline pekerjaan Anda terasa terlalu menekan?",
        "category": "beban_kerja",
        "order_number": 2,
    },
    {
        "text": "Seberapa sering Anda harus bekerja lembur atau membawa pekerjaan ke rumah?",
        "category": "beban_kerja",
        "order_number": 3,
    },
    {
        "text": "Apakah Anda merasa tanggung jawab pekerjaan melebihi kemampuan Anda?",
        "category": "beban_kerja",
        "order_number": 4,
    },
    {
        "text": "Seberapa sering Anda merasa tidak punya cukup waktu untuk menyelesaikan pekerjaan?",
        "category": "beban_kerja",
        "order_number": 5,
    },
    # === LINGKUNGAN KERJA (5 soal) ===
    {
        "text": "Apakah Anda merasa hubungan dengan rekan kerja kurang harmonis?",
        "category": "lingkungan_kerja",
        "order_number": 6,
    },
    {
        "text": "Seberapa sering Anda merasa tidak dihargai atau tidak diakui di tempat kerja?",
        "category": "lingkungan_kerja",
        "order_number": 7,
    },
    {
        "text": "Apakah komunikasi dengan atasan Anda terasa sulit atau menekan?",
        "category": "lingkungan_kerja",
        "order_number": 8,
    },
    {
        "text": "Seberapa sering terjadi konflik atau ketegangan di lingkungan kerja Anda?",
        "category": "lingkungan_kerja",
        "order_number": 9,
    },
    {
        "text": "Apakah Anda merasa tidak memiliki kendali atas keputusan yang memengaruhi pekerjaan Anda?",
        "category": "lingkungan_kerja",
        "order_number": 10,
    },
    # === KESEHATAN & GAYA HIDUP (5 soal) ===
    {
        "text": "Seberapa sering Anda mengalami kesulitan tidur atau insomnia karena memikirkan pekerjaan?",
        "category": "kesehatan",
        "order_number": 11,
    },
    {
        "text": "Apakah Anda sering merasa kelelahan fisik meskipun tidak melakukan aktivitas berat?",
        "category": "kesehatan",
        "order_number": 12,
    },
    {
        "text": "Seberapa sering Anda melewatkan waktu makan atau makan tidak teratur karena pekerjaan?",
        "category": "kesehatan",
        "order_number": 13,
    },
    {
        "text": "Apakah Anda merasa sulit berkonsentrasi atau mudah lupa akhir-akhir ini?",
        "category": "kesehatan",
        "order_number": 14,
    },
    {
        "text": "Seberapa sering Anda merasa cemas atau khawatir berlebihan di luar jam kerja?",
        "category": "kesehatan",
        "order_number": 15,
    },
]


def seed_questions():
    """Insert pertanyaan ke database jika belum ada."""
    existing_count = Question.query.count()

    if existing_count > 0:
        print(f"[SEED] Database sudah memiliki {existing_count} pertanyaan. Skip seed.")
        return

    for q in SEED_QUESTIONS:
        question = Question(
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
