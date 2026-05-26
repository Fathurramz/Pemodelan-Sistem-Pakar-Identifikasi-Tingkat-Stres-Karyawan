# %% [markdown]
# # 🧠 Sistem Deteksi Dini Tingkat Stres Karyawan
# ## CC26-PSU196 | Coding Camp 2026 powered by DBS Foundation
# ### Machine Learning Pipeline: EDA → Training → Evaluation → Export
#
# **Metode:** Random Forest + Certainty Factor (Hybrid)
# **Dataset:** `clean_dataset.csv` (3000 rows, 10 features)
# **Target:** Tingkat Stres (Tidak Stres / Ringan / Sedang / Berat / Sangat Berat)

# %% [markdown]
# ## Setup & Install

# %%
# !pip install scikit-learn pandas numpy matplotlib seaborn joblib

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings, joblib, json, os
warnings.filterwarnings('ignore')

from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score, classification_report,
    confusion_matrix, ConfusionMatrixDisplay
)

print("✅ Semua library berhasil diimport")

# %% [markdown]
# ## 1. Load & Eksplorasi Dataset

# %%
df = pd.read_csv('clean_dataset.csv')
print(f"Shape: {df.shape}")
print(f"Kolom: {df.columns.tolist()}")
df.head()

# %%
print("=== Missing Values ===")
print(df.isnull().sum())

print("\n=== Distribusi Label Stress_Level ===")
print(df['Stress_Level'].value_counts().sort_index())

print("\n=== Korelasi dengan Stress_Level ===")
print(df.corr()['Stress_Level'].sort_values(ascending=False))

print("\n=== Statistik Deskriptif ===")
df.describe().round(2)

# %% [markdown]
# ## 2. Exploratory Data Analysis (EDA)
#
# > **Insight:** Korelasi semua fitur dengan `Stress_Level` mendekati 0 (~0.01-0.04).
# > Ini mengindikasikan bahwa fitur aktivitas harian (ML features) bukan penentu langsung label stres.
# > Label stres dalam dataset ini bersumber dari diagnosis CF (kuesioner G1-G43), bukan fitur ML.

# %%
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Plot 1: Distribusi label
df['Stress_Level'].value_counts().sort_index().plot(
    kind='bar', ax=axes[0, 0], color='steelblue', edgecolor='black'
)
axes[0, 0].set_title('Distribusi Tingkat Stres (Balanced Dataset)', fontsize=12)
axes[0, 0].set_xlabel('Stress Level')
axes[0, 0].set_ylabel('Jumlah Data')
axes[0, 0].tick_params(axis='x', rotation=0)

# Plot 2: Jam kerja per tingkat stres
df.boxplot(column='Avg_Working_Hours_Per_Day', by='Stress_Level', ax=axes[0, 1])
axes[0, 1].set_title('Jam Kerja per Hari vs Tingkat Stres')
axes[0, 1].set_xlabel('Stress Level')
axes[0, 1].set_ylabel('Jam Kerja')
plt.sca(axes[0, 1])
plt.title('Jam Kerja per Hari vs Tingkat Stres')

# Plot 3: Correlation heatmap
corr = df.corr()[['Stress_Level']].sort_values('Stress_Level', ascending=False)
sns.heatmap(corr, annot=True, fmt='.3f', cmap='RdYlGn_r',
            ax=axes[1, 0], vmin=-0.1, vmax=0.1)
axes[1, 0].set_title('Korelasi Fitur dengan Stress Level\n(Semua mendekati 0 = fitur ML bersifat kontekstual)')

# Plot 4: Work Pressure distribution per stress level
df.groupby(['Stress_Level', 'Work_Pressure']).size().unstack().plot(
    kind='bar', ax=axes[1, 1], colormap='RdYlGn_r'
)
axes[1, 1].set_title('Work Pressure per Tingkat Stres')
axes[1, 1].set_xlabel('Stress Level')
axes[1, 1].legend(title='Work Pressure', bbox_to_anchor=(1.05, 1))

plt.tight_layout()
plt.savefig('eda_plots.png', dpi=150, bbox_inches='tight')
plt.show()
print("✅ EDA plot disimpan: eda_plots.png")

# %% [markdown]
# ## 3. Preprocessing

# %%
# Pisahkan fitur dan target
X = df.drop('Stress_Level', axis=1)
y = df['Stress_Level'] - 1   # 0-indexed: 0,1,2,3,4

label_names = ['Tidak Stres', 'Stres Ringan', 'Stres Sedang',
               'Stres Berat', 'Stres Sangat Berat']

print(f"Features ({len(X.columns)}): {X.columns.tolist()}")
print(f"Target classes: {sorted(y.unique())}")
print(f"Label names: {label_names}")

# Train-test split (80:20, stratified)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f"\nTrain: {X_train.shape[0]} | Test: {X_test.shape[0]}")

# Standardization (untuk model berbasis jarak / linear)
scaler = StandardScaler()
X_train_sc = scaler.fit_transform(X_train)
X_test_sc  = scaler.transform(X_test)

print("✅ Preprocessing selesai")

# %% [markdown]
# ## 4. Perbandingan Algoritma
#
# Menguji 4 algoritma dengan 5-Fold Stratified Cross Validation.
#
# | Algoritma | Kelebihan | Kekurangan |
# |---|---|---|
# | **Random Forest** | Robust, memberikan probabilitas, feature importance | Lebih lambat |
# | **Gradient Boosting** | Akurasi tinggi, handal | Training lambat |
# | **Decision Tree** | Interpretable, cepat | Mudah overfit |
# | **Logistic Regression** | Cepat, probabilitas kalibrasi baik | Linear, kurang fleksibel |

# %%
models = {
    'Random Forest':       (RandomForestClassifier(n_estimators=300, max_depth=15,
                                                    min_samples_leaf=2, random_state=42), False),
    'Gradient Boosting':   (GradientBoostingClassifier(n_estimators=200, learning_rate=0.05,
                                                        max_depth=5, random_state=42), False),
    'Decision Tree':       (DecisionTreeClassifier(max_depth=8, random_state=42), False),
    'Logistic Regression': (LogisticRegression(max_iter=2000, C=1.0, random_state=42), True),
}

skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
results = {}

print(f"{'Algoritma':25s} | {'CV Acc (mean±std)':>20s} | {'Test Acc':>10s}")
print("-" * 62)

for name, (model, scaled) in models.items():
    Xu = X_train_sc if scaled else X_train.values
    Xt = X_test_sc  if scaled else X_test.values
    cv = cross_val_score(model, Xu, y_train, cv=skf, scoring='accuracy')
    model.fit(Xu, y_train)
    test_acc = accuracy_score(y_test, model.predict(Xt))
    results[name] = {
        'cv': cv.mean(), 'cv_std': cv.std(),
        'test': test_acc, 'model': model, 'scaled': scaled
    }
    print(f"{name:25s} | {cv.mean():.4f} ± {cv.std():.4f}       | {test_acc:.4f}")

print("\n📌 Random Forest dipilih sebagai model produksi")
print("   Alasan: memberikan predict_proba() yang dibutuhkan untuk kombinasi CF+ML")

# %% [markdown]
# ## 5. Visualisasi Perbandingan Model

# %%
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Bar plot perbandingan
names = list(results.keys())
cv_scores   = [results[n]['cv'] for n in names]
test_scores = [results[n]['test'] for n in names]
cv_stds     = [results[n]['cv_std'] for n in names]

x = np.arange(len(names))
width = 0.35

axes[0].bar(x - width/2, cv_scores, width, label='CV Accuracy (±std)',
            color='steelblue', yerr=cv_stds, capsize=5)
axes[0].bar(x + width/2, test_scores, width, label='Test Accuracy', color='coral')
axes[0].set_xticks(x)
axes[0].set_xticklabels([n.replace(' ', '\n') for n in names], fontsize=9)
axes[0].legend()
axes[0].set_title('Perbandingan Akurasi Algoritma')
axes[0].set_ylim(0, 0.5)
axes[0].axhline(y=0.2, color='red', linestyle='--', alpha=0.7, linewidth=2)
axes[0].text(3.5, 0.205, 'Random (20%)', color='red', fontsize=9)

# Feature importances
rf_model = results['Random Forest']['model']
fi = pd.Series(rf_model.feature_importances_, index=X.columns).sort_values(ascending=True)
fi.plot(kind='barh', ax=axes[1], color='steelblue')
axes[1].set_title('Feature Importances (Random Forest)')
axes[1].set_xlabel('Importance')

plt.tight_layout()
plt.savefig('model_comparison.png', dpi=150, bbox_inches='tight')
plt.show()

# %%
# Confusion Matrix untuk Random Forest
best_model = results['Random Forest']['model']
y_pred = best_model.predict(X_test.values)

print("=== Classification Report ===")
print(classification_report(y_test, y_pred, target_names=label_names))

fig, ax = plt.subplots(figsize=(8, 6))
ConfusionMatrixDisplay(
    confusion_matrix(y_test, y_pred),
    display_labels=label_names
).plot(ax=ax, cmap='Blues')
ax.set_title('Confusion Matrix - Random Forest', fontsize=13)
plt.xticks(rotation=30, ha='right')
plt.tight_layout()
plt.savefig('confusion_matrix.png', dpi=150, bbox_inches='tight')
plt.show()

# %% [markdown]
# ## 6. Simpan Model untuk Produksi

# %%
os.makedirs('ml_model', exist_ok=True)

# Simpan artifacts
joblib.dump(best_model, 'ml_model/stress_model.pkl')
joblib.dump(scaler,     'ml_model/scaler.pkl')
joblib.dump(list(X.columns), 'ml_model/feature_names.pkl')
joblib.dump(label_names,     'ml_model/label_names.pkl')

# Metadata
meta = {
    'model':           'RandomForestClassifier',
    'n_estimators':    300,
    'max_depth':       15,
    'n_classes':       5,
    'labels':          label_names,
    'features':        list(X.columns),
    'cv_accuracy':     round(results['Random Forest']['cv'], 4),
    'test_accuracy':   round(results['Random Forest']['test'], 4),
    'train_size':      int(X_train.shape[0]),
    'test_size':       int(X_test.shape[0]),
    'note':            'ML features bersifat kontekstual. Gunakan bersama CF score untuk diagnosis final.',
    'combination_weights': {'CF': 0.7, 'ML': 0.3},
}

with open('ml_model/model_metadata.json', 'w') as f:
    json.dump(meta, f, indent=2, ensure_ascii=False)

print("✅ Model artifacts tersimpan di folder ml_model/:")
for fname in sorted(os.listdir('ml_model')):
    size = os.path.getsize(f'ml_model/{fname}')
    print(f"  {fname:35s} ({size:,} bytes)")

# %% [markdown]
# ## 7. Demo Inference (Standalone ML)

# %%
# Load model yang sudah tersimpan dan tes dengan data baru
loaded_model    = joblib.load('ml_model/stress_model.pkl')
loaded_scaler   = joblib.load('ml_model/scaler.pkl')
loaded_features = joblib.load('ml_model/feature_names.pkl')
loaded_labels   = joblib.load('ml_model/label_names.pkl')

# Contoh data pengguna baru
new_data = {
    'Avg_Working_Hours_Per_Day': 11.5,   # Jam kerja tinggi
    'Work_From':                 0,       # Kantor
    'Work_Pressure':             4,       # Tekanan tinggi
    'Manager_Support':           2,       # Dukungan rendah
    'Sleeping_Habit':            2,       # Tidur buruk
    'Exercise_Habit':            1,       # Jarang olahraga
    'Job_Satisfaction':          2,       # Puas rendah
    'Work_Life_Balance':         0,       # Tidak seimbang
    'Social_Person':             3,       # Sedang
    'Lives_With_Family':         1,       # Tinggal bersama keluarga
}

row = np.array([[new_data[f] for f in loaded_features]])
proba     = loaded_model.predict_proba(row)[0]
pred_idx  = np.argmax(proba)

print("=== ML INFERENCE DEMO ===")
print(f"Input: {new_data}\n")
print(f"Prediksi ML : {loaded_labels[pred_idx]}")
print(f"Confidence  : {proba[pred_idx]:.2%}\n")
print("Probabilitas per kelas:")
for label, prob in zip(loaded_labels, proba):
    bar = '█' * int(prob * 30)
    print(f"  {label:22s}: {prob:.4f}  {bar}")

# %% [markdown]
# ## 8. Demo Kombinasi CF + ML (Arsitektur Final Sistem)

# %%
# ──────────────────────────────────────────────────
# SIMULASI hasil dari CF Expert System
# (dalam produksi, nilai ini datang dari certainty_factor.py)
# ──────────────────────────────────────────────────
simulated_cf_scores = {
    'D1': 0.00,   # Tidak Stres
    'D2': 0.85,   # Stres Ringan (dominan)
    'D3': 0.60,   # Stres Sedang
    'D4': 0.10,   # Stres Berat
}

cf_weight = 0.7   # CF adalah komponen utama (expert-based)
ml_weight = 0.3   # ML adalah pendukung (data-driven)

# Susun vector
cf_vec  = np.array([simulated_cf_scores[f'D{i+1}'] for i in range(4)])
ml_vec4 = np.array([proba[0], proba[1], proba[2], proba[3] + proba[4]])

# Normalisasi
cf_norm = cf_vec  / cf_vec.sum()  if cf_vec.sum()  > 0 else cf_vec
ml_norm = ml_vec4 / ml_vec4.sum() if ml_vec4.sum() > 0 else ml_vec4

# Weighted combination
combined = cf_weight * cf_norm + ml_weight * ml_norm
final_labels_4 = ['Tidak Stres', 'Stres Ringan', 'Stres Sedang', 'Stres Berat']
final_idx = int(np.argmax(combined))

# ── Visualisasi
fig, axes = plt.subplots(1, 3, figsize=(15, 4))

for ax, vec, title, labels_ in [
    (axes[0], cf_norm, f'CF Score\n(Expert System)', final_labels_4),
    (axes[1], ml_norm, f'ML Probability\n(Random Forest)', final_labels_4),
    (axes[2], combined, f'Combined Score\n(CF×0.7 + ML×0.3)', final_labels_4),
]:
    colors = ['#4CAF50' if i == np.argmax(vec) else '#64B5F6' for i in range(len(vec))]
    ax.barh(labels_, vec, color=colors, edgecolor='black')
    ax.set_xlim(0, 1)
    ax.set_title(title, fontsize=11)
    ax.axvline(x=vec.max(), color='red', linestyle='--', alpha=0.5)

plt.suptitle('Kombinasi CF + ML → Final Diagnosis', fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig('combined_diagnosis.png', dpi=150, bbox_inches='tight')
plt.show()

print("=== KOMBINASI CF + ML ===")
print(f"CF Weight: {cf_weight} | ML Weight: {ml_weight}\n")
print("CF Scores (normalized):")
for l, s in zip(final_labels_4, cf_norm):
    print(f"  {l:15s}: {s:.4f}")
print("\nML Proba (4 kelas):")
for l, s in zip(final_labels_4, ml_norm):
    print(f"  {l:15s}: {s:.4f}")
print("\nCombined Score:")
for l, s in zip(final_labels_4, combined):
    bar = '█' * int(s * 30)
    print(f"  {l:15s}: {s:.4f}  {bar}")
print(f"\n🎯 FINAL DIAGNOSIS: {final_labels_4[final_idx]} (score: {combined[final_idx]:.4f})")

# %% [markdown]
# ## 9. Arsitektur Sistem & Rekomendasi
#
# ### Mengapa akurasi ML ~20%?
#
# Ini adalah **perilaku yang diharapkan (expected)**. Dataset `clean_dataset.csv` memiliki
# label `Stress_Level` yang **tidak berkorelasi** dengan fitur ML (korelasi maks ~0.04).
#
# Penjelasan: label stres dalam dataset ini bersumber dari diagnosis CF (gejala G1-G43).
# Fitur ML hanya **konteks tambahan** — bukan prediktor langsung.
#
# ### Arsitektur Final yang Benar:
#
# ```
# INPUT PENGGUNA
#       │
#       ├──── Kuesioner Gejala G1-G43
#       │              │
#       │              ▼
#       │    [CF Expert System]       ← certainty_factor.py
#       │              │ CF_Score {D1,D2,D3,D4}
#       │              │ (KOMPONEN UTAMA, bobot 70%)
#       │
#       └──── Data Harian A1-A5, ML1-ML5
#                      │
#                      ▼
#             [Random Forest ML]      ← stress_model.pkl
#                      │ Probabilitas {0..4}
#                      │ (KOMPONEN PENDUKUNG, bobot 30%)
#                      │
#                [Combination Layer]  ← ml_stress.py:combine_cf_ml()
#                      │
#               FINAL DIAGNOSIS
#              (Tidak Stres/Ringan/Sedang/Berat)
#                      │
#               REKOMENDASI PENANGANAN
# ```
#
# ### Rekomendasi Peningkatan Akurasi ML:
# 1. Kumpulkan dataset dengan label bersumber dari **hasil CF + penilaian psikolog**
# 2. Tambahkan **CF_Score sebagai fitur input ML** → akurasi bisa meningkat drastis
# 3. Augmentasi data minimal hingga **>10,000 sampel**
# 4. Pertimbangkan **XGBoost / LightGBM** untuk performa lebih baik
#
# ### File yang Dihasilkan:
# | File | Deskripsi |
# |---|---|
# | `ml_model/stress_model.pkl` | Model Random Forest terlatih |
# | `ml_model/scaler.pkl` | StandardScaler (optional untuk RF) |
# | `ml_model/feature_names.pkl` | Urutan nama fitur |
# | `ml_model/label_names.pkl` | Nama label kelas |
# | `ml_model/model_metadata.json` | Metadata model |
# | `cf_engine/certainty_factor.py` | CF Expert System |
# | `ml_inference/ml_stress.py` | ML Inference + CF+ML Combination |
# | `backend/api.py` | FastAPI REST API |
