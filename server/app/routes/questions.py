from flask import Blueprint, jsonify
from app.models import Question

questions_bp = Blueprint("questions", __name__)


@questions_bp.route("/questions", methods=["GET"])
def get_questions():
    """
    Ambil semua pertanyaan kuesioner, urut berdasarkan order_number.

    Returns:
        200: List pertanyaan
        [
            {
                "id": 1,
                "text": "Seberapa sering Anda merasa kewalahan...",
                "category": "beban_kerja",
                "order_number": 1
            },
            ...
        ]
    """
    questions = Question.query.order_by(Question.order_number).all()

    return jsonify({
        "questions": [q.to_dict() for q in questions],
        "total": len(questions),
    }), 200
