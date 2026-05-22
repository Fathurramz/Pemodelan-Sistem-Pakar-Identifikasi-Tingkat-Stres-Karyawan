from app import db
from datetime import datetime


class User(db.Model):
    """Model untuk tabel users."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relasi ke assessments
    assessments = db.relationship("Assessment", backref="user", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "created_at": self.created_at.strftime("%d %B %Y"),
        }


class Question(db.Model):
    """Model untuk tabel questions (pertanyaan kuesioner)."""

    __tablename__ = "questions"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.Text, nullable=False)
    category = db.Column(
        db.Enum("beban_kerja", "lingkungan_kerja", "kesehatan", name="category_enum"),
        nullable=False,
    )
    order_number = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "category": self.category,
            "order_number": self.order_number,
        }


class Assessment(db.Model):
    """Model untuk tabel assessments (hasil tes stres)."""

    __tablename__ = "assessments"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    stress_level = db.Column(
        db.Enum("Rendah", "Sedang", "Tinggi", name="stress_level_enum"),
        nullable=False,
    )
    factors = db.Column(db.JSON, nullable=False)
    recommendations = db.Column(db.JSON, nullable=False)
    answers = db.Column(db.JSON, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.user.name if self.user else "Unknown",
            "score": self.score,
            "stressLevel": self.stress_level,
            "factors": self.factors,
            "recommendations": self.recommendations,
            "lastTest": self.created_at.strftime("%d %B %Y"),
        }
