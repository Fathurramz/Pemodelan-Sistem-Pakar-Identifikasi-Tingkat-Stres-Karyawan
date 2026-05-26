"""
FastAPI Backend - Sistem Deteksi Dini Tingkat Stres Karyawan
CC26-PSU196 | Coding Camp 2026 powered by DBS Foundation

Endpoints:
  POST /api/diagnose/cf          - CF-only diagnosis
  POST /api/diagnose/ml          - ML-only prediction
  POST /api/diagnose/combined    - CF + ML combined (recommended)
  GET  /api/health               - Health check
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, Optional
import sys, os

# Add parent dirs to path (adjust as needed in your project)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from certainty_factor import (
    diagnose as cf_diagnose,
    answers_from_text,
    answers_from_numeric,
    USER_CF_MAP,
    KNOWLEDGE_BASE,
    DIAGNOSES,
)
from ml_stress import (
    predict_stress_probability,
    combine_cf_ml,
    FEATURE_INFO,
)

app = FastAPI(
    title="Stress Detection API",
    description="Sistem Deteksi Dini Tingkat Stres Karyawan - CC26-PSU196",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ganti dengan domain frontend di production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─────────────────────────────────────────
# SCHEMAS
# ─────────────────────────────────────────

class CFRequest(BaseModel):
    """
    Request untuk CF diagnosis.
    symptom_answers: {kode_gejala: nilai_cf_user (0.0-1.0)}
    Atau gunakan jawaban numerik: {kode_gejala: int (0-4)}
    """
    symptom_answers: Dict[str, float] = Field(
        ...,
        example={
            "G1": 0.75, "G2": 1.0, "G3": 0.75,
            "G6": 0.5, "G16": 0.75,
        }
    )


class CFTextRequest(BaseModel):
    """CF dengan jawaban teks (tidak_pernah/jarang/kadang_kadang/sering/selalu)"""
    symptom_answers: Dict[str, str] = Field(
        ...,
        example={"G1": "sering", "G2": "selalu", "G3": "sering"}
    )


class MLRequest(BaseModel):
    """Request untuk ML prediction."""
    Avg_Working_Hours_Per_Day: float = Field(..., ge=1.0, le=24.0, example=9.5)
    Work_From: int = Field(..., ge=0, le=2, example=1,
                           description="0=Kantor, 1=WFH, 2=Hybrid")
    Work_Pressure: int = Field(..., ge=1, le=5, example=4)
    Manager_Support: int = Field(..., ge=1, le=5, example=3)
    Sleeping_Habit: int = Field(..., ge=1, le=5, example=3)
    Exercise_Habit: int = Field(..., ge=1, le=5, example=2)
    Job_Satisfaction: int = Field(..., ge=1, le=5, example=3)
    Work_Life_Balance: int = Field(..., ge=0, le=1, example=0,
                                   description="0=Tidak, 1=Ya")
    Social_Person: int = Field(..., ge=1, le=5, example=3)
    Lives_With_Family: int = Field(..., ge=0, le=1, example=1,
                                   description="0=Tidak, 1=Ya")


class CombinedRequest(BaseModel):
    """Request untuk combined CF + ML diagnosis."""
    cf_answers: Dict[str, float] = Field(
        ...,
        description="Jawaban kuesioner CF (G1-G43): {kode: cf_user (0.0-1.0)}"
    )
    ml_features: MLRequest
    cf_weight: float = Field(default=0.7, ge=0.0, le=1.0,
                              description="Bobot CF dalam kombinasi (default 0.7)")


# ─────────────────────────────────────────
# ROUTES
# ─────────────────────────────────────────

@app.get("/api/health")
def health_check():
    return {"status": "ok", "service": "Stress Detection API v1.0.0"}


@app.post("/api/diagnose/cf")
def diagnose_cf(request: CFRequest):
    """
    Diagnosis menggunakan metode Certainty Factor saja.
    Input: jawaban kuesioner G1-G43 dengan nilai CF user (0.0-1.0)
    """
    try:
        result = cf_diagnose(request.symptom_answers)
        return {
            "method": "Certainty Factor",
            "diagnosis": result["diagnosis_label"],
            "diagnosis_code": result["diagnosis_code"],
            "cf_score": result["cf_score"],
            "cf_percentage": result["cf_percentage"],
            "all_scores": result["all_scores"],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/diagnose/cf/text")
def diagnose_cf_text(request: CFTextRequest):
    """CF dengan jawaban teks: tidak_pernah/jarang/kadang_kadang/sering/selalu"""
    try:
        cf_answers = answers_from_text(request.symptom_answers)
        result = cf_diagnose(cf_answers)
        return {
            "method": "Certainty Factor (text input)",
            "diagnosis": result["diagnosis_label"],
            "diagnosis_code": result["diagnosis_code"],
            "cf_score": result["cf_score"],
            "cf_percentage": result["cf_percentage"],
            "all_scores": result["all_scores"],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/diagnose/ml")
def diagnose_ml(request: MLRequest):
    """
    Prediksi menggunakan Machine Learning saja.
    Input: fitur aktivitas harian (A1-A5, ML1-ML5)
    """
    try:
        features = request.model_dump()
        result = predict_stress_probability(features)
        return {
            "method": "Machine Learning (Random Forest)",
            "predicted_label": result["predicted_label"],
            "confidence": result["confidence"],
            "probabilities": result["probabilities"],
            "note": "ML model memberikan probabilitas sebagai pendukung CF diagnosis",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/diagnose/combined")
def diagnose_combined(request: CombinedRequest):
    """
    Diagnosis hybrid: CF (utama) + ML (pendukung).
    Ini adalah endpoint utama yang direkomendasikan.
    """
    try:
        # CF diagnosis
        cf_result = cf_diagnose(request.cf_answers)

        # ML prediction
        ml_features = request.ml_features.model_dump()
        ml_result = predict_stress_probability(ml_features)

        # Combine
        final = combine_cf_ml(cf_result, ml_result, cf_weight=request.cf_weight)

        return {
            "method": "Hybrid (CF + ML)",
            "final_diagnosis": final["final_diagnosis"],
            "final_code": final["final_code"],
            "final_score": final["final_score"],
            "score_breakdown": final["score_breakdown"],
            "cf_detail": {
                "diagnosis": cf_result["diagnosis_label"],
                "cf_score": cf_result["cf_score"],
                "cf_percentage": cf_result["cf_percentage"],
                "all_scores": cf_result["all_scores"],
            },
            "ml_detail": {
                "predicted": ml_result["predicted_label"],
                "confidence": ml_result["confidence"],
                "probabilities": ml_result["probabilities"],
            },
            "recommendation": final["recommendation"],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/knowledge-base")
def get_knowledge_base():
    """Ambil daftar gejala dan CF pakar (untuk admin)."""
    return {
        "symptoms": KNOWLEDGE_BASE,
        "diagnoses": DIAGNOSES,
        "cf_user_scale": USER_CF_MAP,
    }


# ─────────────────────────────────────────
# RUN (development)
# ─────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
