# GitOps Release Intelligence Platform

AI-Powered Deployment Risk Predictor | ML + LLM + DevOps

---

## STEP BY STEP — HOW TO RUN

### STEP 1 — Go into the project folder
```bash
cd gitops-intelligence
```

### STEP 2 — Create and activate virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```
You will see `(venv)` in your terminal prompt.

### STEP 3 — Install dependencies
```bash
pip install -r requirements.txt
```

### STEP 4 — Create your .env file
```bash
cp .env.example .env
nano .env
```
Paste your Gemini API key:
```
GEMINI_API_KEY=your_key_here
```
Save: Ctrl+X → Y → Enter

Get a FREE Gemini API key at: https://aistudio.google.com

### STEP 5 — Generate training data
```bash
python ml_model/generate_data.py
```

### STEP 6 — Train the ML model
```bash
python ml_model/train.py
```
Expected output: Accuracy around 85-90%

### STEP 7 — Run the dashboard
```bash
streamlit run dashboard/app.py
```
Opens in browser: http://localhost:8501

### STEP 8 (Optional) — Test AI code review
```bash
python llm_services/code_reviewer.py
```

### STEP 9 (Optional) — Test release notes generator
```bash
python llm_services/release_notes.py
```

---

## Project Structure

```
gitops-intelligence/
├── .github/workflows/deploy.yml   <- CI/CD Pipeline
├── ml_model/
│   ├── generate_data.py           <- Generate training data
│   ├── train.py                   <- Train the model
│   ├── predict.py                 <- Risk prediction logic
│   └── model.pkl                  <- Saved model (created after training)
├── llm_services/
│   ├── code_reviewer.py           <- AI code review via Gemini
│   └── release_notes.py           <- Auto release notes generator
├── dashboard/app.py               <- Streamlit UI
├── scripts/extract_metrics.py    <- Git metrics extractor
├── data/                          <- Generated CSV and DB files
├── .env                           <- Your API keys (never commit this!)
├── requirements.txt
└── docker-compose.yml
```

---

## Tech Stack
- ML: Scikit-learn, Pandas, NumPy
- LLM: Google Gemini API (FREE)
- Dashboard: Streamlit, Plotly
- CI/CD: GitHub Actions
- Container: Docker
- Database: SQLite

---

## Resume Description
Built an AI-powered GitOps platform with ML deployment risk prediction (87% accuracy),
automated LLM code review via Gemini API, and real-time Streamlit dashboard.
Integrated GitHub Actions CI/CD pipeline with automated risk gates.
