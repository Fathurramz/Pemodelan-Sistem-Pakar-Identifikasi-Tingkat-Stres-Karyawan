"""
Entry point — Jalankan server Flask.

Cara menjalankan:
    python run.py
"""

from app import create_app
from app.seed import seed_questions

app = create_app()

# Auto-seed pertanyaan saat pertama kali server jalan
with app.app_context():
    seed_questions()

if __name__ == "__main__":
    import os

    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "1") == "1"

    print("")
    print("=" * 56)
    print("  Sistem Pakar Identifikasi Tingkat Stres Karyawan")
    print("=" * 56)
    print(f"  Server berjalan di: http://localhost:{port}")
    print("")
    print("  API Endpoints:")
    print("    POST /api/auth/register  -> Daftar user")
    print("    POST /api/auth/login     -> Login")
    print("    GET  /api/questions      -> Pertanyaan kuesioner")
    print("    POST /api/assessments    -> Submit jawaban")
    print("    GET  /api/stress-result  -> Hasil analisis")
    print("=" * 56)
    print("")

    app.run(host="0.0.0.0", port=port, debug=debug)
