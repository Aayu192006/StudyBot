# 🎓 StudyBot — AI-Powered Study Assistant

A full-stack chatbot that predicts student grades using an ML model, fetches
study notes via Google Custom Search, and generates personalized responses
using Claude AI.

---

## 📁 Project Structure

```
study-chatbot/
├── backend/
│   ├── main.py            ← FastAPI app (ML + Claude + Search)
│   ├── train_model.py     ← Train & save the grade prediction model
│   ├── requirements.txt
│   └── .env.example       ← Copy to .env and fill in your keys
└── frontend/
    └── index.html         ← Complete chat UI (open in browser)
```

---

## ⚙️ Setup — Backend

### 1. Install Python dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure API keys

```bash
cp .env.example .env
```

Edit `.env` and fill in:

| Variable           | Where to get it |
|--------------------|-----------------|
| `ANTHROPIC_API_KEY`| https://console.anthropic.com/ |
| `GOOGLE_API_KEY`   | https://console.cloud.google.com/ → Custom Search JSON API |
| `GOOGLE_CSE_ID`    | https://programmablesearchengine.google.com/ |

### 3. Train the ML model

If you have your own dataset (CSV with columns: weekly_study_hours,
attendance_percentage, class_participation, total_score, grade):

```python
# In train_model.py, replace the synthetic data block with:
import pandas as pd
df = pd.read_csv("your_dataset.csv")
X = df[["weekly_study_hours","attendance_percentage","class_participation","total_score"]]
y = df["grade"]
```

Then run:

```bash
cd backend
python train_model.py
```

This saves `grade_model.pkl` — the FastAPI server loads it automatically.

### 4. Start the server

```bash
cd backend
uvicorn main:app --reload --port 8000
```

The API will be live at `http://localhost:8000`.
Swagger docs: `http://localhost:8000/docs`

---

## 🌐 Setup — Frontend

No build step needed. Just open `frontend/index.html` in your browser:

```bash
# macOS / Linux
open frontend/index.html

# Windows
start frontend/index.html
```

Or serve it locally:

```bash
cd frontend
python -m http.server 5500
# then open http://localhost:5500
```

Make sure the backend is running on port 8000 before using the chat.

---

## 🔌 API Endpoints

| Method | Endpoint         | Description |
|--------|-----------------|-------------|
| GET    | `/`              | Health check |
| GET    | `/health`        | Model load status |
| POST   | `/predict-grade` | Predict grade from metrics |
| POST   | `/chat`          | Full chatbot (grade + search + Claude) |

### POST `/predict-grade`

```json
{
  "weekly_study_hours": 15,
  "attendance_percentage": 85,
  "class_participation": 7,
  "total_score": 72
}
```

Response:
```json
{ "grade": "B", "confidence": null, "method": "ml_model" }
```

### POST `/chat`

```json
{
  "message": "I am weak in Physics",
  "metrics": {
    "weekly_study_hours": 15,
    "attendance_percentage": 85,
    "class_participation": 7,
    "total_score": 72
  },
  "conversation_history": []
}
```

Response:
```json
{
  "reply": "...",
  "grade_info": { "grade": "B", "method": "ml_model" },
  "subject_detected": "Physics",
  "search_results": [...]
}
```

---

## 🧠 How It Works

```
User Input (metrics + message)
        │
        ├─→ ML Model → Predicted Grade (A/B/C/D/F)
        │
        ├─→ Keyword Extractor → Weak Subject detected
        │
        ├─→ Google Custom Search → Top study notes/resources
        │
        └─→ Claude API (with grade + search results as context)
                  │
                  └─→ Personalized response with notes, tips, links
```

---

## 🛠️ Customization

### Add more subjects to detect

In `main.py`, `extract_subject()` — extend the keywords list or use
a small NLP model (spaCy NER) for better subject detection.

### Use your real dataset

Replace the synthetic data in `train_model.py` with your CSV.
Supported grade formats: `A`, `B`, `C`, `D`, `F` (or numeric 0–100
which you can bin into grades).

### Change the Claude model

In `main.py`, edit the `model=` parameter:
```python
model="claude-opus-4-20250514"  # More powerful, slower
model="claude-haiku-4-5-20251001"  # Fastest, cheapest
```

### Deploy

- **Backend**: Deploy to Railway, Render, or any Python host. Set env vars in their dashboard.
- **Frontend**: Deploy to Vercel, Netlify, or GitHub Pages. Update `API_BASE` in `index.html` to your backend URL.

---

## 📦 Requirements

- Python 3.10+
- Node.js (not required — pure HTML frontend)
- Anthropic API key
- Google Custom Search API key + CSE ID

---

## 📄 License

MIT
