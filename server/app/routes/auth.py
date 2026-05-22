from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
import bcrypt
from app import db
from app.models import User

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    """
    Register user baru.

    Body JSON:
        {
            "name": "Ahmad Reyhan",
            "email": "reyhan@example.com",
            "password": "password123"
        }

    Returns:
        201: User berhasil didaftarkan + JWT token
        400: Validasi gagal
        409: Email sudah terdaftar
    """
    data = request.get_json()

    # Validasi input
    if not data:
        return jsonify({"error": "Request body tidak boleh kosong"}), 400

    name = data.get("name", "").strip()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not name or not email or not password:
        return jsonify({"error": "Nama, email, dan password wajib diisi"}), 400

    if len(password) < 6:
        return jsonify({"error": "Password minimal 6 karakter"}), 400

    # Cek apakah email sudah terdaftar
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"error": "Email sudah terdaftar"}), 409

    # Hash password
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    # Simpan user baru
    new_user = User(
        name=name,
        email=email,
        password=hashed_password.decode("utf-8"),
    )
    db.session.add(new_user)
    db.session.commit()

    # Buat JWT token
    access_token = create_access_token(identity=str(new_user.id))

    return jsonify({
        "message": "Registrasi berhasil!",
        "user": new_user.to_dict(),
        "access_token": access_token,
    }), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Login user.

    Body JSON:
        {
            "email": "reyhan@example.com",
            "password": "password123"
        }

    Returns:
        200: Login berhasil + JWT token
        400: Validasi gagal
        401: Email atau password salah
    """
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body tidak boleh kosong"}), 400

    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not email or not password:
        return jsonify({"error": "Email dan password wajib diisi"}), 400

    # Cari user berdasarkan email
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"error": "Email atau password salah"}), 401

    # Verifikasi password
    if not bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
        return jsonify({"error": "Email atau password salah"}), 401

    # Buat JWT token
    access_token = create_access_token(identity=str(user.id))

    return jsonify({
        "message": "Login berhasil!",
        "user": user.to_dict(),
        "access_token": access_token,
    }), 200
