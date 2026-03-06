"""
Risk prediction script used by both dashboard and GitHub Actions
"""
import joblib
import json
import sys
import pandas as pd
import os

FEATURES = [
    'files_changed', 'lines_added', 'lines_deleted',
    'hour_of_day', 'day_of_week', 'days_since_last_deploy',
    'recent_failures', 'test_pass_rate', 'is_main_branch',
    'num_contributors'
]

def predict_risk(metrics: dict) -> dict:
    model_path = os.path.join(os.path.dirname(__file__), 'model.pkl')

    if not os.path.exists(model_path):
        return {
            "risk_score": 50.0,
            "status": "UNKNOWN",
            "recommendation": "Model not found. Please run: python ml_model/train.py",
            "emoji": "⚠️"
        }

    model = joblib.load(model_path)
    X = pd.DataFrame([metrics])[FEATURES]

    risk_prob  = model.predict_proba(X)[0][1]
    risk_score = round(risk_prob * 100, 1)

    if risk_score < 30:
        status         = "SAFE"
        recommendation = "Safe to deploy. Auto-deployment can proceed."
        emoji          = "🟢"
    elif risk_score < 60:
        status         = "MODERATE"
        recommendation = "Moderate risk. Deploy carefully and monitor closely."
        emoji          = "🟡"
    else:
        status         = "HIGH_RISK"
        recommendation = "HIGH RISK — Pipeline blocked! Manual approval required."
        emoji          = "🔴"

    return {
        "risk_score":     risk_score,
        "status":         status,
        "recommendation": recommendation,
        "emoji":          emoji
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        metrics = json.loads(sys.argv[1])
    else:
        metrics = {
            "files_changed": 8, "lines_added": 120, "lines_deleted": 30,
            "hour_of_day": 14, "day_of_week": 2, "days_since_last_deploy": 3,
            "recent_failures": 1, "test_pass_rate": 0.92,
            "is_main_branch": 1, "num_contributors": 3
        }

    result = predict_risk(metrics)
    print(json.dumps(result, indent=2))

    if result["status"] == "HIGH_RISK":
        sys.exit(1)
