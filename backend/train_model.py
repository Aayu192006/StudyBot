"""
train_model.py  —  Train and save the grade prediction ML model.

Features:
  - weekly_study_hours    (0–40)
  - attendance_percentage (0–100)
  - class_participation   (0–10)
  - total_score           (0–100)

Labels: A, B, C, D, F

Run:
  python train_model.py
"""

import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder

# ─── SYNTHETIC DATASET ────────────────────────────────────────────────────────
import pandas as pd
print("Loading real dataset...")
df = pd.read_csv("student_performance.csv")

# Sample down for swift, optimal training without maxing out system memory
if len(df) > 50000:
    df = df.sample(n=50000, random_state=42)

print("Formatting Data...")
X = df[["weekly_self_study_hours", "attendance_percentage", "class_participation", "total_score"]]
y = df["grade"]

# ─── TRAIN ────────────────────────────────────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=200, max_depth=10, random_state=42)
model.fit(X_train, y_train)

# ─── EVALUATE ─────────────────────────────────────────────────────────────────
y_pred = model.predict(X_test)
print("=== Classification Report ===")
print(classification_report(y_test, y_pred))

importances = model.feature_importances_
feature_names = ["study_hours", "attendance", "participation", "total_score"]
print("\n=== Feature Importances ===")
for name, imp in sorted(zip(feature_names, importances), key=lambda x: -x[1]):
    print(f"  {name:25s}: {imp:.3f}")

# ─── SAVE ─────────────────────────────────────────────────────────────────────
joblib.dump(model, "grade_model.pkl")
print("\n✅ Model saved to grade_model.pkl")

# Quick sanity check
sample = np.array([[20, 85, 7, 72]])  # 20h study, 85% attendance, 7/10 participation, 72 score
print(f"\nSample prediction {sample.tolist()[0]} → {model.predict(sample)[0]}")
print(f"Probabilities: { {cls: round(p,2) for cls, p in zip(model.classes_, model.predict_proba(sample)[0])} }")
