from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Assessment, Question, User
from app.utils.expert_system import analyze_stress

assessments_bp = Blueprint("assessments", __name__)


@assessments_bp.route("/assessments", methods=["POST"])
@jwt_required()
def submit_assessment():
    """
    Submit jawaban kuesioner dan dapatkan analisis stres.

    Header:
        Authorization: Bearer <JWT_TOKEN>

    Body JSON:
        {
            "answers": {
                "1": 4,
                "2": 3,
                "3": 5,
                ...
            }
        }

    Returns:
        201: Hasil analisis stres
        400: Validasi gagal
    """
    user_id = get_jwt_identity()
    data = request.get_json()

    if not data or "answers" not in data:
        return jsonify({"error": "Jawaban kuesioner wajib diisi"}), 400

    answers = data["answers"]

    # Validasi jawaban
    if not isinstance(answers, dict) or len(answers) == 0:
        return jsonify({"error": "Format jawaban tidak valid"}), 400

    # Ambil semua pertanyaan dari database
    questions = Question.query.all()

    if not questions:
        return jsonify({"error": "Belum ada pertanyaan di database. Jalankan seed terlebih dahulu."}), 500

    # Jalankan analisis sistem pakar (forward chaining)
    result = analyze_stress(answers, questions)

    # Simpan hasil ke database
    assessment = Assessment(
        user_id=int(user_id),
        score=result["score"],
        stress_level=result["stress_level"],
        factors=result["factors"],
        recommendations=result["recommendations"],
        answers=answers,
    )
    db.session.add(assessment)
    db.session.commit()

    return jsonify({
        "message": "Analisis stres berhasil!",
        "result": assessment.to_dict(),
    }), 201


@assessments_bp.route("/stress-result", methods=["GET"])
@jwt_required()
def get_stress_result():
    """
    Ambil hasil analisis stres terakhir dari user yang sedang login.

    Header:
        Authorization: Bearer <JWT_TOKEN>

    Returns:
        200: Hasil analisis stres terakhir
        404: Belum pernah melakukan tes
    """
    user_id = get_jwt_identity()

    # Ambil assessment terbaru milik user ini
    assessment = (
        Assessment.query
        .filter_by(user_id=int(user_id))
        .order_by(Assessment.created_at.desc())
        .first()
    )

    if not assessment:
        return jsonify({"error": "Anda belum pernah melakukan tes. Silakan selesaikan kuesioner terlebih dahulu."}), 404

    return jsonify(assessment.to_dict()), 200


@assessments_bp.route("/assessments/history", methods=["GET"])
@jwt_required()
def get_assessment_history():
    """
    Ambil semua riwayat tes stres milik user.

    Returns:
        200: List riwayat assessment
    """
    user_id = get_jwt_identity()

    assessments = (
        Assessment.query
        .filter_by(user_id=int(user_id))
        .order_by(Assessment.created_at.desc())
        .all()
    )

    return jsonify({
        "history": [a.to_dict() for a in assessments],
        "total": len(assessments),
    }), 200
